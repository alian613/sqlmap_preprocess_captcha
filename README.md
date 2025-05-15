# OCR CAPTCHA Preprocessing for SQLmap

Bypass CAPTCHA challenges automatically during `sqlmap` injection testing.  
This script helps automatically solve CAPTCHA challenges during a `sqlmap` injection test by fetching the CAPTCHA image, performing OCR (either via Tesseract or a PyTorch model), and appending the result to your POST data.

📖 [中文說明文件](README_zh.md)

## Features

- ✅ Automatically **bypasses CAPTCHA** protections for automated sqlmap testing
- ✅ Supports basic OCR using Tesseract
- ✅ Supports advanced OCR using your own PyTorch model (`predict.py`)
  > OCR CAPTCHA model training tool available in my other project:
  🔗 [https://github.com/alian613/ocr_captcha](https://github.com/alian613/ocr_captcha)
- ✅ Compatible with `sqlmap`'s `--preprocess` option

---

## Requirements

Before running the script, install the necessary Python packages:

```bash
pip install -r requirements.txt
````

- Python 3.7+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- If using PyTorch:
    - A `predict.py` script that implements `recognize(image: Image.Image) -> str`


---

## Configuration

Edit the following variables in `preprocess_captcha.py` before using:

```python
CAPTCHA_URL = "https://example.com/captcha"  # The full URL to the CAPTCHA image
USE_PYTORCH = False  # Set to True to use your custom PyTorch model
COOKIES = {
    "JSESSIONID": "your-session-id-here",  # Must match sqlmap --cookie parameter
}
```

### PyTorch Model

If USE_PYTORCH = True, make sure you have a predict.py file in the same directory.  
It must expose a function:

```python
def recognize(image: Image.Image) -> str:
    ...
```

Sample code can be found here:
[https://github.com/alian613/ocr_captcha/blob/main/predict.py](https://github.com/alian613/ocr_captcha/blob/main/predict.py)


---


## SQLmap Usage

Example command to launch sqlmap with CAPTCHA preprocessing:
```bash
sqlmap -u https://target.site/form \
  --data="username=*&action=*" \
  --cookie="JSESSIONID=your-session-id" \
  --preprocess=preprocess_captcha.py \
  -v 6
```
The `--data` string should reflect the actual POST structure of the target site.  
`-v 6` lets you view full HTTP traffic to debug OCR CAPTCHA behavior.  

sqlmap will call your preprocess() function before each request. e.g.
`username=testuser&action=submit&captcha=1A2BC`


---

## Support My Open Source Project

If you appreciate my work, consider ⭐ starring this repository or buying me a coffee to support development.  
Your support means a lot to me — thank you!  

*** [Ko-fi Support](https://ko-fi.com/alian613) ***

如果你覺得這個專案對你有幫助，歡迎給個 ⭐，也歡迎請我喝杯咖啡，非常感謝 ~


---


## 📄 License

This project is licensed under the MIT License.

---

## Disclaimer

This script is intended for educational and ethical penetration testing purposes only.  
Do **not** use it against systems you do not have explicit permission to test.  

本程式僅供教育用途及合法授權的滲透測試使用，  
旨在促進資安環境的改善與提升安全性，  
請勿用於未經授權的系統或任何非法行為。

