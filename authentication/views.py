from pprint import pprint
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, View
from authentication.forms import LoginForm, RegisterForm
from django.forms import ValidationError
from django.contrib import messages


class IndexView(TemplateView):
    template_name = 'authentication/home.html'


class LoginView(View):
    template_name = 'authentication/login.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):

        valuenext = request.GET.get("next", "/")
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(valuenext)
            else:
                messages.error(
                    request, "Adresse électronique/mot de passe non valide.")
                context = {"form": form}
                return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, {"form": form})

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})


class RegisterView(View):
    template_name = 'authentication/register.html'
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            # on cree un compte
            institution = form.save(commit=False)
            institution.logo = request.FILES['logo']
            institution.save()
            pprint(institution.logo)
            messages.success(request,
                             'Inscription reussie ! Connectez à présent')
            return redirect('authentication:login')

        else:
            print(form.errors)
            return render(request, self.template_name, {"form": form})


class Logout(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")
