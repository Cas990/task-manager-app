<template>
  <div id="app">
    <router-view />  <!-- This will display either LoginPage or TaskPage based on the route -->
  </div>
</template>

<script>
import {defineComponent} from 'vue'; 

export default defineComponent({
  name: 'App',
});
</script>

<style>
/* Add any global styling here */
</style>
