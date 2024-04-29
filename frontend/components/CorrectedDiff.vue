<script setup lang="ts">
import {type Change, diffChars} from "diff"
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import type {Ref} from "vue";

const props = defineProps<{origin: string, updated: string, id: string, nth: number, isLastElement: boolean}>()
const emit = defineEmits<{update: [idx: number, value: string], post: [idx: number, origin: string, fixed: string]}>()

const diffParts: Ref<Change[]> = ref([])
const hasDiff = ref(false)
const originText = ref("")
const updatedText = ref("")
const fixedText = ref("")
const update = ref(false)

const runDiff = (origin: string, updated: string) => {
  diffParts.value = diffChars(origin, updated)
  hasDiff.value = diffParts.value.some(part => part.added || part.removed)
  originText.value = origin
  updatedText.value = fixedText.value = updated
}

const emitUpdate = () => {
  emit('update', props.nth, fixedText.value)
  runDiff(updatedText.value.trim(), fixedText.value.trim())
}

const emitPost = () => {
  emit('post', props.nth, originText.value.trim(), fixedText.value.trim())
  update.value = false
  runDiff(updatedText.value.trim(), fixedText.value.trim())
}

runDiff(`${props.origin}`, `${props.updated}`)

</script>

<template>
  <Suspense>
    <div v-bind:class="`box has-background-${hasDiff ? 'info' : 'success'}`" v-bind:id="`${props.id}-${props.nth}`">
      <div class="columns">
        <div class="column is-10">
          <template v-for="(member, index) in diffParts" v-bind:key="`member-${index}`">
            <span v-if="member.added" class="has-text-primary-50" style="text-decoration: underline">{{member.value }}</span>
            <span v-else-if="member.removed" class="has-text-danger" style="text-decoration: line-through">{{member.value}}</span>
            <span v-else class="has-text-white">{{member.value}}</span>
          </template>
          <textarea class="input" style="width: 100%; margin-top: 5px;" v-model="fixedText" v-if="update"/>
        </div>
        <div class="column is-2">
          <a class="button is-light" v-bind:href="`#${props.id}-${props.nth + 1}`" v-if="!props.isLastElement"><font-awesome-icon :icon="['fas', 'angle-down']" /></a>
          <a class="button is-light" href="#content" v-else><font-awesome-icon :icon="['fas', 'angle-up']"/></a>
          <button class="button is-primary" style="margin-left: 5px;" @click="update = !update" v-if="!update">
            <font-awesome-icon :icon="['fas', 'pen']" />
          </button>
          <button class="button is-primary" style="margin-left: 5px;" @click="update = !update; emitUpdate()" v-else>
            <font-awesome-icon :icon="['fas', 'check']" />
          </button>
          <button class="button is-warning" style="margin-left: 5px" v-if="update" @click="update = !update; emitPost()" :disabled="!hasDiff">
            <font-awesome-icon :icon="['fas', 'comments']" />
          </button>
        </div>
      </div>
    </div>
  </Suspense>
</template>

<style scoped>
  [id].box {
    scroll-margin-top: 20vh;
  }
</style>