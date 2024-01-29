// 各ページを読み込む前にトークンを検証する
export default defineNuxtRouteMiddleware(async(to, from) => {
  // Cookieからトークン取得, 取得できなければ'/signin'にリダイレクト
  const token = useAuth().getToken()
  if (token==null) {
    return navigateTo('/signin')
  }

  let authenticated: boolean | undefined = undefined // トークン検証用フラグ

  async function validateToken(token: string) {
    const { data, error } = await useUserApi().validateToken(token)
    // トークン検証APIからエラーが返ってきた場合、authenticatedにfalseをセット
    if (!data.value || error.value) {
      console.error(error.value)
      authenticated = false
    // トークンが有効であれば、authenticatedにtrueをセット
    } else {
      authenticated = true
    }
  }

  // トークン検証の結果、authenticatedフラグにfalseがセットされた場合、'/signin'にリダイレクト
  await validateToken(token)
  if (authenticated==false) {
    return navigateTo('/signin')
  }
})
