from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for dev only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

names = ["BamBam", "Ball", "Guide"]

@app.get("/names")
def read_api():
    return {'names': names}

