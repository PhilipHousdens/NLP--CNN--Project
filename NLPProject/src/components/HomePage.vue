<script setup>
import { ref } from 'vue';

const inputText = ref(''); // Variable to store user input
const summary = ref(''); // Variable to store the summarized text

// Function to handle the form submission
const getSummary = async () => {
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
};

</script>

<template>
  <div>
    <h1>Text Summarization</h1>
    
    <!-- Form to accept input text -->
    <textarea 
      v-model="inputText" 
      rows="6" 
      cols="50" 
      placeholder="Enter the text to summarize"
    ></textarea>

    <!-- Button to trigger summarization -->
    <button @click="getSummary">Summarize</button>

    <!-- Display the summarized text -->
    <h3>Summary:</h3>
    <p>{{ summary }}</p>
  </div>
</template>

<style scoped>
textarea {
  width: 100%;
  padding: 10px;
  font-size: 14px;
}

button {
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  margin-top: 10px;
}

button:hover {
  background-color: #45a049;
}

h3 {
  margin-top: 20px;
}
</style>
