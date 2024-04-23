import asyncio
from typing import List
import torch
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

from fastapi import APIRouter, Depends
from konlpy.tag import Kkma
from pydantic import BaseModel
from starlette.requests import Request

from backend.rate_limiter import limiter
from backend.router_auth import Session, get_logged_user

router = APIRouter(prefix='/correction', tags=['correction'])

kkma = Kkma()


class PharseRequest(BaseModel):
    content: str


class PharseResponse(BaseModel):
    pharse: List[str]


@router.post("/phrases", response_model=PharseResponse)
@limiter.limit("60/seconds")
async def get_phrases(request: Request, pharse: PharseRequest, user: Session = Depends(get_logged_user)):
    loop = asyncio.get_running_loop()
    pharses = await loop.run_in_executor(None, kkma.sentences, pharse.content)
    return PharseResponse(pharse=pharses)


if torch.cuda.is_available():
    device = torch.device("cuda:0")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")

tokenizer = PreTrainedTokenizerFast.from_pretrained('./bart')
model = BartForConditionalGeneration.from_pretrained('./bart')
model.to(device)
print(f"[MODEL] device: {device.type}, {device.index}")


class CorrectionRequest(BaseModel):
    content: List[str]


class CorrectionResponse(BaseModel):
    content: List[str]


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def batches(items, batch_size):
    batches = [items[i: i + batch_size] for i in range(0, len(items), batch_size)]
    return batches


def run_model(contents: List[str], batch_size=8) -> List[str]:
    # 1. Tokenize and pad inputs in batches
    batch = [tokenizer([f"{tokenizer.bos_token}{p}{tokenizer.eos_token}"for p in batch], add_special_tokens=True, padding=True, truncation=True, return_tensors="pt",
                       max_length=128) for batch in batches(contents, batch_size)]

    # 2. Initialize empty list for storing generated texts
    generated_texts = []

    # 3. Process batches efficiently using a loop
    for batch_inputs in batch:
        batch_outputs = model.generate(batch_inputs['input_ids'].to(device), max_length=128)
        batch_generated_texts = [tokenizer.decode(output, skip_special_tokens=True) for output in batch_outputs]
        generated_texts.extend(batch_generated_texts)

    return generated_texts


@router.post("/correction", response_model=CorrectionResponse)
@limiter.limit("60/seconds")
async def correction(request: Request, correction: CorrectionRequest, user: Session = Depends(get_logged_user)):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, run_model, correction.content)
    return CorrectionResponse(content=result)
