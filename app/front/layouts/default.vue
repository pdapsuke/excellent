<template>
  <v-app id="inspire">
    <!-- ヘッダー >>> -->
    <v-app-bar color="primary" :elevation="2">
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-app-bar-title>
        <div @click="useRouter().push('/')" class="font-weight-bold font-italic text-h5" style="cursor: pointer;">BASSEN.com</div>
      </v-app-bar-title>
      <div v-if="auth.authenticated()">ようこそ、{{ useAuth().getUsername() }}さん</div>
      <v-btn v-if="auth.authenticated()" :icon="mdiLogout" @click="logout()"></v-btn>
    </v-app-bar>
    <!-- <<< ヘッダー -->

    <!-- サイドメニュー >>> -->
    <v-navigation-drawer v-if="auth.authenticated()" v-model="drawer">
      <v-divider></v-divider>
      <!-- メニューリスト >>> -->
      <v-list>
        <template v-for="item in menu" :key="item.name" >
          <v-list-item link :to="item.path">
            <template v-slot:prepend>
              <v-icon>{{ item.icon }}</v-icon>
            </template>
            <v-list-item-title>{{ item.name }}</v-list-item-title>
          </v-list-item>
        </template>
      </v-list>
      <!-- メニューリスト >>> -->
    </v-navigation-drawer>
    <!-- <<< サイドメニュー -->

    <!-- コンテンツ >>> -->
    <v-main>
      <v-container class="py-8 px-6" fluid >
        <slot />
      </v-container>
    </v-main>
    <!-- <<< コンテンツ -->

    <!-- フッター >>> -->
    <v-footer class="footer justify-center">
      <div>&copy; 2023 Bassen.com</div>
    </v-footer>
    <!-- <<< フッター -->
  </v-app>
</template>

<script setup lang="ts">
import { mdiAccount, mdiMapSearchOutline, mdiLogout } from '@mdi/js'
import { Auth } from 'aws-amplify'

const auth = useAuth()

interface MenuItem {
  icon: string
  name: string
  path: string
}

const drawer = ref<boolean>(false)
const menu = ref<Array<MenuItem>>([
  {
    icon: mdiAccount,
    name: "Mypage",
    path: "/mypage/IttaBattingCenters",
  },
  {
    icon: mdiMapSearchOutline,
    name: "Search",
    path: "/",
  },
])

async function logout() {
  try {
  await Auth.signOut()
  } catch (error) {
    console.log('error signing out', error)
  }
  useAuth().logout()
  useRouter().push({path: "/signin"})
}
</script>

<style lang="scss">
.footer {
  width: 100%;
  position: absolute;
  bottom: 0;
}
</style>