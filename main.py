from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import spacy
import pytesseract
import os
from PIL import Image
import hashlib
from datetime import datetime

# Import the modules for result writing and IP tracking
import result_writer
import ip_tracker
import json

def save_blockchain_to_file():
    with open("blockchain.json", "w") as f:
        json.dump(blockchain, f, indent=4)

main = FastAPI()

nlp = spacy.load("en_core_web_sm")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

nlp = spacy.load("en_core_web_sm")

# drug-related terms 
drug_terms = ["grams","kilo","narcotics","powder","pills","cocaine","heroin","meth","shipment","delivery","stash","weed","cannabis",
              "marijuana","acid","LSD", "crack","opium","syringe","smack","ecstasy","crystal","XTC","molly","blunt","dope","baggies",
              "deal","plug","connect","buyer","supplier","joint","high","trip","ounce","quarter","eighth","dime","cartel","drop",
              "boost","hit","fix","snort","smoke","pop","inject","overdose","cash","green plant","wood","bread"]

# Simulated blockchain ledger
blockchain = []
@main.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application! Use /analyze_message or /analyze_image to interact with the API."}

@main.post("/analyze_message")
def analyze_message(message: str):
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
    
def log_to_blockchain(data):
    block = {
        "block_id": hashlib.sha256(str(data).encode()).hexdigest(),
        "data": data,
        "timestamp": datetime.now().isoformat()
    }
    blockchain.append(block)
    save_blockchain_to_file()
    return block

def load_blockchain_from_file():
    global blockchain
    try:
        with open("blockchain.json", "r") as f:
            blockchain = json.load(f)
    except FileNotFoundError:
        blockchain = []
load_blockchain_from_file()


def analyze_message_content(message):
    """detect suspicious terms"""
    doc = nlp(message)
    keywords_detected = [token.text for token in doc if token.text.lower() in drug_terms]
    if keywords_detected:
        suspicion_level = "high"
        flag_reason = "Drug-related terms detected"
        print(f"ALERT: Suspicious message detected! - {keywords_detected}")
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
    """Extract text using OCR"""
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text

def process_message(message=None, image_path=None, sender_ip=None, receiver_ip=None):
    """Process both text and images to detect suspicious content"""
    if message:
        analysis = analyze_message_content(message)
        print(f"Processed Message: {message}")
    elif image_path:
        extracted_text = extract_text_from_image(image_path)
        analysis = analyze_message_content(extracted_text)
        print(f"Extracted and Processed Text from Image: {extracted_text}")
    else:
        raise ValueError("Either a message or image path must be provided")

    
    data = {
        "sender_ip": sender_ip,
        "receiver_ip": receiver_ip,
        "analysis": analysis,
        "timestamp": datetime.now().isoformat()
    }
    
   
    block = log_to_blockchain(data)
    print(f"Logged to blockchain: {block}")

    # Write results to result.txt
    result_writer.write_to_file(message if message else extracted_text, sender_ip, receiver_ip, block)

    # Track and show IP location on map
    ip_tracker.track_ip_location(sender_ip, receiver_ip)

def process_all_images_in_folder(folder_path, sender_ip, receiver_ip):
    """Process all image files in a specified folder"""
    for filename in os.listdir(folder_path):
        if filename.endswith((".png", ".jpg", ".jpeg")): 
            image_path = os.path.join(folder_path, filename)
            print(f"\nProcessing image: {image_path}")
            process_message(image_path=image_path, sender_ip=sender_ip, receiver_ip=receiver_ip)

# Example usage:
# Text message processing
message_text = "Need 100 grams for shipment tomorrow"
process_message(message=message_text, sender_ip="192.168.1.25", receiver_ip="203.0.113.78")

message="Can you bring me 50 grams of powder by Friday? Need it for the client."
process_message(message=message, sender_ip="192.168.1.25", receiver_ip="203.0.113.78")

message1="The shipment is ready, I'll drop it at the usual spot tomorrow. Don't forget the cash."
process_message(message=message1, sender_ip="192.168.1.25", receiver_ip="203.0.113.78")

message2="Hey, can you pick up some groceries on your way home? We're out of milk ."
process_message(message=message2, sender_ip="192.168.1.25", receiver_ip="203.0.113.78")

message3="Let's meet at the coffee shop at 5 PM to discuss the project details. See you there!"
process_message(message=message3, sender_ip="192.168.1.25", receiver_ip="203.0.113.78")

message4="The package you ordered has been shipped and will arrive by the end of the week."
process_message(message=message4, sender_ip="192.168.1.25", receiver_ip="203.0.113.78")

# Process all images in the specified folder
process_all_images_in_folder("C:\\Users\\saifu\\Downloads\\InsightOps1", sender_ip="192.168.1.25",receiver_ip="203.0.114.79")

# output
print("\nBlockchain Ledger:")
for block in blockchain:
    print(block)
