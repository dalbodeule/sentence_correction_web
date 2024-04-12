from typing import List
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
from fastapi import APIRouter, Depends
from konlpy.tag import Kkma
from pydantic import BaseModel
from starlette.requests import Request

from rate_limiter import limiter
from router_auth import Session, get_logged_user

router = APIRouter(prefix='/correction', tags=['correction'])

kkma = Kkma()


class PharseRequest(BaseModel):
    content: str


class PharseResponse(BaseModel):
    pharse: List[str]


@router.post("/phrases", response_model=PharseResponse)
@limiter.limit("60/seconds")
async def get_phrases(request: Request, pharse: PharseRequest, user: Session = Depends(get_logged_user)):
    pharses = kkma.sentences(pharse.content)
    return PharseResponse(pharse=pharses)


tokenizer = PreTrainedTokenizerFast.from_pretrained('gogamza/kobart-base-v2', bos_token="<s>", eos_token="</s>", unk_token="<unk>", pad_token="<pad>", mask_token="<mask>")
model = BartForConditionalGeneration.from_pretrained('gogamza/kobart-base-v2')


class CorrectionRequest(BaseModel):
    content: List[str]


class CorrectionResponse(BaseModel):
    content: List[str]


@router.post("/correction", response_model=CorrectionResponse)
@limiter.limit("60/seconds")
async def correction(request: Request, correction: CorrectionRequest, user: Session = Depends(get_logged_user)):
    generated_texts = []

    for text in correction.content:
        input_ids = tokenizer.encode(f"<s>{text}</s>", return_tensors="pt")
        output = model.generate(input_ids, max_length=128)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        generated_texts.append(generated_text)

    return CorrectionResponse(content=generated_texts)