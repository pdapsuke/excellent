<template>
	<div>
		<Alert ref="alert" />
		<div class="my-10">
      <v-row justify="center">
				<v-col cols="12" lg="6" sm="6">
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
							<v-row>
								<v-col cols="12" lg="6" sm="6" class="d-flex justify-start">
									<div>
											<v-btn color="info" class="mr-4" type="submit" @click.prevent="resendConfirmationCode">resend code</v-btn>
									</div>
								</v-col>
								<v-col cols="12" lg="6" sm="6" class="d-flex justify-end">
									<div>
											<v-btn color="error" class="mr-4" type="submit" @click.prevent="confirmSignUp">confirm</v-btn>
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
import { Auth } from 'aws-amplify'
import { mdiCheck } from '@mdi/js'

// ミドルウェアによるログインチェック
definePageMeta({ middleware: ["disable-direct-access"] })

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
	try {
    await Auth.confirmSignUp(username, code.value)
	} catch(error) {
		alert.value.error("認証コードが違います")
    return
	}
	alert.value.success("ユーザーが作成されました")
	setTimeout(() => {
		useRouter().push({path: "/signin"})
	}, 2000)
}

// 認証コードを再送
async function resendConfirmationCode() {
  const { data, pending, error, refresh } = await useAsyncData<any>(
    "resendConfirmationCode",
    () => {
      Auth.resendSignUp(username)
    }
  )
  if (error.value) {
    console.error(error.value)
		alert.value.error(error.value)
    return
  } else {
		alert.value.success("認証コードを再送しました")
	}
}

</script>
