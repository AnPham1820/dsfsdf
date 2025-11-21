# Tệp: test_models.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load key từ file .env
load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("Lỗi: Không tìm thấy GOOGLE_API_KEY")
else:
    genai.configure(api_key=api_key)
    print("Đang lấy danh sách model...\n")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Lỗi kết nối: {e}")