# SQLmap OCR CAPTCHA 工具
 
使用 Tesseract 或自訓練的 PyTorch 模型進行 OCR CAPTCHA 驗證碼圖片，並自動將辨識結果加到 POST 資料中。

📖 [English Documentation](README.md)

## 功能

- ✅ **繞過 CAPTCHA**，方便 SQLmap 自動化測試
- ✅ 支援基本 OCR (使用 Tesseract)
- ✅ 支援進階 OCR (使用自訂 PyTorch 模型 `predict.py`)
  > OCR CAPTCHA 模型訓練工具，可以參考我另一個專案：  
  🔗 [https://github.com/alian613/ocr_captcha](https://github.com/alian613/ocr_captcha)
- ✅ 支援 SQLmap 的 `--preprocess` 選項

---

## 環境需求

請先安裝必要的 Python 套件：

```bash
pip install -r requirements.txt
```

- Python 3.7+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- 若使用 PyTorch 模型：
 > 需有一個 `predict.py` 檔案，內含 recognize(image: Image.Image) -> str 函式


---

## 配置說明

在 preprocess_captcha.py 內修改以下變數：

```python
CAPTCHA_URL = "https://example.com/captcha"  # CAPTCHA 圖片完整 URL  
USE_PYTORCH = False  # 設為 True 則使用自訂 PyTorch 模型  
COOKIES = {
"JSESSIONID": "your-session-id-here",  # 請與 sqlmap --cookie 參數保持一致  
}
```

### PyTorch 模型使用說明
若 USE_PYTORCH = True，請確保同目錄有 predict.py，並實作：
```python
def recognize(image: Image.Image) -> str:
    ...
```
範例程式碼詳見：
[https://github.com/alian613/ocr_captcha](https://github.com/alian613/ocr_captcha)


---


## SQLmap 使用範例
```bash
sqlmap -u https://target.site/form \
  --data="username=*&action=*" \
  --cookie="JSESSIONID=your-session-id" \
  --preprocess=preprocess_captcha.py \
  -v 6
```
- --data 請依目標網站的 POST 結構填寫
- -v 6 可查看完整 HTTP traffic，方便 debug CAPTCHA OCR

- SQLmap 會在每次發送請求前呼叫 preprocess() 函式，  
  例如：username=testuser&action=submit&captcha=1A2BC


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