# Initialize the reader once (will download models on first run if missing)
# Cache it so we don't reload it every time
reader = None

def get_reader():
    global reader
    try:
        import easyocr
        if reader is None:
            reader = easyocr.Reader(['en'], gpu=False) # Use CPU for general compatibility
        return reader
    except ImportError:
        return None

def extract_text_from_image(image_bytes):
    """
    Extracts text from an uploaded image using EasyOCR.
    image_bytes: Bytes of the uploaded image.
    """
    try:
        reader_instance = get_reader()
        if reader_instance is None:
            return ""
            
        # EasyOCR can read from bytes directly
        result = reader_instance.readtext(image_bytes, detail=0)
        text = " ".join(result)
        return text
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""
        
def verify_claim_with_ocr(extracted_text, claim_amount, patient_id):
    """
    Basic verification logic comparing OCR text to claim details.
    """
    text_lower = extracted_text.lower()
    
    # Very rudimentary check: see if the claim amount exists in the text
    amount_str = str(int(claim_amount))
    amount_found = amount_str in text_lower
    
    # See if patient ID or some numeric part exists
    # If patient_id is PAT1234, check for 1234
    patient_num = "".join(filter(str.isdigit, patient_id))
    patient_found = False
    if patient_num and patient_num in text_lower:
        patient_found = True
        
    return {
        "amount_match": amount_found,
        "patient_match": patient_found,
        "extracted_text": extracted_text
    }
