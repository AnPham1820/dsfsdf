
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

# Import từ các app khác
from forum import sql as forum_sql
from accounts import sql as accounts_sql
from . import ai_service

# --- API: Danh sách môn học ---
class SubjectListAPIView(APIView):
    def get(self, request, format=None):
        subjects = accounts_sql.all_subject()
        return Response(subjects)

# --- API: Danh sách bài đăng (GET) & Tạo bài đăng (POST) ---
class PostListAPIView(APIView):
    # Yêu cầu đăng nhập cho POST
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            limit = int(request.query_params.get('limit', 20))
        except ValueError:
            limit = 20
        posts = forum_sql.latest_posts(limit)
        return Response(posts)

    def post(self, request, format=None):
        data = request.data
        title = data.get('title')
        content = data.get('content')
        subject_id = data.get('subject_id')
        user_id = request.user.id 

        if not title or not subject_id:
            return Response({"error": "Thiếu thông tin"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            forum_sql.insert_post(title, content, subject_id, user_id, None)
            return Response({"message": "Thành công"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- API: Chi tiết bài đăng ---
class PostDetailAPIView(APIView):
    def get(self, request, post_id, format=None):
        post_details = forum_sql.get_post_details(post_id)
        if not post_details:
            return Response({"error": "Không tìm thấy"}, status=status.HTTP_404_NOT_FOUND)
        return Response(post_details)
    
class AISummarizeView(APIView):
    """
    API: Tóm tắt nội dung
    POST /api/ai/summarize/
    Body: { "content": "..." }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        content = request.data.get('content')
        if not content:
            return Response({"error": "Thiếu nội dung để tóm tắt"}, status=status.HTTP_400_BAD_REQUEST)
        
        summary = ai_service.generate_summary(content)
        
        if summary:
            return Response({"summary": summary})
        else:
            return Response({"error": "Lỗi khi gọi OpenAI"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

class AIChatView(APIView):
    """
    API: Chatbot học tập
    POST /api/ai/chat/
    Body: { "message": "Câu hỏi..." }
    """

    def post(self, request):
        message = request.data.get('message')
        if not message:
            return Response({"error": "Vui lòng nhập câu hỏi"}, status=status.HTTP_400_BAD_REQUEST)
            
        answer = ai_service.suggest_answer(message)
        return Response({"answer": answer})