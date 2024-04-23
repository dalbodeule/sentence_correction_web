<script setup lang="ts">
import { diffChars } from "diff"

const props = defineProps(['origin', 'updated', 'id'])

const diffParts = diffChars(`${props.origin}`, `${props.updated}`)
const hasDiff = diffParts.some(part => part.added || part.removed)

const updatedText = props.updated ?? ""
console.log(diffParts)
</script>

<template>
  <Suspense>
    <div v-bind:class="`box has-background-${hasDiff ? 'info' : 'success'}`" v-bind:id="props.id">
      <template v-for="(member, index) in diffParts" v-bind:key="`member-${index}`">
        <span v-if="member.added" class="has-text-primary-50">{{member.value }}</span>
        <span v-else-if="member.removed" class="has-text-danger" style="text-decoration: line-through">{{member.value}}</span>
        <span v-else class="has-text-white">{{member.value}}</span>
      </template>
    </div>
  </Suspense>
</template>

<style scoped>

</style>