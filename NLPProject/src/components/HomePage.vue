<script setup>
import { ref, onMounted } from 'vue';

// Array to store names from the API
const names = ref([]);

// Variables for text summarization
const inputText = ref('');
const summary = ref('');

// Fetch names from FastAPI on mount
onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/names'); // Fetch from FastAPI
    const data = await response.json();
    names.value = data.names; // Store names in reactive variable
  } catch (error) {
    console.error("Error fetching names:", error);
  }
});

// Summarize the input text (this is just an example summarization)
const summarizeText = () => {
  if (inputText.value.trim() === '') {
    alert('Please enter some text to summarize.');
    return;
  }
  // Example of a simple summarization (taking the first 100 characters)
  summary.value = inputText.value.slice(0, 100) + '...';
};
</script>

<template>
  <div class="max-w-4xl mx-auto p-6">
    <h1 class="text-3xl font-semibold text-left mb-6">Text Summarization</h1>

    <!-- Input Box for News Text -->
    <textarea 
      v-model="inputText" 
      class="w-full p-4 text-lg border border-gray-300 rounded-lg resize-y mb-6" 
      placeholder="Paste your news text here..." 
      rows="10"
    ></textarea>

    <!-- Summarize Button -->
    <button 
      @click="summarizeText" 
      class="bg-green-500 text-white px-6 py-2 text-lg font-semibold rounded-lg hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400"
    >
      Summarize
    </button>

    <!-- Display Summarized Text -->
    <div v-if="summary" class="mt-6 text-lg">
      <strong class="font-semibold">Summary:</strong>
      <p>{{ summary }}</p>
    </div>

    <!-- Display Names from the API -->
    <h2 class="mt-8 text-2xl font-semibold">Names from Backend</h2>
    <ul class="mt-4">
      <li v-for="(name, index) in names" :key="index">{{ name }}</li>
    </ul>
  </div>
</template>

<style scoped>
/* Optional scoped styles for the homepage */
</style>
