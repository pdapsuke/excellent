<template>
  <div>
    <Alert ref="alert" />
    <div class="mb-10">
      <v-row class="justify-center">
        <div class="font-weight-bold">行った！したバッティングセンター</div>
        <v-divider class="border-opacity-90 mx-3" color="black" :thickness="1" vertical></v-divider>
        <NuxtLink :to="`/mypage/PostedMachineInformations`">投稿したマシン情報</NuxtLink>
        <v-divider class="border-opacity-90 mx-3" color="black" :thickness="1" vertical></v-divider>
        <NuxtLink :to="`/mypage/AttaMachineInformations`">あった！したマシン情報</NuxtLink>
        <v-divider class="border-opacity-90 mx-3" color="black" :thickness="1" vertical></v-divider>
        <NuxtLink :to="`/mypage/NakattaMachineInformations`">なかった！したマシン情報</NuxtLink>
        <v-divider class="border-opacity-90 mx-3" color="black" :thickness="1" vertical></v-divider>
        <NuxtLink :to="`/mypage/withdrawal`">アカウント削除</NuxtLink>
      </v-row>
    </div>
    <div class="mb-3">
			<div v-if="battingcenters.length == 0">行った！したバッティングセンターはありません</div>
      <v-table v-else class="d-flex justify-center">
        <thead>
          <tr>
            <th class="text-left">バッティングセンター情報</th>
            <th class="text-left"></th>
            <th class="text-left"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="battingcenter in battingcenters"
            :key="battingcenter.place_id">
            <td>
              <div class="d-flex justify-start mt-3">
                <div><NuxtLink :to="`/batting_centers/${battingcenter.id}`">{{ battingcenter.name }}</NuxtLink></div>
              </div>
              <div class="d-flex justify-start mb-3">
                <div>{{ battingcenter.formatted_address }}</div>
              </div>
            </td>
            <td><div class="font-weight-bold text-secondary font-italic text-h5">{{ battingcenter.itta_count }}</div></td>
            <td>
              <IttaButton
                :itta="battingcenter.itta"
                @click="itta(battingcenter)"
              ></IttaButton>
            </td>
          </tr>
        </tbody>
      </v-table>      
    </div>
  </div>
</template>
<script setup lang="ts">
// ミドルウェアによるログインチェック
definePageMeta({ middleware: ["auth"] })

interface BattingCenter {
    id: number
    place_id: string
    name: string
    formatted_address: string
    photos: any[] | undefined
    itta_count: number
    itta: boolean
}

interface IttaResponse {
    id: number
    itta_count: number
    itta: boolean
}

const alert = ref<any>(null)

let battingcenters = ref<BattingCenter[]>()
let ittaResponse = ref<IttaResponse>()
let ittaError = ref<any>()

// 行った！したバッティングセンターの一覧を取得
const { data, error } =  await useUserApi().getMyIttaBattingCenters()

if (!data.value || error.value) {
	alert.value.error(error.value)
	console.error(error.value)
} else {
	battingcenters.value = data.value
}

// 行った！フラグに応じて行った！を登録/解除
async function itta(battingcenter: BattingCenter) {

  // 行った！フラグがfalseの場合、行った！ユーザーの追加
  if (battingcenter.itta == false) {
    ({ data: ittaResponse, error: ittaError } =  await useBattingCenterApi().addIttaUser(battingcenter.id))

  // 行った！フラグがtrueの場合、行った！ユーザーの削除
  } else if (battingcenter.itta == true) {
    ({data: ittaResponse, error: ittaError } =  await useBattingCenterApi().removeIttaUser(battingcenter.id))

  // 行った！フラグがtrue, false以外の場合、エラー出力
  } else {
    alert.value.error("Bad Request")
    console.error("Bad Request")
    return
  }

  if (!ittaResponse.value || ittaError.value) {
    alert.value.error(ittaError.value)
    console.error(ittaError.value)
    return
  }

  // 行った！フラグと行った数を更新
  battingcenter.itta = ittaResponse.value.itta
  battingcenter.itta_count = ittaResponse.value.itta_count
}

</script>
