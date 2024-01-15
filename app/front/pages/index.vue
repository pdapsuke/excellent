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
// refは明示的なインポートは不要だが、説明のために記述している
import { ref } from 'vue'
import { mdiNoteEditOutline, mdiDeleteForeverOutline } from '@mdi/js'

const pref = ref<number>()
const city = ref<number>()
const alert = ref<any>(null)
const rules = useRules()
const prefForm = ref<any>(null)
const cityForm = ref<any>(null)
const searchForm = ref<any>(null)
const username = useAuth().getUsername<string>()

let cities = ref<any>()
let battingcenters = ref<any>()

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
}

// async function getIttaCount(battingcenter: any) {
//     // 行った！数を返すAPIの呼び出し、行った数をオブジェクトのメンバーに追加
//     const { data: itta_count, pending:itta_count_pending, error:itta_count_error , refresh: itta_count_refresh } =  await useBattingCenterApi().get(battingcenter.place_id)
//     battingcenter.itta_count = itta_count.value.count  
// }

async function submit() {
  const { valid: searchFormValid } = await searchForm.value.validate()  // 追加: バリデーション実行
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

// 行った！を登録
async function itta(battingcenter: any) {
  const { data: itta_response, pending:itta_pending, error: itta_error, refresh: itta_refresh } =  await useUserApi().updateItta({
    username: username,
    place_id: battingcenter.place_id,
    itta: battingcenter.itta,
  })
  await getIttaCount(battingcenter)
}

// prefのitem-valueが変更された場合にfetchCitiesを呼び出す
watch(pref, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    fetchCities();
  }
});

</script>
