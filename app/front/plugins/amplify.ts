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

			// OPTIONAL - Manually set the authentication flow type. Default is 'USER_SRP_AUTH'
			// authenticationFlowType: 'ALLOW_REFRESH_TOKEN_AUTH',

			// OPTIONAL - Hosted UI configuration
			oauth: {
				domain: 'https://excellent-poc.auth.ap-northeast-1.amazoncognito.com',
				scope: [
					'email', 'openid', 'phone'
				],
				redirectSignIn: 'https://www.serverworks.co.jp/',
				redirectSignOut: 'http://localhost:3000/',
				responseType: 'token', // or 'token', note that REFRESH token will only be generated when the responseType is code
			},
		},
	})
})