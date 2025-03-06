from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
origins = [
    "http://localhost:5173",  # Frontend development server URL
    "http://localhost",       # If needed, allow localhost as well
    "http://127.0.0.1",      # Allow 127.0.0.1
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow only these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Load model and tokenizer
MODEL_PATH = "models/summarization_model"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH).to("cuda" if torch.cuda.is_available() else "cpu")

# Define request model
class SummarizationRequest(BaseModel):
    text: str

# Summarization endpoint
@app.post("/summarize/")
async def summarize_text(request: SummarizationRequest):
    try:
        # Tokenize input text
        inputs = tokenizer(request.text, return_tensors="pt", truncation=True, padding="max_length", max_length=512).to(model.device)

        # Generate summary
        summary_ids = model.generate(inputs["input_ids"], num_beams=4, max_length=200, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return {"summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
