from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView
from .models import Field, Grade, Group, Level
from .forms import FieldForm, GradeForm, GroupForm, LevelForm


class HomeView(TemplateView):
    template_name = "core/home.html"


class FieldView(View):
    template_name = "core/home.html"
    form_class = FieldForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.template_name)
        else:
            print(form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        fields = Field.objects.all()
        return render(request, self.template_name, {'fields':fields})

    
class LevelView(View):
    template_name = "core/home.html"
    form_class = LevelForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.template_name)
        else:
            print(form.errors)
            return render(request, self.template_name, {})
    
    def get(self, request, *args, **kwargs):
        levels = Level.objects.all()
        return render(request, self.template_name, {'levels':levels})


class GradeView(View):
    template_name = "core/home.html"
    form_class = GradeForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.template_name)
        else:
            print(form.errors)
            return render(request, self.template_name, {})
    
    def get(self, request, *args, **kwargs):
        grades = Grade.objects.all()
        return render(request, self.template_name, {'grades':grades})


class GroupView(View):
    template_name = "core/home.html"
    form_class = GroupForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.template_name)
        else:
            print(form.errors)
            return render(request, self.template_name, {})
    
    def get(self, request, *args, **kwargs):
        groups = Group.objects.all()
        return render(request, self.template_name, {'groups':groups})
