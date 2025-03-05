from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import torch
import json
from pydantic import BaseModel
from models.LSTMModel import LSTMSeq2Seq
from transformers import AutoTokenizer
import os
import asyncio

print(os.getcwd())  # Check current working directory

app = FastAPI()

# CORS middleware should be added before any route definitions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development, you can restrict this later)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load config
with open("models/config.json", "r") as f:
    config = json.load(f)

# Define a request model for text input
class TextRequest(BaseModel):
    text: str  # The text input field that will be required

# Load vocab and model
VOCAB_SIZE = 50000  # Define your vocab size
EMBED_SIZE = 100
HIDDEN_SIZE = 216

# Load vocab (ensure vocab and rev_vocab are loaded properly)
# Assuming the vocab is a PyTorch dictionary stored as vocab.pth
vocab = torch.load("models/vocab.pth", map_location=torch.device('cpu'))

# Ensure <UNK>, <SOS>, and <EOS> are added with the correct indices
if "<UNK>" not in vocab:
    vocab["<UNK>"] = 1
if "<SOS>" not in vocab:
    vocab["<SOS>"] = 2
if "<EOS>" not in vocab:
    vocab["<EOS>"] = 3

rev_vocab = {v: k for k, v in vocab.items()}  # Reverse vocab

# Check if <UNK>, <SOS>, and <EOS> exist
print(f"UNK index: {vocab.get('<UNK>', 'Not found')}")
print(f"SOS index: {vocab.get('<SOS>', 'Not found')}")
print(f"EOS index: {vocab.get('<EOS>', 'Not found')}")

# Load embedding matrix
embedding_matrix = torch.load("models/embedding_matrix.pth", map_location=torch.device('cpu'))  # Change this path to where you saved it
model = LSTMSeq2Seq(VOCAB_SIZE, EMBED_SIZE, HIDDEN_SIZE, embedding_matrix).to(device)
model.load_state_dict(torch.load("models/model.pth", map_location=torch.device('cpu')), strict=False)  # Load trained weights
model.eval()

# Load tokenizer (if you're using one, this might be useful for preprocessing)
tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')

# API endpoint to summarize text
@app.post("/summarize/")
async def summarize_text(request: TextRequest):
    try:
        text = request.text  # Get the text from the request body
        # Run model inference synchronously (direct call without asyncio.to_thread)
        summary = run_model_inference(text)
        return {"summary": summary}
    except Exception as e:
        print(f"Error during inference: {e}")
        return {"error": "There was an issue processing your request"}
def run_model_inference(text):
    # Convert text to tensor (ensure vocab contains <SOS>, <EOS>, etc.)
    unk_index = vocab.get("<UNK>", 1)
    text_indices = [vocab.get(word, vocab.get("<UNK>", 1)) for word in text.split()]
    text_tensor = torch.tensor(text_indices, dtype=torch.long).unsqueeze(0).to(device)

    # Run the model's encoder
    embedded_text = model.embedding(text_tensor)
    _, (hidden, cell) = model.encoder(embedded_text)

    generated_seq = [vocab["<SOS>"]]  # Start with <SOS>

    # Generate the sequence (using the decoder)
    for _ in range(100):  # Adjust max length
        last_word = generated_seq[-1]
        if last_word == vocab["<EOS>"]:
            break

        last_word_tensor = torch.tensor([last_word], dtype=torch.long).to(device)
        embedded_input = model.embedding(last_word_tensor).unsqueeze(1)

        output, (hidden, cell) = model.decoder(embedded_input, (hidden, cell))
        output_probs = torch.softmax(model.fc(output.squeeze(1)), dim=-1)

        next_word_idx = torch.argmax(output_probs, dim=-1).item()

        generated_seq.append(next_word_idx)
        if next_word_idx == vocab["<EOS>"]:
            break

    # Convert generated sequence indices to words using rev_vocab
    summary = " ".join([rev_vocab.get(idx, "<UNK>") for idx in generated_seq if idx not in {vocab["<SOS>"], vocab["<EOS>"], vocab["<PAD>"], vocab["<UNK>"]}])
    
    print(f"Generated summary: {summary}")
    return summary

# Store the latest summary (to be accessed later via /get-summary)
latest_summary = None  # Initialize it as None

@app.get("/get-summary")
async def get_summary():
    if latest_summary:
        return {"summary": latest_summary}
    else:
        return {"summary": "No summary available yet."}

@app.on_event("startup")
async def load_model():
    try:
        print("Loading model...")
        model = LSTMSeq2Seq(VOCAB_SIZE, EMBED_SIZE, HIDDEN_SIZE, embedding_matrix).to(device)
        model.load_state_dict(torch.load("models/model.pth", map_location=torch.device('cpu')), strict=False)
        model.eval()
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")


