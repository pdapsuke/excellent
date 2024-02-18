<template>
  <div>
    <Alert ref="alert" />
    <div class="mb-3">
      <v-list lines="one" class="mb-3 mx-5">
        <v-list-item
          v-for="(item, i) in checkListsForSearch"
          :key="i">
          <template v-slot:prepend>
            <v-icon color="primary" :icon="mdiCheck"></v-icon>
          </template>
          <v-list-item-title v-text="checkListsForSearch[i]"></v-list-item-title>
        </v-list-item>
      </v-list>
      <v-row class="mx-5">
        <v-col cols="12" lg="10" sm="10">
          <div>
            <v-form ref="searchForm" lazy-validation>
              <v-row>
                <v-col cols="12" lg="6" sm="6">
                  <div>
                    <v-select
                      label="都道府県"
                      v-model="pref"
                      :items="prefectures"
                      :rules="[rules.required]"
                      item-title="prefName"
                      item-value="prefCode"
                    ></v-select>
                  </div>
                </v-col>
                <v-col cols="12" lg="6" sm="6">
                  <div>
                    <v-select
                      label="市区町村"
                      :items="cities"
                      :rules="[rules.required]"
                      item-title="cityName"
                      item-value="cityCode"
                      v-model="city"
                    ></v-select>
                  </div>
                </v-col>
              </v-row>
            </v-form>
          </div>
        </v-col>
        <v-col cols="12" lg="2" sm="2">
          <div>
            <v-btn
              color="primary"
              @click="submit"
            >検索</v-btn>
          </div>
        </v-col>
      </v-row>
    </div>
    <div v-if="loading==true" class="d-flex justify-center ma-5">
      <v-progress-circular
        color="primary"
        indeterminate
        :size="49"
        :width="7"
      ></v-progress-circular>
    </div>
    <div v-if="loading==false">
      <v-table class="d-flex justify-start">
        <thead>
          <tr>
            <th class="text-left"></th>
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
              <div class="d-flex justify-center ma-5">
                <v-img
                  :src="battingcenter.photos"
                  contain
                  max-height="300"
                  max-width="300"
                ></v-img>
              </div>
            </td>
            <td>
              <div class="d-flex justify-start">
                <div><NuxtLink :to="`/batting_centers/${battingcenter.id}`">{{ battingcenter.name }}</NuxtLink></div>
              </div>
              <div class="d-flex justify-start">
                <div>{{ battingcenter.formatted_address }}</div>
              </div>
            </td>
            <td>{{ battingcenter.itta_count }}</td>
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
import { mdiCheck } from '@mdi/js'

// ミドルウェアによるログインチェック
definePageMeta({ middleware: ["auth"] })

interface City {
  prefCode: number
  cityCode: string
  cityName: string
  bigCityFlag: string
}

interface BattingCenter {
    id: number
    place_id: string
    name: string
    formatted_address: string
    photos: any[] | undefined
    itta_count: number
    itta: string
}

interface IttaResponse {
    id: number
    itta_count: number
    itta: string
}

const pref = ref<number>()
const alert = ref<any>(null)
const prefForm = ref<any>(null)
const cityForm = ref<any>(null)
const searchForm = ref<any>(null)
const rules = useRules()
const loading = ref<boolean>(null) // ローディングスピナー表示フラグ
const checkListsForSearch = [
  "都道府県、市区町村を選んでバッティングセンターを探そう！",
  "各バッティングセンターに設置されているピッチングマシン情報を共有しよう！",
  "たまにバッティングセンター以外の施設が出てくるのはご愛嬌",
]

let city = ref<number>()
let cities = ref<City[]>()
let battingcenters = ref<BattingCenter[]>()
let ittaResponse = ref<IttaResponse>()
let ittaError = ref<any>()

// 都道府県一覧取得
const { data: prefectures, error: fetchPrefecturesError } = await usePrefectureCityApi().getAllPrefecture()

// 市区町村一覧APIを呼び出す
async function fetchCities() {
  console.log("fetchCities function called");
  const { data: citiesResponse, error: fetchCitiesError } = await usePrefectureCityApi().getCity(pref.value)

  // 取得失敗した場合、アラートとログを出力してreturn
  if (!citiesResponse.value || fetchCitiesError.value) {
    alert.value.error(fetchCitiesError.value)
    console.error(fetchCitiesError.value)
    return
  }

  cities.value = citiesResponse.value
  city.value = cities.value[0].cityCode
}

async function submit() {
  // フォームバリデーション
  const { valid: searchFormValid } = await searchForm.value.validate()  // バリデーション実行
  if (!searchFormValid) {
    return
  }
  loading.value = true // ローディングスピナー表示
  let selectedPrefectureName = await prefectures.value.find((item) => item.prefCode == pref.value).prefName
  let selectedCityName = await cities.value.find((item) => item.cityCode == city.value).cityName
  const { data: results, error: searchError } =  await useBattingCenterApi().searchBattingCenters(`${selectedPrefectureName}${selectedCityName}`)

  if (!results.value || searchError.value) {
    alert.value.error(searchError.value)
    console.error(fetchCitiesError.value)
    loading.value = false // ローディングスピナー非表示
    return
  }

  battingcenters.value = results.value
  loading.value = false // ローディングスピナー非表示
}

// 行った！フラグに応じて行った！を登録/解除
async function itta(battingcenter: BattingCenter) {

  // 行った！フラグが"yes"の場合、行った！ユーザーの追加
  if (battingcenter.itta == "no") {
    ({ data: ittaResponse, error: ittaError } =  await useBattingCenterApi().addIttaUser(battingcenter.id))

  // 行った！フラグが"no"の場合、行った！ユーザーの削除
  } else if (battingcenter.itta == "yes") {
    ({data: ittaResponse, error: ittaError } =  await useBattingCenterApi().removeIttaUser(battingcenter.id))

  // 行った！フラグが"yes", "no"以外の場合、エラー出力
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

// prefのitem-valueが変更された場合にfetchCitiesを呼び出す
watch(pref, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    fetchCities()
  }
});

</script>
