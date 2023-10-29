<template>
<div>
  <div class="my-10">
    <v-row justify="center">
      <v-col cols="12" lg="4" sm="6">
      <v-card class="pa-5">
        <v-card-title class="d-flex justify-center mb-3">
          <div>
            <v-img :src="`/logo-no-background.png`" contain height="180"></v-img>
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
          <div class="d-flex justify-end">
            <v-btn color="secondary" class="mr-4" type="submit" @click.prevent="signIn">signin</v-btn>
          </div>
        </v-form>
      </v-card>
      </v-col>
    </v-row>
  </div>
</div>
</template>

<script setup lang="ts">
import { Auth } from 'aws-amplify';

// テキストフィールドにバインドされるデータ
const username = ref<string>("")
const password = ref<string>("")
const loginForm = ref<any>(null)  // v-form要素のref

async function signIn() {
  const { data, pending, error, refresh } = await useAsyncData<any>(
    "login",
    () => {
      return Auth.signIn(username.value, password.value)
    }
  )
  if (!data.value || error.value) {
    console.error(error.value)
    return
  }
  useAuth().login(data.value.signInUserSession.idToken.jwtToken)
  useRouter().push({path: "/"})
}

</script>