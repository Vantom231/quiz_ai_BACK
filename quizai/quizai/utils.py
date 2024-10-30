from rest_framework.exceptions import AuthenticationFailed
from users.models import User
from .settings import SECRET_KEY

import jwt, datetime

class JwtHandler:
    def check(request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthorize')

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")
    
    def create(user: User, password: str) -> str:
        if user is None:
            raise AuthenticationFailed('User Not Found!')
        
        if not user.check_password(raw_password=password):
            raise AuthenticationFailed('Incorect Password!')
        
        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm="HS256")
        return token