export default defineNuxtRouteMiddleware((to, from) => {
  // 遷移前のパスと遷移後のパスが等しい、かつ
  // クエリパラメータがない場合(更新ボタンを押下時は遷移前後のパスが等しくなるため)、ページへの直接アクセスとみなす
  if (from.path == to.path && Object.keys(to.query).length === 0) {
    return navigateTo('/signin')
  }
})
