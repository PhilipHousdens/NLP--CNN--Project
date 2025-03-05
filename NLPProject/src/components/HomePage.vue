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
    const response = await fetch('http://127.0.0.1:8000/summarize/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ article: inputText.value }),
    });

    // Add a timeout check if the request is taking too long
    const timeout = 10000;  // Timeout after 10 seconds
    const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject('Request timeout'), timeout)
    );
    
    const data = await Promise.race([response.json(), timeoutPromise]);
    summary.value = data.summary;
  } catch (error) {
    console.error("Error fetching summary:", error);
    summary.value = `Error: ${error}`;  // Show error message to the user
  }
});

// Summarize the input text
const summarizeText = () => {
  if (inputText.value.trim() === '') {
    alert('Please enter some text to summarize.');
    return;
  }
  // Simple summarization: take first 100 characters
  summary.value = inputText.value.slice(0, 100) + '...';
};

</script>

<template>
  <div class="max-w-4xl w-full p-8 bg-white shadow-lg rounded-lg">

    <!-- Text Summarization Section -->
    <h1 class="text-4xl font-bold text-brown-900 mb-8 text-center">News Text Summarization</h1>
    
    <textarea 
      v-model="inputText"
      class="w-full p-4 text-lg border border-brown-300 rounded-lg resize-y shadow-sm mb-6 focus:outline-none focus:ring-2 focus:ring-brown-500"
      placeholder="Paste your news text here..." 
      rows="10"
    ></textarea>

    <button 
      @click="summarizeText"
      class="bg-brown-600 text-white px-6 py-2 rounded-lg font-semibold shadow-md hover:bg-brown-700 focus:outline-none focus:ring-2 focus:ring-brown-300 w-full"
    >
      Summarize
    </button>

    <!-- Display Summary -->
    <div v-if="summary" class="mt-6 text-lg text-brown-800">
      <strong class="font-semibold">Summary:</strong>
      <p>{{ summary }}</p>
    </div>

    <!-- Display Names from the API -->
    <div v-if="names.length" class="mt-8 text-lg text-brown-800">
      <h2 class="text-2xl font-semibold mb-4">Names from Backend</h2>
      <ul class="list-disc pl-6">
        <li v-for="(name, index) in names" :key="index" class="mb-2 text-brown-600">{{ name }}</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
/* Brown color palette adjustments */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

body {
  font-family: 'Roboto', sans-serif;
  background-color: #effd5f; /* light beige background */
}

.bg-brown-900 {
  background-color: #3E2723; /* Dark brown */
}

.bg-brown-600 {
  background-color: #6D4C41; /* Medium brown */
}

.bg-brown-500 {
  background-color: #8D6E63; /* Lighter brown */
}

.text-brown-900 {
  color: #3E2723; /* Dark brown text */
}

.text-brown-800 {
  color: #4E342E; /* Soft brown text */
}

.text-brown-600 {
  color: #6D4C41; /* Medium brown text */
}

</style>
