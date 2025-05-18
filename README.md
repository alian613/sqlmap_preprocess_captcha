# OCR CAPTCHA Preprocessing for SQLmap

Bypass CAPTCHA challenges automatically during `sqlmap` injection testing.  
This tool automatically solve CAPTCHA challenges during a `sqlmap` injection test by fetching the CAPTCHA image, performing OCR (either via Tesseract or a PyTorch model), and appending the result to your POST data.

📖 [中文說明文件](README_zh.md)

## Features

- ✅ Automatically **bypasses CAPTCHA** protections for automated SQLmap testing
- ✅ Supports basic OCR using Tesseract, for example:  
  ![Tesseract example](docs/tesseract_captcha.png)
- ✅ Supports advanced OCR using your own PyTorch model (`predict.py`), for example:  
  ![PyTorch example1](docs/pytorch_captcha1.png)  
  ![PyTorch example2](docs/pytorch_captcha2.png)
  > OCR CAPTCHA model training tool available in my other project:
  🔗 [https://github.com/alian613/ocr_captcha](https://github.com/alian613/ocr_captcha)
- ✅ Compatible with `sqlmap`'s `--preprocess` option


---


## 0x00. Requirements

### 1. Python3.7+

### 2. [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
Install on Ubuntu / Kali:
```bash
apt update
apt install tesseract-ocr
```

### 3. Install required Python packages:

```bash
pip install -r requirements.txt
````

If you're using Python 3.11+
It's recommended to use a virtual environment:
```bash
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python /usr/share/sqlmap/sqlmap.py -u ... --dbs
```

Before running the script, install the necessary Python packages:

### (Optional) PyTorch OCR model
> Skip this step if you don't use a custom model.
- Set `USE_PYTORCH = True` in `preprocess_captcha.py`
- Make sure you have a `predict.py` file in the same directory.
- Ensure a file `predict.py` exists with the following function:
```python
def recognize(image: Image.Image) -> str:
    ...
```
Sample code can be found here:
[https://github.com/alian613/ocr_captcha/blob/main/predict.py](https://github.com/alian613/ocr_captcha/blob/main/predict.py)


---


## 0x01. Configuration

Edit the following variables in `preprocess_captcha.py` before using:

```python
CAPTCHA_URL = "https://example.com/captcha"  # Full URL to fetch the CAPTCHA image 
USE_PYTORCH = False  # True: use custom PyTorch model, False: use Tesseract OCR  
COOKIES = {
    "JSESSIONID": "your-session-id-here",  # Must match SQLmap's --cookie value  
}
```


---


## 0x02. SQLmap Usage

Example command to launch sqlmap with CAPTCHA preprocessing:
```bash
sqlmap -u https://target.site/form \
  --data="username=*&action=*" \
  --cookie="JSESSIONID=your-session-id" \
  --preprocess=preprocess_captcha.py \
  -v 6
```
- `--data`: string should reflect the actual POST structure of the target site.
- `--cookie`: Should match the cookie in `preprocess_captcha.py`
- `-v 6`: lets you view full HTTP traffic to debug OCR CAPTCHA behavior.  

![Example](docs/process.png)

SQLmap will call your preprocess() function before each request. e.g.
`username=testuser&action=submit&captcha=1A2BC`


---


## 0x03. Process Overview
When SQLmap prepares a request, it will automatically:  

1. Fetch the CAPTCHA image from the configured URL
2. Use OCR to recognize the text in the image
3. Inject the result into the POST data as captcha=RECOGNIZED_TEXT  
Example: username=test&action=submit&captcha=1A2BC


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

