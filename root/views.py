from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login

from workspace.forms import HiddenWorkspaceForm
from workspace.models import Workspace

from .models import Priority, WhatsNew, Idea
from .forms import IdeaForm

from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError
from django.core.exceptions import  ObjectDoesNotExist
# Create your views here.


class Index(View):
    template_name = "root/index.html"

    def get(self, request):
        print(id(request))
        print(id(self))
        context = self.initial_data(request)

        form = HiddenWorkspaceForm()

        context["form"] = form
        return render(
            request,
            template_name=self.template_name,
            context=context
        )

    def post(self, request):

        print(request.POST)
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

        


def ideas(request):
    template_name = "root/ideas.html"
    modal_form_url = reverse("root:ideas")
    priorities = Priority.objects.all()
    whats_new_p = WhatsNew.objects.all()
    modal_form = IdeaForm()
    modal_form_error_id = False


    if request.POST:
        modal_form = IdeaForm(request.POST)
        priority = Priority.objects.get(priority=request.POST['modal_form_id'][-1])
        user = request.user
        print(modal_form, priority, user, sep="\n")
        if modal_form.is_valid():
            idea = Idea(author=user, priority=priority, title=modal_form.cleaned_data.get("title"), text=modal_form.cleaned_data.get("text"))
            idea.save()
            redirect("root:ideas")
        else:
            modal_form.add_error(None, "something went wrong")
            modal_form_error_id = request.POST['modal_form_id']



    context = {
        "priorities": priorities,
        "whats_new_p": whats_new_p,
        "modal_form_url": modal_form_url,
        "modal_form":modal_form,
        "modal_form_error_id": modal_form_error_id
    }

    return render(
        request, 
        template_name=template_name, 
        context=context
    )

class Login(LoginView):
    template_name = "root/login.html"


class Logout(LogoutView):
    template_name = "root/logout.html"


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
