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
        
        system_prompt = ""
        system_prompt += f"Jesteś nauczycielem przedmiotu {subject.name}, "
        system_prompt += f"uczysz na poziomie {self._level[subject.level]} "

        user_prompt = ""
        user_prompt += f"Stwórz quiz składający się z {subject.number_of_questions} {self._difficulty[subject.difficulty]} pytań, "
        if subject.level_class:
            if subject.difficulty > 1 :
                user_prompt += f"dla roku {subject.level_class} {self._level[subject.level]} "
            else:
                user_prompt += f"dla {subject.level_class} klasy {self._level[subject.level]}, "
        if subject.question:
            user_prompt += f"na temat {subject.question}. "

        user_prompt += """Żadne z pytań nie może przekraczać 50 słów, dodadkowo do każdego z pytać dołącz 4 odpowiedzi, 
                    z których tylko jedna będzie poporawna, a trzy nie poprawne. 
                    Odpowiedź zamieść w tabeli json o strukturze: 
                    Pytani jako 'q', odpowiedź A jako 'a', odpowiedź B jako 'b', odpowiedź C jako 'c', odpowiedź D jako 'd',
                    i poprawna odpowiedź jako 'anw'.
                    Wygeneruj tylko tabelę, bez żadnych dodatkowych danych."""

        print(user_prompt)
        resp = client.chat.completions.create(
            messages = [
                {"role":"system", "content": system_prompt},
                {"role":"user", "content": user_prompt}
            ],
            model = "gpt-4o-mini",
            max_tokens=1000,
            temperature=0.7
        )

        res = resp.choices[0].message.content
        res = "[" + res.split("[")[1]
        res = res.split("]")[0] + "]"


        return Response(json.loads(res))
