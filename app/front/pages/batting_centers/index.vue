<template>
  <div>
    <Alert ref="alert" />
    <div class="mb-3">
      <div class="text-h4">Items</div>
    </div>
    <div class="d-flex justify-end">
      <div class="mr-3">
        <v-btn :icon="mdiRefresh" @click="refreshItems"></v-btn>
      </div>
      <div>
        <v-btn color="primary" :icon="mdiPlusBoxMultipleOutline" link to="/items/create"></v-btn>
      </div>
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
          <td><NuxtLink :to="`/items/${item.id}`">{{ item.id }}</NuxtLink></td>
          <td>{{ item.title }}</td>
          <td>
            <div class="d-flex">
              <div>
                <v-btn icon flat link :to="`/items/${item.id}/edit`">
                  <v-icon color="warning" :icon="mdiNoteEditOutline"></v-icon>
                </v-btn>
              </div>
              <div>
                <v-btn icon flat link @click="confirmDeletion.open({id: item.id})">
                  <v-icon color="error" :icon="mdiDeleteForeverOutline"></v-icon>
                </v-btn>
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </v-table>

    <ConfirmDialog 
      title="アイテムの削除"
      message="本当に削除しますか"
      confirmBtn="削除"
      cancelBtn="キャンセル"
      colorCancel="primary"
      colorConfirm="error"
      ref="confirmDeletion"
      @confirm="deleteItem"
    />
  </div>
</template>

<script setup lang="ts">
import { mdiPlusBoxMultipleOutline, mdiNoteEditOutline, mdiDeleteForeverOutline, mdiRefresh } from '@mdi/js'

// ミドルウェアによるログインチェック
definePageMeta({ middleware: ["auth"] })

const alert = ref<any>(null) // Alertコンポーネントのref
const confirmDeletion = ref<any>(null) //ConfirmDialogコンポーネントのref

// アイテム一覧取得
const { data: items, pending, error: getItemsError, refresh: refreshItems } = await useItemApi().getAll()

onMounted(() => {
  // アイテム一覧の取得に失敗した場合のエラー処理
  if (getItemsError.value instanceof Error) {
    alert.value.error(getItemsError.value)
    console.error(getItemsError.value)
    return
  }
})

// アイテム削除関数
async function deleteItem(confirm: boolean, params: {id: number}) {
  // 確認ダイアログで承認されたかをチェック
  if (!confirm) {
    return
  }
  // アイテム削除APIを呼び出し
  const { error } = await useItemApi().delete(params.id)
  // エラーの場合はアラート表示
  if (error.value instanceof Error) {
    alert.value.error(error.value)
    console.error(error.value)
    return
  }
  // 削除に成功したらアイテム一覧を取得
  refreshItems()
}
</script>