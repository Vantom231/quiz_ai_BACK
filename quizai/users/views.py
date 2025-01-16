from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from quizai.utils import JwtHandler
from quizes.models import Subject

from .serializers import UserSerializer, DashboardSerializer
from .models import User
from .dashboard import Dashboard

import jwt, datetime, json

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
       serializer = UserSerializer(data=request.data) 
       serializer.is_valid(raise_exception=True)
       serializer.save()
       return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        # if user is None:
        #     raise AuthenticationFailed('User Not Found!')
        
        # if not user.check_password(raw_password=password):
        #     raise AuthenticationFailed('Incorect Password!')
        
        # payload = {
        #     "id": user.id,
        #     "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        #     "iat": datetime.datetime.utcnow()
        # }

        # token = jwt.encode(payload=payload, key='secret', algorithm="HS256")

        token = JwtHandler.create(user=user, password=password)

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):
    def get(self, request):
        # token = request.COOKIES.get('jwt')

        # if not token:
        #     raise AuthenticationFailed("Unauthenticated")
        
        # try:
        #     payload = jwt.decode(token, "secret", algorithms=["HS256"])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed("Unauthenticated")

        payload = JwtHandler.check(request=request)

        user = User.objects.filter(id=payload["id"]).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class DashboardView(APIView):
    def get(self, request):
        payload = JwtHandler.check(request=request)

        user = User.objects.filter(id=payload["id"]).first()
        subjects_len = len(Subject.objects.filter(user=user).all())

        dashboard = Dashboard()
        dashboard.finished_quizes = user.finished_quizes
        dashboard.subject_created = user.subject_created
        dashboard.quizes_generated = user.generated_quizes

        dashboard.name = user.name
        dashboard.email = user.email
        dashboard.user_name = user.username

        #dashboard.subject_list = subjects
        serializer = DashboardSerializer({
            "finished_quizes": user.finished_quizes, 
            "subject_active": subjects_len, 
            "subject_created": user.subject_created, 
            "quizes_generated": user.generated_quizes, 
            "name": user.name, 
            "email": user.email, 
            "user_name": user.username 
            })

        #res = json.dumps(dashboard)

        return Response(serializer.data)








class LogOutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "Logged Out"
        }

        return response