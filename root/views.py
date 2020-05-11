from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from workspace.forms import HiddenWorkspaceForm
from workspace.models import Workspace


from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError
from django.core.exceptions import  ObjectDoesNotExist
# Create your views here.


class Index(View):
    template_name = "root/index.html"

    def get(self, request):
        context = self.initial_data(request)

        form = HiddenWorkspaceForm()

        context["form"] = form
        return render(
            request,
            template_name=self.template_name,
            context=context
        )

    def post(self, request):
        context = self.initial_data(request)
        form = HiddenWorkspaceForm(request.POST)

        if form.is_valid():
            workspace_name = form.cleaned_data.get("name")
            workspace_password = form.cleaned_data.get("password")

        try:
            workspace = Workspace.objects.get(name=workspace_name, public=True)
            if workspace.password != workspace_password:
                raise ValidationError(_("Password is incorect"))
            workspace.users.add(request.user)
            return redirect(workspace)

        except ObjectDoesNotExist as E:
            form.add_error(None, "workspace doesn`t exist")
        except ValidationError as E:
            form.add_error(None, E.message)


        context['form'] = form

        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )

    def initial_data(self, request):
        public_workspaces = Workspace.objects.filter(public=True, hidden=False)
        if request.user.is_authenticated:
            allowed_workspaces = request.user.workspace_set.all()
        else:
            allowed_workspaces = Workspace.objects.none()

        context = {
                "public_workspaces": public_workspaces,
                "allowed_workspaces": allowed_workspaces,
        }
        return context

class Login(LoginView):
    template_name = "root/login.html"
    pass


class Logout(LogoutView):
    template_name = "root/logout.html"
    pass


class SignUp(View):
    template_name = "root/sign_up.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("root:index")

        form = UserCreationForm()
        return render(request, template_name=self.template_name, context={"form": form})

    def post(self, request):

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("root:index")
        else:
            return render(request, template_name=self.template_name, context={"form": form})
