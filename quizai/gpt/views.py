from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from openai import OpenAI
import os

from quizai.utils import JwtHandler
from users.models import User
from quizes.models import Subject, Resoults

import jwt, datetime, json


class generationView(APIView):
    _level = [
        "szkoły podstawowej",
        "szkoły licealnej",
        "studiów inżynierskich",
        "studiów magisterskich",
        "studiów doktorskich",
    ]

    _difficulty = [
        "bardzo łatwych",
        "łatwych",
        "średnio trudnych",
        "trudnych",
        "bardzo trudnych",
    ]

    def get(self, request, id):
        payload = JwtHandler.check(request=request)
        subject = Subject.objects.filter(id=id).first()
        user = User.objects.filter(id=payload["id"]).first()

        if user.id != subject.user.id:
            raise AuthenticationFailed("Unauthorized!")

        resoults = Resoults.objects.filter(subject=subject)

        api_key = os.getenv("OPENAI_API_KEY")

        client = OpenAI(api_key=api_key)

        resp = client.chat.completions.create(
            messages = [
                {"role":"system", "content": f"Jesteś nauczycielem przedmiotu {subject.name} na poziomie {self._level[subject.level]}"},
                {"role":"user", "content": f"""wygeneruj quiz składający się z {subject.number_of_questions} {self._difficulty[subject.difficulty]} pytań. 
                    Żadne z pytań nie może przekraczać 50 słów, dodadkowo do każdego z pytać dołącz 4 odpowiedzi, 
                    z których tylko jedna będzie poporawna, a trzy nie poprawne. 
                    Odpowiedź zamieść w tabeli json o strukturze: 
                    Pytani jako 'q', odpowiedź A jako 'a', odpowiedź B jako 'b', odpowiedź C jako 'c', odpowiedź D jako 'd',
                    i poprawna odpowiedź jako 'anw'.
                    Wygeneruj tylko tabelę, bez żadnych dodatkowych danych."""}
            ],
            model = "gpt-4o-mini",
            max_tokens=1000,
            temperature=0.7
        )

        res = resp.choices[0].message.content
        res = "[" + res.split("[")[1]
        res = res.split("]")[0] + "]"


        return Response(json.loads(res))
