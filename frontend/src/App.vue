<template>
  <div id="app">
    <router-view />  <!-- This will display either LoginPage, TaskPage or Register based on the route -->
  </div>
</template>

<script>
import {defineComponent} from 'vue'; 

export default defineComponent({
  name: 'App',
});
</script>

<style>
</style>
