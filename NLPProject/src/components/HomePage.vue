<script setup>
import { ref, onMounted } from 'vue';

const names = ref([]); // Array to store names from API

onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/names'); // Fetch from FastAPI
    const data = await response.json();
    names.value = data.names; // Store names in reactive variable
  } catch (error) {
    console.error("Error fetching names:", error);
  }
});
</script>

<template>
  <div>
    <h1>Welcome To Our Project:</h1>
    <ul>
      <li v-for="(name, index) in names" :key="index">{{ name }}</li>
    </ul>
  </div>
</template>
