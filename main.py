# Import the modules for result writing and IP tracking
import result_writer
import ip_tracker
import json
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import spacy
import pytesseract
from PIL import Image
import hashlib
from datetime import datetime
import os

# Initialize FastAPI app
main = FastAPI()
main.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load the Spacy model
nlp = spacy.load("en_core_web_sm")

# Configure Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Drug-related terms
drug_terms = ["grams", "kilo", "narcotics", "powder", "pills", "cocaine", "heroin", "meth", "shipment", "delivery",
              "stash", "weed", "cannabis", "marijuana", "acid", "LSD", "crack", "opium", "syringe", "smack", "ecstasy",
              "crystal", "XTC", "molly", "blunt", "dope", "baggies", "deal", "plug", "connect", "buyer", "supplier",
              "joint", "high", "trip", "ounce", "quarter", "eighth", "dime", "cartel", "drop", "boost", "hit", "fix",
              "snort", "smoke", "pop", "inject", "overdose", "cash", "green plant", "wood", "bread"]

# Simulated blockchain ledger
blockchain = []


def log_to_blockchain(data):
    """Log data to a simulated blockchain."""
    block = {
        "block_id": hashlib.sha256(str(data).encode()).hexdigest(),
        "data": data,
        "timestamp": datetime.now().isoformat()
    }
    blockchain.append(block)
    return block


def analyze_message_content(message):
    """Analyze a message for suspicious terms."""
    doc = nlp(message)
    keywords_detected = [token.text for token in doc if token.text.lower() in drug_terms]
    if keywords_detected:
        suspicion_level = "high"
        flag_reason = "Drug-related terms detected"
    else:
        suspicion_level = "low"
        flag_reason = "No suspicious terms detected"
    return {
        "message": message,
        "keywords_detected": keywords_detected,
        "suspicion_level": suspicion_level,
        "flag_reason": flag_reason
    }


def extract_text_from_image(image_path):
    """Extract text from an image using OCR."""
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text


@main.post("/analyze_text")
def analyze_text(message: str = Form(...)):
    """Analyze text input from the web interface."""
    analysis = analyze_message_content(message)
    data = {
        "message": message,
        "analysis": analysis,
        "timestamp": datetime.now().isoformat()
    }
    block = log_to_blockchain(data)
    return {"analysis": analysis, "block": block}


@main.post("/analyze_image")
async def analyze_image(file: UploadFile = File(...)):
    """Analyze an uploaded image."""
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    extracted_text = extract_text_from_image(file_location)
    os.remove(file_location)
    analysis = analyze_message_content(extracted_text)
    data = {
        "extracted_text": extracted_text,
        "analysis": analysis,
        "timestamp": datetime.now().isoformat()
    }
    block = log_to_blockchain(data)
    return {"analysis": analysis, "block": block}


@main.get("/blockchain")
def get_blockchain():
    """Get the current blockchain ledger."""
    return {"blockchain": blockchain}
