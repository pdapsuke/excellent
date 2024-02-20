<template>
  <v-dialog v-model="dialog" persistent max-width="400px">
    <v-card>
      <v-card-title class="my-3">
        <span class="headline">{{props.title}}</span>
      </v-card-title>
      <v-form ref="postForm" lazy-validation class="mx-3">
        <v-select
          v-model="selectedBallSpeeds"
          variant="outlined"
          label="球速"
          :items="parameters.ball_speeds"
          :rules="[rules.arrayElementRequired]"
          item-title="speed"
          item-value="id"
          clearable
          multiple
          class="mb-3"
        ></v-select>
        <v-select
          v-model="selectedBreakingBalls"
          variant="outlined"
          label="球種"
          :items="parameters.breaking_balls"
          :rules="[rules.arrayElementRequired]"
          item-title="name"
          item-value="id"
          clearable
          multiple
          class="mb-3"
        ></v-select>
        <v-select
          v-model="selectedBatterBox"
          variant="outlined"
          label="打席"
          :items="[{id: 1, value: '左'}, {id: 2, value: '右'}, {id: 3, value: '両'}]"
          item-title="value"
          item-value="value"
          :rules="[rules.required]"
          clearable
          class="mb-3"
        ></v-select>
      </v-form>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn :color="props.colorCancel" @click="confirm(false)">{{cancelBtn}}</v-btn>
        <v-btn :color="props.colorConfirm" @click="confirm(true)">{{confirmBtn}}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
interface Props {
  title: string
  message: string
  cancelBtn: string
  confirmBtn: string
  colorCancel: "primary" | "secondary" | "error" | "warning" | "info" | "success"
  colorConfirm: "primary" | "secondary" | "error" | "warning" | "info" | "success"
}

const postForm = ref<any>(null) // 入力欄のref
const rules = useRules() // バリデーションルール

// ダイアログの表示・非表示のコントロール
const dialog = ref<boolean>(false)

// コンポーネントの呼び出し元から受け取るパラメータ
let parameters: Parameters = {}

// 選択済の球速、球種を格納する変数
const selectedBatterBox = ref<string>()
const selectedBallSpeeds = ref<number[]>()
const selectedBreakingBalls = ref<number[]>()

// 親コンポーネントがダイアログを開くときに呼び出す関数
function open(v: any = {}) {
  dialog.value = true // ダイアログを表示
  parameters = v
}

async function confirm(confirm: boolean) {
  // confirmがtrueの場合、フォームバリデーション
  if (confirm==true) {
    const { valid: postFormValid } = await postForm.value.validate()
    if (!postFormValid) {
      return
    }
  }
  dialog.value = false
  emit(
    "confirm",
    confirm,
    selectedBatterBox.value,
    selectedBallSpeeds.value,
    selectedBreakingBalls.value,
  )
    selectedBatterBox.value = undefined
    selectedBallSpeeds.value = undefined
    selectedBreakingBalls.value = undefined
}

// propsを定義
const props = withDefaults(defineProps<Props>(), {
  title: "",
  cancelBtn: "Cancel",
  confirmBtn: "OK",
  colorCancel: "primary",
  colorConfirm: "error",
})

// イベントを定義
const emit = defineEmits<{
  confirm: [
    ok: boolean,
    selectedBatterBox: number[],
    selectedBallSpeeds: number[],
    selectedBreakingBalls: number[],
  ]
}>()

// 外部に公開
defineExpose({
  open: open,
})

</script>
