<template>
  <div class="home">
    <h1>GStore</h1>
    <HelloWorld msg="Welcome to GStore"/>
  </div>
</template>

<script>
import HelloWorld from '@/components/HelloWorld.vue'// @ is an alias to /src

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  }
}
</script>
