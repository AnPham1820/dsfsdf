# Tệp: api/ai_service.py

import google.generativeai as genai
from django.conf import settings
import os
from dotenv import load_dotenv

def get_model():
    """
    Cấu hình và lấy model Gemini
    """
    load_dotenv()
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Lỗi: Chưa cấu hình GOOGLE_API_KEY trong file .env")
        return None
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash')

def generate_summary(text):
    """
    Hàm tóm tắt nội dung bài viết
    """
    model = get_model()
    if not model:
        return "Chức năng tóm tắt đang bảo trì."

    try:
        prompt = f"Bạn là một trợ lý học tập. Hãy tóm tắt văn bản sau một cách ngắn gọn bằng tiếng Việt:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Lỗi Gemini: {e}")
        return "Không thể tóm tắt lúc này."

def suggest_answer(question):
    """
    Hàm gợi ý câu trả lời (Chatbot)
    """
    model = get_model()
    if not model:
        return "Chức năng Chatbot đang bảo trì."

    try:
        prompt = f"Bạn là một giảng viên đại học nhiệt tình tại trường PEPE. Hãy giải đáp câu hỏi sau của sinh viên một cách chính xác, ngắn gọn và dễ hiểu:\n\nCâu hỏi: {question}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Lỗi Gemini: {e}")
        return "Xin lỗi, hệ thống đang bận. Vui lòng thử lại sau."