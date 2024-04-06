<template>
  <div>
    <v-btn
      :class="{ 'active-btn': props.atta === true }"
      flat
			:style="{ color: props.atta === false ? 'gray' : 'red' }"
    >
			あった！
    </v-btn>
  </div>
</template>

<script setup lang="ts">
interface Props {
	atta: string
}

const props = defineProps<Props>()

</script>

<style scoped>
.active-btn {
	font-weight: bold;
}

</style>
