<script setup>
import { ref } from "vue";
import axios from "axios";

const inputText = ref("");
const summary = ref("");
const loading = ref(false);

const summarizeText = async () => {
  if (!inputText.value) return;

  loading.value = true;
  summary.value = "";

  try {
    const response = await axios.post("http://localhost:8000/summarize/", {
      text: inputText.value,
    });
    summary.value = response.data.summary;
  } catch (error) {
    summary.value = "Error: " + error.response?.data?.detail || error.message;
  } finally {
    loading.value = false;
  }
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
