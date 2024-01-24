<template>
  <v-dialog v-model="dialog" persistent max-width="400px">
    <v-card>
      <v-card-title>
        <span class="headline">{{props.title}}</span>
      </v-card-title>
      <v-select
        v-model="selectedBallSpeeds"
        variant="outlined"
        label="球速"
        :items="parameters.ball_speeds"
        item-title="speed"
        item-value="id"
        clearable
        multiple
        dense
      ></v-select>
      <v-select
        v-model="selectedBreakingBalls"
        variant="outlined"
        label="球種"
        :items="parameters.breaking_balls"
        item-title="name"
        item-value="id"
        clearable
        multiple
        dense
      ></v-select>
      <v-select
        v-model="selectedBatterBox"
        variant="outlined"
        label="打席"
        :items="[{id: 1, value: '左'}, {id: 2, value: '右'}, {id: 3, value: '両'}]"
        item-title="value"
        item-value="value"
        clearable
        dense
      ></v-select>
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

// ダイアログの表示・非表示のコントロール
const dialog = ref<boolean>(false)

// コンポーネントの呼び出し元から受け取るパラメータ
let parameters: Parameters = {}

// 選択済の球速、球種を格納する変数
let selectedBatterBox = ref<string>()
let selectedBallSpeeds = ref<number[]>()
let selectedBreakingBalls = ref<number[]>()

// 親コンポーネントがダイアログを開くときに呼び出す関数
function open(v: any = {}) {
  dialog.value = true // ダイアログを表示
  parameters = v

  // パラメータから対象マシンで既に設定されている球速、球種を受け取る
  selectedBatterBox.value = parameters.batter_box
  selectedBallSpeeds.value = parameters.selected_ball_speeds
  selectedBreakingBalls.value = parameters.selected_breaking_balls
}

function confirm(confirm: boolean) {
  dialog.value = false
  emit(
    "confirm",
    confirm,
    parameters,
    selectedBatterBox.value,
    selectedBallSpeeds.value,
    selectedBreakingBalls.value,
  )
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
    parameters: any,
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
