from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView

from django.views import View
from django.conf import settings
from workspace.models import Workspace
# Create your views here.


class Index(View):
    def get(self, request):
        public_workspaces = Workspace.objects.filter(public=True)
        if request.user.is_authenticated:
            allowed_workspaces = request.user.workspace_set.all()
        else:
            allowed_workspaces = Workspace.objects.none()

        print(settings.LOGIN_URL)

        return render(
            request,
            template_name="root/index.html",
            context={
                "public_workspaces": public_workspaces,
                "allowed_workspaces": allowed_workspaces,
            }
        )


class Login(LoginView):
    template_name = "root/login.html"
    pass


class Logout(LogoutView):
    template_name = "root/logout.html"
    pass


class SignUp(View):
    template_name = "root/sign_up.html"
    pass