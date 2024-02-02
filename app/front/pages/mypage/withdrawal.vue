<template>
  <div>
    <Alert ref="alert" />
    <div class="mb-10">
      <v-row class="justify-center">
        <NuxtLink :to="`/mypage/IttaBattingCenters`">行った！したバッティングセンター</NuxtLink>
        <v-divider class="border-opacity-90 mx-3" color="black" :thickness="1" vertical></v-divider>
        <NuxtLink :to="`/mypage/PostedMachineInformations`">投稿したマシン情報</NuxtLink>
        <v-divider class="border-opacity-90 mx-3" color="black" :thickness="1" vertical></v-divider>
        <NuxtLink :to="`/mypage/AttaMachineInformations`">あった！したマシン情報</NuxtLink>
        <v-divider class="border-opacity-90 mx-3" color="black" :thickness="1" vertical></v-divider>
        <NuxtLink :to="`/mypage/NakattaMachineInformations`">なかった！したマシン情報</NuxtLink>
        <v-divider class="border-opacity-90 mx-3" color="black" :thickness="1" vertical></v-divider>
        <div class="font-weight-bold">アカウント削除</div>
      </v-row>
    </div>
    <v-list lines="one" class="justify-start">
      <v-list-item
        v-for="(item, i) in checkListsForDeletion"
        :key="i"
      >
        <template v-slot:prepend>
          <v-icon color="error" :icon="mdiCheck"></v-icon>
        </template>
        <v-list-item-title v-text="checkListsForDeletion[i]"></v-list-item-title>
      </v-list-item>
    </v-list>
    <div class="d-flex justify-end">
      <v-btn color="secondary" class="mr-4" @click="confirmDeletion.open()">ユーザー削除</v-btn>
    </div>
  </div>
  <!-- 削除確認ダイアログ -->
  <ConfirmDialog
    title="ユーザー削除"
    message="本当に削除しますか"
    confirmBtn="削除"
    cancelBtn="キャンセル"
    colorCancel="primary"
    colorConfirm="error"
    ref="confirmDeletion"
    @confirm="handleDeleteUser">
  </ConfirmDialog>
</template>

<script setup lang="ts">
import { mdiCheck } from '@mdi/js'
import { Auth } from 'aws-amplify'

const checkListsForDeletion = [
  "この操作は元に戻せません",
  "投稿したマシン情報は削除されます"
]

const email = useAuth().getUserEmail()
const alert = ref<any>(null)
const confirmDeletion = ref<any>(null)

async function handleDeleteUser(confirm: boolean) {
  if (!confirm) { return }
  try {
    // DB上のユーザー情報を削除
    const { error: deleteUserOnDBError} = await useUserApi().deleteUser(email)
    if (deleteUserOnDBError.value) {
      alert.value.error(deleteUserOnDBError.value)
      return
    }
    const user = await Auth.currentAuthenticatedUser()
    user.deleteUser((error, data) => {
      if (error) {
        console.error(error)
        alert.value.error(error)
      } else {
        useAuth().logout()
        alert.value.success("ユーザーが削除されました")
        setTimeout(() => {
          useRouter().push({path: "/signin"})
        }, 2000)
      }
    })
  } catch (error) {
    console.log(error)
    alert.value.error(error)
  }
}
</script>