<template>
  <div>
    <p>Health check endpoint</p>
  </div>
</template>

<script setup lang="ts">
const event = useRequestEvent()

if (event) {
  const { data } = await useApi().get<any>("backendHealthCheck", "/healthcheck")
  if (data.value.status == 'OK') {
    setResponseStatus(event, 200, 'OK')
  } else {
    setResponseStatus(event, 500, 'InternalServerError')
  }
}

</script>