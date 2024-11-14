from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from quizai.utils import JwtHandler
from users.models import User

from .models import Subject, Resoults
from .serializers import SubjectSerializer, ResoultsSerializer

import jwt, datetime


class SubjectSingleView(APIView):
    def get(self, request, id):
        payload = JwtHandler.check(request=request)
        subject = Subject.objects.filter(id=id).first()
        user = User.objects.filter(id=payload["id"]).first()

        if user.id != subject.user.id:
            raise AuthenticationFailed("Unauthorized!")

        serializer = SubjectSerializer(instance=subject)
        return Response(serializer.data)

    def delete(self, request, id):
        payload = JwtHandler.check(request=request)
        subject = Subject.objects.filter(id=id).first()
        user = User.objects.filter(id=payload["id"]).first()

        if user.id != subject.user.id:
            raise AuthenticationFailed("Unauthorized!")

        resoults = Resoults.objects.filter(subject=subject)

        for res in resoults :
            res.delete()

        subject.delete()

        return Response(status=200)

    
    

class SubjectView(APIView):
    def get(self, request):
        payload = JwtHandler.check(request=request)
        user = User.objects.filter(id=payload["id"]).first()
        subjects = Subject.objects.filter(user=user)

        serializer = SubjectSerializer(instance=subjects, many=True)

        return Response(serializer.data)

    def post(self, request):
        payload = JwtHandler.check(request=request)
        user = User.objects.filter(id=payload["id"]).first()
        serializer = SubjectSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(number_finished=0, user=user)

        return Response(serializer.data)


class ResoultsView(APIView):
    def post(self, request, id):
        payload = JwtHandler.check(request=request)
        subject= Subject.objects.filter(id=id).first()
        user = User.objects.filter(id=payload["id"]).first()
        serializer = ResoultsSerializer(data=request.data)

        if user.id != subject.user.id:
            raise AuthenticationFailed("Unauthorized!")

        serializer.is_valid(raise_exception=True)
        serializer.save(subject=subject, creation_date=datetime.datetime.now())

        resoults = Resoults.objects.filter(subject=subject)

        if ( resoults.count() >= 5):
            resoults[0].delete()

        accuracy = 0
        for res in resoults:
            accuracy = accuracy + res.accuracy
        accuracy = accuracy/resoults.count()

        # subject changes
        subject.number_finished = subject.number_finished + 1
        if (accuracy >= 65 and subject.difficulty < 4):
            subject.difficulty = subject.difficulty + 1
        if (accuracy <= 20 and subject.difficulty > 0):
            subject.difficulty = subject.difficulty - 1
        subject.save()

        return Response(serializer.data)

    def get(self, request, id):
        payload = JwtHandler.check(request=request)
        subject = Subject.objects.filter(id=id).first()
        user = User.objects.filter(id=payload["id"]).first()

        if user.id != subject.user.id:
            raise AuthenticationFailed("unauthorized!")

        resoults = subject.resoults_set.all()
        serializer = ResoultsSerializer(instance=resoults, many=True)

        return Response(serializer.data)