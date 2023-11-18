<template>
  <div>
    <div class="mb-3">
      <div class="text-h4">{{ detail.name }}</div>
      <v-select
        v-model="ball_speeds"
        variant="outlined"
        label="球速"
        :items="[{id: 1, value: 60}, {id: 2, value: 70}, {id: 3, value: 80}]"
        item-title="value"
        item-value="value"
        clearable
        multiple
        dense
      ></v-select>
      <v-select
        v-model="pitch_types"
        variant="outlined"
        label="球種"
        :items="[{id: 1, value: 'ストレート'}, {id: 2, value: 'カーブ'}, {id: 3, value: 'フォーク'}]"
        item-title="value"
        item-value="value"
        clearable
        multiple
        dense
      ></v-select>
      <v-select
        v-model="batter_box"
        variant="outlined"
        label="打席"
        :items="[{id: 1, value: '左'}, {id: 2, value: '右'}, {id: 3, value: '両'}]"
        item-title="value"
        item-value="value"
        clearable
        dense
      ></v-select>
      <div class="d-flex justify-end">
        <v-btn color="secondary" class="mr-4" type="submit" @click.prevent="post">投稿</v-btn>
      </div>
      <div class="text-h4">球速{{ ball_speeds }}</div>
      <div class="text-h4">球種{{ pitch_types }}</div>
      <div class="text-h4">打席{{ batter_box }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { mdiNoteEditOutline, mdiDeleteForeverOutline } from '@mdi/js'


// パスパラメータ(itemId)を取得
const { placeId } = useRoute().params
const ball_speeds = ref<number[]>([])
const pitch_types = ref<string[]>([])
const batter_box = ref<string>("")
const username = useAuth().getUsername<string>()

const { data: detail, pending, error, refresh } = await useBattingCenterApi().getDetail(placeId)

async function post() {
  

  const { data: postResponse, pending: postPending, error: postError, refresh: postRefresh } = await useMachineInformationApi().post({
    ballspeed: ball_speeds.value,
    pitch_type: pitch_types.value,
    batter_box: batter_box.value,
    username: username,
    place_id: placeId,
  })

  console.log(postResponse)

}

</script>
