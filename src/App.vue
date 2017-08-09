<template>
  <div id="app">
    <img src="./assets/logo.png">
    <k-line></k-line>
  </div>
</template>

<script>
import KLine from './components/KLine'

export default {
  name: 'app',
  components: {
    KLine
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
