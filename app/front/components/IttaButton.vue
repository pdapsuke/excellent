<template>
  <div>
    <v-btn
      :class="{ 'active-btn': props.itta === true, 'inactive-btn': props.itta === false }"
      :variant="props.itta === true ? 'outlined': ''"
			:color="props.itta === false ? 'white': 'red'"
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
