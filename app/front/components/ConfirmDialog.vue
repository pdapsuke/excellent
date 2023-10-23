<template>
  <!--  -->
  <v-dialog v-model="dialog" persistent max-width="400px">
    <v-card>
      <v-card-title>
        <span class="headline">{{props.title}}</span>
      </v-card-title>
      <v-card-text>
        {{props.message}}
      </v-card-text>
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
let parameters: any = {}

// 親コンポーネントがダイアログを開くときに呼び出す関数
function open(v: any = {}) {
  dialog.value = true // ダイアログを表示
  parameters = v
}

// ダイアログのボタンがクリックされたときに呼び出す関数
function confirm(confirm: boolean) {
  dialog.value = false // ダイアログを非表示
  // confirmイベントを発生させる
  emit("confirm", confirm, parameters)
}

// propsはdefinePropsで定義する。デフォルト値はwithDefaultsで定義する。
const props = withDefaults(defineProps<Props>(), {
  title: "",
  message: "",
  cancelBtn: "Cancel",
  confirmBtn: "OK",
  colorCancel: "primary",
  colorConfirm: "error",
})

// イベントを発生させたいときは、defineEmitsを使う。
const emit = defineEmits<{
  // confirmイベントを定義
  confirm: [ok: boolean, parameters: any], // イベントの引数を名前付きタプルで定義
}>()

// カスタムコンポーネント内の関数などを呼びたいときはdefineExposeを使って、明示的に公開する必要がある。
defineExpose({
  open: open,
})
</script>
