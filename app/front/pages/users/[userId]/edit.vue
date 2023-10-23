<template>
  <div>
    <Alert ref="alert" />
    <div>
      <div class="text-h4">Edit user</div>
    </div>
    <v-sheet class="mx-auto">
      <v-form ref="form" @submit.prevent="submit">
        <v-text-field
          v-model="user!.username"
          variant="outlined"
          label="username"
          :rules="[rules.required, rules.maxLength(100)]"
          dense
          readonly
        ></v-text-field>
        <v-text-field
          v-model="password"
          variant="outlined"
          label="password"
          :rules="[rules.required, rules.minLength(8), rules.maxLength(100)]"
          type="password"
          clearable
          dense
        ></v-text-field>
        <v-text-field
          v-model="age"
          variant="outlined"
          label="age"
          :rules="[rules.required, rules.max(150)]"
          type="number"
          clearable
          dense
        ></v-text-field>
        <v-select
          v-model="role_ids"
          variant="outlined"
          label="roles"
          :items="[{id: 1, name: 'SYSTEM_ADMIN'}, {id: 2, name: 'LOCATION_ADMIN'}, {id: 3, name: 'LOCATION_OPERATOR'}]"
          item-title="name"
          item-value="id"
          clearable
          multiple
          dense
        ></v-select>
        <v-btn
          color="primary"
          type="submit"
        >更新</v-btn>
      </v-form>
    </v-sheet>
  </div>
</template>

<script setup lang="ts">

// ミドルウェアによるログインチェック
definePageMeta({ middleware: ["auth"] })

// パスパラメータを取得
const {userId} = useRoute().params

const username = ref<string>("")
const password = ref<string>("")
const age = ref<number>(30)
const role_ids = ref<number[]>([])
const alert = ref<any>(null)  // Alertコンポーネントのref
const form = ref<any>(null)  // v-formコンポーネントのref
const rules = useRules()  // バリデーション関数クラス

// ユーザー取得
const { data: user, pending, error: getUserError, refresh } = await useUserApi().get(userId)
if (user.value) {
  age.value = user.value.age
  role_ids.value = user.value.roles.map((role: any) => role.id)
}

onMounted(() => {
  // ユーザー取得に失敗したらアラートを表示
  if (getUserError.value instanceof Error) {
    alert.value.error(getUserError.value)
    console.error(getUserError.value)
    return
  }
})

// ユーザー更新
async function submit() {
  // バリデーション
  const {valid, errors} = await form.value.validate()
  if (!valid) {
    return
  }
  // ユーザー作成APIを呼び出す
  const { data, pending, error, refresh } = await useUserApi().update(user.value!.id, {
    username: username.value,
    password: password.value,
    age: age.value,
    role_ids: role_ids.value,
  })
  // エラー：アラートを表示
  if (error.value instanceof Error) {
    alert.value.error(error.value)
    console.error(error.value)
    return
  }
  // 成功：ユーザー一覧画面に遷移
  useRouter().push("/users/")
}
</script>
