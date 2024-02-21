<template>
  <div>
		<Alert ref="alert" />
    <div class="my-10">
      <v-row justify="center">
        <v-col cols="12" lg="6" sm="6">
        <v-card class="pa-5">
          <v-card-title class="d-flex justify-center mb-3">
            <div>
              <v-img :src="`/assets/logo.png`" contain height="200"></v-img>
            </div>
          </v-card-title>
          <v-form ref="signupForm" lazy-validation>
            <v-text-field
              v-model="username"
              label="Username"
              :rules="[rules.required]"
            ></v-text-field>
            <v-text-field
              v-model="email"
              label="Email"
              :rules="[rules.emailValidate]"
            ></v-text-field>
            <v-text-field
              label="Confirm Email"
              :rules="[rules.required, rules.emailConfirm(email)]"
            ></v-text-field>
            <v-text-field
              v-model="password"
              label="Password"
              type="password"
              :rules="[rules.passwordValidate]"
            ></v-text-field>
            <v-row>
              <v-col cols="12" lg="9" sm="9" class="d-flex justify-start">
                <div>
                  <NuxtLink :to="`/signin`">アカウントをお持ちの方はこちら</NuxtLink>
                </div>
              </v-col>
              <v-col cols="12" lg="3" sm="3" class="d-flex justify-end">
                <div>
                  <v-btn color="secondary" class="mr-4" type="submit" @click.prevent="signUp">signUp</v-btn>
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
import { Hub } from 'aws-amplify';

const username = ref<string>("")
const email = ref<string>("")
const password = ref<string>("")
const signupForm = ref<any>(null) // signupFormのref
const alert = ref<any>(null) // alertのref
const rules = useRules() // バリデーションルール

type SignUpParameters = {
  username: string;
  password: string;
  email: string;
};

type ConfirmSignUpParameters = {
  username: string;
  code: string;
};

type SignInParameters = {
  username: string;
  pw: string;
};

async function signUp() {
  // バリデーション
  const {valid, errors} = await signupForm.value.validate()
  if (!valid) {
    return
  }

  const { data, pending, error, refresh } = await useAsyncData<any>(
    "signup",
    () => {
      return Auth.signUp({
        username: username.value,
        password: password.value,
        attributes: {
            email: email.value, // optional
            // other custom attributes
        },
        autoSignIn: {
          // optional - enables auto sign in after user is confirmed
          enabled: true,
        },
      })
    }
  )
  if (!data.value || error.value) {
    console.error(error.value)
    alert.value.error(error.value)
    return
  } else {
      await navigateTo({
      path: '/confirm',
      query: {
        username: username.value,
      }
    })
  }
}
</script>