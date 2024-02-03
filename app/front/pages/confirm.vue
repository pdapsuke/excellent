<template>
	<div>
		<Alert ref="alert" />
		<div class="my-10">
				<v-row justify="center">
				<v-col cols="12" lg="4" sm="6">
				<v-card class="pa-5">
						<v-card-title class="d-flex justify-center mb-3">
						<div>
								<v-img :src="`/logo-no-background.png`" contain height="180"></v-img>
						</div>
						</v-card-title>
						<v-form ref="confirmForm" lazy-validation>
						<v-text-field
								v-model="code"
								label="verification code"
								:rules="[rules.required]"
						></v-text-field>
						<div class="d-flex justify-end">
								<v-btn color="secondary" class="mr-4" type="submit" @click.prevent="confirmSignUp">confirm</v-btn>
						</div>
						</v-form>
				</v-card>
				</v-col>
				</v-row>
		</div>
	</div>
</template>

<script setup lang="ts">
import { Auth } from 'aws-amplify'
import { mdiCheck } from '@mdi/js'

const code = ref<string>("")
const username = useRoute().query.username
const confirmForm = ref<any>(null) // confirmFormのref
const alert = ref<any>(null) // alertコンポーネントのref
const rules = useRules() // バリデーションルール

// 認証コードでサインアップを確認
async function confirmSignUp() {
  // バリデーション
  const {valid, errors} = await confirmForm.value.validate()
  if (!valid) {
    return
  }
  const { data, pending, error, refresh } = await useAsyncData<any>(
    "confirmSignup",
    () => {
      Auth.confirmSignUp(username, code.value)
    }
  )
  if (error.value) {
    console.error(error.value)
		alert.value.error(error.value)
    return
  } else {
		// サインアップ確認後、/signinにリダイレクト
		alert.value.success("ユーザーが作成されました")
		setTimeout(() => {
			useRouter().push({path: "/signin"})
		}, 2000)
	}
}
</script>
