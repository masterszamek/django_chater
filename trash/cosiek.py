from root.serializers import CreateIdeaSerializer
from django.contrib.auth.models import User

user = User.objects.get(username="maciek")
context={"user":user}
data={
    "title":"Aaaa",
    "text":"Sdsdsd",
    "priority":1,
}

iss = CreateIdeaSerializer(data=data, context=context)