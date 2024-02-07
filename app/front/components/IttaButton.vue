<template>
  <div>
    <v-btn
      :class="{ 'active-btn': props.itta === 'yes', 'inactive-btn': props.itta === 'no' }"
      :variant="props.itta === 'no' ? 'outlined': ''"
			:color="props.itta === 'no' ? 'white': 'red'"
      rounded
    >
			行った！
    </v-btn>
  </div>
</template>

<script setup lang="ts">
interface Props {
	itta: string
}

const props = defineProps<Props>()

</script>

<style scoped>
.active-btn {
  background-color: green;
	font-weight: bold;
}

.inactive-btn {
  background-color: lightgray;
}
</style>
