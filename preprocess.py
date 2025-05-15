import requests
from PIL import Image
import pytesseract
from io import BytesIO

# CAPTCHA image URL (please set accordingly)
CAPTCHA_URL = ""

# Make sure the COOKIES variable matches the cookies used in sqlmap --cookie parameter.
COOKIES = {
    "JSESSIONID": "",
}

# Whether to use a self-trained PyTorch model for OCR
USE_PYTORCH = False

# Allowed characters whitelist for Tesseract OCR
TESSEDIT_CHAR_WHITELIST = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

if USE_PYTORCH:
    try:
        import predict  # Import your custom PyTorch OCR module
        print("[INFO] Using PyTorch model for OCR")
    except ImportError:
        raise ImportError("[ERROR] Cannot import predict module, please verify it exists and is importable")

# Uncomment and modify the line below if you need to specify the Tesseract executable path on Windows
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def fetch_captcha_image() -> Image.Image:
    """
    Fetch the CAPTCHA image from CAPTCHA_URL and return a PIL Image object.
    Raises an exception if the request fails.
    """
    response = requests.get(CAPTCHA_URL, cookies=COOKIES)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        raise Exception(f"Failed to fetch CAPTCHA image, status code: {response.status_code}")


def recognize_captcha(image: Image.Image) -> str:
    """
    Perform OCR on the given PIL Image.
    Uses PyTorch model if enabled; otherwise uses Tesseract OCR.
    Returns the recognized text string.
    """
    if USE_PYTORCH:
        return predict.recognize(image)
    else:
        gray_image = image.convert("L")
        text = pytesseract.image_to_string(
            gray_image,
            config=f"--psm 8 -c tessedit_char_whitelist={TESSEDIT_CHAR_WHITELIST}",
        )
        return text.strip()


def preprocess(req):
    """
    Entry point for sqlmap --preprocess.
    Fetches a new CAPTCHA image, performs OCR, then appends the recognized text
    to the POST data under the 'captcha' field.
    If an error occurs, logs the error and uses a default value '00000'.
    """

    result = '00000'
    try:
        image = fetch_captcha_image()
        result = recognize_captcha(image)
        image.save(f'{result}.png')  # Save image for debugging
        print(f"OCR recognition result: {result}")
    except Exception as e:
        print(f"Error： {e}")

    if req.data:
        # Append recognized captcha to POST data
        req.data += b'&captcha=' + result.encode('utf-8')
        print(f'--DATA : {req.data}')
    return req
