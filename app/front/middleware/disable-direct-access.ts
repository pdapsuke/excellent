// この書き方でURL直アクセスを制限できる理由はあんま分かってない
export default defineNuxtRouteMiddleware((from, $route) => {
    if (from.name === $route.name) {
      return navigateTo('/signin')
    }
})
