import pymupdf
import requests
import tempfile
import os
from ..logger import logger
from ..config import API_URL, APP_ID
import io


PROMPT_API_URL = API_URL
PROMPT_APP_ID = APP_ID


def extract_text_from_pdf(file_stream):
    text = ""
    try:
        pdf_doc = pymupdf.open(stream=file_stream, filetype="pdf")
        for page in pdf_doc:
            text += page.get_text()
    except Exception as e:
        logger.error(e)
        print(f"Error reading PDF: {e}")
    return text


def inspect_text_with_prompt(text):
    headers = {
        "APP-ID": PROMPT_APP_ID,
        "Content-Type": "application/json"
    }
    data = {"prompt": text}
    try:
        response = requests.post(PROMPT_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            response = response.json()
            passed = response.get('result', {}).get('prompt', {}).get('passed', False)
            if not passed:
                logger.critical({'secret found': True,
                                 'response': response})
            else:
                logger.info(response)
            return {'found_secrets': not passed}
    except Exception as e:
        print(f"Error calling Prompt API: {e}")
        return {"error": str(e)}


def inspect_pdf(file_storage, filename):
    tmp_path = None
    try:
        # Save uploaded file to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
            file_storage.save(tmp.name)
            tmp_path = tmp.name

        # Read PDF bytes
        with open(tmp_path, 'rb') as tmp_file:
            pdf_bytes = tmp_file.read()

        # Extract text
        text = extract_text_from_pdf(io.BytesIO(pdf_bytes))
        if not text.strip():
            logger.info(f"No text found in PDF: {filename}")
            return {"error": "No text found in PDF"}, 400

        # Inspect text with your custom function
        return inspect_text_with_prompt(text)

    except Exception as e:
        logger.exception("Error processing PDF")
        return {"error": f"Inspection error: {e}"}, 500

    finally:
        # Always clean up
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
