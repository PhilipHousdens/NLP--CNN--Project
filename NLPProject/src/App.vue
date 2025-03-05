<script setup>
import HomePage from './components/HomePage.vue'
import newsImage from './assets/news.jpg'  // Make sure the path is correct
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-6" :style="{ backgroundImage: `url(${newsImage})`, backgroundSize: 'cover', backgroundPosition: 'center' }">
    <!-- Render the HomePage component -->
    <HomePage />
  </div>
</template>
