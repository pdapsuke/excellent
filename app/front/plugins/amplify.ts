import { Amplify } from 'aws-amplify'
import { run } from 'node:test'

export default defineNuxtPlugin(nuxtApp => {
	const runtimeConfig = useRuntimeConfig()
	Amplify.configure({
		Auth: {
			// REQUIRED - Amazon Cognito Region
			region: runtimeConfig.public.region,
			// OPTIONAL - Amazon Cognito User Pool ID
			userPoolId: runtimeConfig.public.userPoolId,

			// OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
			userPoolWebClientId: runtimeConfig.public.userPoolWebClientId,

			// OPTIONAL - This is used when autoSignIn is enabled for Auth.signUp
			// 'code' is used for Auth.confirmSignUp, 'link' is used for email link verification
			signUpVerificationMethod: 'code', // 'code' | 'link'
		},
	})
})