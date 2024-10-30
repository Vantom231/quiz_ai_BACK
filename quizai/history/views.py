from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from quizai.utils import JwtHandler
from users.models import User

from .models import HistoryQuestion, HistoryQuiz
from .serializers import HistoryQuestionSerializer, HistoryQuizSerializer

import jwt, datetime


class HistoryQuestionView(APIView):
    def post(self, request, id):
        payload = JwtHandler.check(request=request)
        quiz = HistoryQuiz.objects.filter(id=id).first()
        user = User.objects.filter(id=payload["id"]).first()
        serializer = HistoryQuestionSerializer(data=request.data, many=True)

        if user.id != quiz.user.id:
            raise AuthenticationFailed("Unauthorized!")

        serializer.is_valid(raise_exception=True)
        serializer.save(quiz=quiz)

        return Response(serializer.data)

    def get(self, request, id):
        payload = JwtHandler.check(request=request)
        quiz = HistoryQuiz.objects.filter(id=id).first()
        user = User.objects.filter(id=payload["id"]).first()

        if user.id != quiz.user.id:
            raise AuthenticationFailed("unauthorized!")

        questions = quiz.historyquestion_set.all()
        serializer = HistoryQuestionSerializer(instance=questions, many=True)

        return Response(serializer.data)
        


class HistoryQuizView(APIView):
    def post(self, request):
        payload = JwtHandler.check(request=request)
        user = User.objects.filter(id=payload["id"]).first()

        serializer = HistoryQuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        quiz =  HistoryQuiz.objects.filter(id=serializer.data["id"]).first()
        
        return Response(serializer.data)

    def get(self, request):
        payload = JwtHandler.check(request=request)
        user = User.objects.filter(id=payload["id"]).first()
        quizes = HistoryQuiz.objects.filter(user=user)

        serializer = HistoryQuizSerializer(quizes, many=True)

        return Response(serializer.data)


class HistoryQuizViewSingle(APIView):
    def get(self, request, id):
        
        quiz = HistoryQuiz.objects.filter(id=id).first()
        serializer = HistoryQuizSerializer(instance=quiz)
        return Response(serializer.data)