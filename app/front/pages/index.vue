<template>
  <div>
    <Alert ref="alert" />
    <div class="mb-3">
      <div class="text-h4">Items</div>
      <v-form ref="searchForm" lazy-validation>
        <v-select
          label="prefectures"
          v-model="pref"
          :items="prefectures"
          :rules="[rules.required]"
          item-title="prefName"
          item-value="prefCode"
        >
        </v-select>
        <v-select
          label="cities"
          :items="cities"
          :rules="[rules.required]"
          item-title="cityName"
          item-value="cityCode"
          v-model="city"
        >
        </v-select>
      </v-form>
      <v-btn
        color="primary"
        @click="submit"
      >検索</v-btn>
    </div>
    <div class="mb-3">
      <v-table>
        <thead>
          <tr>
            <th class="text-left">バッティングセンター名</th>
            <th class="text-left">所在地</th>
            <th class="text-left">行った！数</th>
            <th class="text-left">行った！ボタン</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="battingcenter in battingcenters"
            :key="battingcenter.place_id">
            <td><NuxtLink :to="`/batting_centers/${battingcenter.place_id}`">{{ battingcenter.name }}</NuxtLink></td>
            <td>{{ battingcenter.formatted_address }}</td>
            <td>{{ battingcenter.itta_count }}</td>
            <td>
              <v-switch
                v-model="battingcenter.itta"
                color="primary"
                hide-details
                true-value="yes"
                false-value="no"
                :label="`${battingcenter.itta}`"
                @change="itta(battingcenter)"
              ></v-switch>
            </td>
          </tr>
        </tbody>
      </v-table>      
    </div>
  </div>
</template>

<script setup lang="ts">
import { mdiNoteEditOutline, mdiDeleteForeverOutline } from '@mdi/js'

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
  const { valid: searchFormValid } = await searchForm.value.validate()  // バリデーション実行
  if (!searchFormValid) {
    return
  }
  let selectedPrefectureName = await prefectures.value.find((item) => item.prefCode == pref.value).prefName
  let selectedCityName = await cities.value.find((item) => item.cityCode == city.value).cityName
  const { data: results, error: searchError } =  await useBattingCenterApi().searchBattingCenters(`${selectedPrefectureName}${selectedCityName}`)

  if (!results.value || searchError.value) {
    alert.value.error(searchError.value)
    console.error(fetchCitiesError.value)
    return
  }

  battingcenters.value = results.value
}

// 行った！フラグに応じて行った！を登録/解除
async function itta(battingcenter: BattingCenter) {

  // 行った！フラグが"yes"の場合、行った！ユーザーの追加
  if (battingcenter.itta == "yes") {
    ({ data: ittaResponse, error: ittaError } =  await useBattingCenterApi().addIttaUser(battingcenter.id))

  // 行った！フラグが"no"の場合、行った！ユーザーの削除
  } else if (battingcenter.itta == "no") {
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
