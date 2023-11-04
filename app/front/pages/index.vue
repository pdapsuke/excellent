<template>
  <div>
    <div class="mb-3">
      <div class="text-h4">Items</div>
      {{ pref }}
      {{ city }}
      {{ cities }}
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
    </div>
    <v-table>
      <thead>
        <tr>
          <th>id</th>
          <th>title</th>
          <th>action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.title }}</td>
          <td>
            <div class="d-flex">
              <div>
                <v-btn icon flat >
                  <v-icon color="warning" :icon="mdiNoteEditOutline"></v-icon>
                </v-btn>
              </div>
              <div>
                <v-btn icon flat >
                  <v-icon color="error" :icon="mdiDeleteForeverOutline"></v-icon>
                </v-btn>
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<script setup lang="ts">
// refは明示的なインポートは不要だが、説明のために記述している
import { ref } from 'vue'
import { mdiNoteEditOutline, mdiDeleteForeverOutline } from '@mdi/js'

const pref = ref<number>(1)
const city = ref<number>()
let cities = ref<any>()

const items = ref<any>([
    {id: "1", "title": "Chapter1 FastAPI入門"},
    {id: "2", "title": "Chapter2 RDB入門"},
    {id: "3", "title": "Chapter2.5 SQLAlchemyを利用したデータベースの操作"},
    {id: "4", "title": "Chapter3 Alembicを利用したマイグレーションを実装してみよう"},
    {id: "5", "title": "Chapter4 FastAPIでCRUDを実装してみよう"},
])

// 都道府県一覧取得
const { data: prefectures, pending:a, error:b, refresh: c } = await usePrefectureCityApi().getAllPrefecture()
const { data: citiesFromAPI, pending: d, error: e, refresh: f } = await usePrefectureCityApi().getCity(1)
cities = citiesFromAPI

async function fetchCities() {
  // 市区町村一覧APIを呼び出す
  const { data, pending, error, refresh } = await usePrefectureCityApi().getCity(pref.value)
  cities = data
}

</script>