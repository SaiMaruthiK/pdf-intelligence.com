from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from extract_outline import extract_outline

app = FastAPI()

# Allow connections from browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as f:
        shutil.copyfileobj(file.file, f)
    try:
        result = extract_outline(temp_filename)
    finally:
        os.remove(temp_filename)
    return result
