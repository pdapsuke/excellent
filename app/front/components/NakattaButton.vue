<template>
  <div>
    <v-btn
      :class="{ 'active-btn': props.nakatta === true }"
      flat
			:style="{ color: props.nakatta === false ? 'gray' : 'blue' }"
    >
			なかった！
    </v-btn>
  </div>
</template>

<script setup lang="ts">
interface Props {
	nakatta: string
}

const props = defineProps<Props>()

</script>

<style scoped>
.active-btn {
	font-weight: bold;
}

</style>
