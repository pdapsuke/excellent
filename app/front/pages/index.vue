<template>
  <div>
    <div class="mb-3">
      <div class="text-h4">Items</div>
      {{ battingcenters }}
      <v-select
        label="prefectures"
        v-model="pref"
        :items="prefectures"
        item-title="prefName"
        item-value="prefCode"
        @update:modelValue="fetchCities"
      >
      </v-select>
      <v-select
        label="cities"
        :items="cities"
        item-title="cityName"
        item-value="cityCode"
        v-model="city"
      >
      </v-select>
      <v-btn
        color="primary"
        @click="submit"
      >検索</v-btn>
    </div>
    <div class="mb-3">
      <v-table         >
        <thead>
          <tr>
            <th class="text-left">バッティングセンター名</th>
            <th class="text-left">所在地</th>
            <th class="text-left">行った！数</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="battingcenter in battingcenters"
            :key="battingcenter.place_id">
            <td>{{ battingcenter.name }}</td>
            <td>{{ battingcenter.formatted_address }}</td>
            <td>{{ battingcenter.itta_count }}</td>
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

const pref = ref<number>(1)
const city = ref<number>()
let cities = ref<any>()
let battingcenters = ref<any>()

// 都道府県一覧取得
const { data: prefectures, pending:a, error:b, refresh: c } = await usePrefectureCityApi().getAllPrefecture()
const { data: citiesFromAPI, pending: d, error: e, refresh: f } = await usePrefectureCityApi().getCity(1)
// console.log(prefectures)
cities = citiesFromAPI

async function fetchCities() {
  // 市区町村一覧APIを呼び出す
  const { data, pending, error, refresh } = await usePrefectureCityApi().getCity(pref.value)
  // console.log(data)
  cities = data
}

async function submit() {
  let selectedPrefectureName = await prefectures.value.find((item) => item.prefCode == pref.value).prefName
  let selectedCityName = await cities.value.find((item) => item.cityCode == city.value).cityName
  const { data: result, pending:hoge, error: fuga, refresh: eiya } =  await useBattingCenterApi().post(`${selectedPrefectureName} ${selectedCityName}`)
  battingcenters.value = result.value
  for (const battingcenter of battingcenters.value) {
    // console.log(battingcenter)
    // 行った！数を返すAPIの呼び出し、行った数をオブジェクトのメンバーに追加
    const { data: itta_count, pending:itta_count_pending, error:itta_count_error , refresh: itta_count_refresh } =  await useBattingCenterApi().get(177)
    console.log(itta_count)
    battingcenter.itta_count = itta_count.value.count
    // console.log(battingcenter)
  } 
}
</script>