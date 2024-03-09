<template>
<div>
  <Alert ref="alert" />
  <div class="my-10">
    <v-row justify="center">
      <v-col cols="12" lg="6" sm="6">
      <v-card class="pa-5">
        <v-card-title class="d-flex justify-center mb-3">
          <div>
            <v-img :src="imgUrl" contain height="200"></v-img>
          </div>
        </v-card-title>
        <v-form ref="loginForm" lazy-validation>
          <v-text-field
            v-model="username"
            label="Username"
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Password"
            type="password"
          ></v-text-field>
            <v-row>
              <v-col cols="12" lg="9" sm="9" class="d-flex justify-start">
                <div>
                  <NuxtLink :to="`/signup`">アカウントをお持ちでない方はこちら</NuxtLink>
                </div>
              </v-col>
              <v-col cols="12" lg="3" sm="3" class="d-flex justify-end">
                <div>
                  <v-btn color="secondary" class="mr-4" type="submit" @click.prevent="signIn">signin</v-btn>
                </div>
              </v-col>
            </v-row>
        </v-form>
      </v-card>
      </v-col>
    </v-row>
  </div>
</div>
</template>

<script setup lang="ts">
import { Auth } from 'aws-amplify';
import imgUrl from '@/assets/logo.png';

// テキストフィールドにバインドされるデータ
const username = ref<string>("")
const password = ref<string>("")
const alert = ref<any>(null)  // Alertコンポーネントのref

async function signIn() {
  const { data, error: cognitoError } = await useAsyncData<any>(
    "cognitoSignIn",
    () => {
      return Auth.signIn(username.value, password.value)
    }
  )

  // ログイン失敗ならアラートとログを出力してreturn
  if (!data.value || cognitoError.value) {
    alert.value.error(cognitoError.value)
    console.error(cognitoError.value)
    return
  }

  // ログイン成功ならCookieにトークンをセット
  useAuth().login(data.value.signInUserSession.idToken.jwtToken)
  console.log(data.value.signInUserSession.idToken.jwtToken)

  // バックエンドにサインインリクエスト
  const { error: backendError } = await useUserApi().signIn(data.value.signInUserSession.idToken.jwtToken)

  // ログイン失敗ならアラートとログを出力してreturn
  if (backendError.value) {
    alert.value.error(backendError.value)
    console.error(backendError.value)
    return
  }
  useRouter().push({path: "/"})
}

</script>