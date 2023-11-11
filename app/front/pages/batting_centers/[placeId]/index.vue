<template>
  <div>
    <div class="mb-3">
      <div class="text-h4">{{ detail.result.name }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { mdiNoteEditOutline, mdiDeleteForeverOutline } from '@mdi/js'


// パスパラメータ(itemId)を取得
const { placeId } = useRoute().params
console.log(placeId)
const { data: detail, pending, error: getItemError, refresh } = await useBattingCenterApi().getDetail(placeId)
console.log(detail)


</script>
