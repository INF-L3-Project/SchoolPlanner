from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView
from .models import Field, Grade, Group, Level
from .forms import FieldForm, GradeForm, GroupForm, LevelForm


class HomeView(TemplateView):
    template_name = "core/home.html"


class FieldView(View):
    """Cette vue c'est pour les filières (exemple : Informatique)."""

    template_name = "core/field.html"
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
        return render(request, self.template_name, {"fields": fields})


class LevelView(View):
    """Cette vue c'est pour les niveaux (exemple : 3 ou L3)."""

    template_name = "core/level.html"
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
        return render(request, self.template_name, {"levels": levels})


class GradeView(View):
    """Cette vue c'est pour les classes (exemple : Informatique L3)."""

    template_name = "core/grade.html"
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
        return render(request, self.template_name, {"grades": grades})


class GroupView(View):
    """Cette vue c'est pour les groupes (exemple : Informatique L3 - Genie Logiciel)."""

    template_name = "core/group.html"
    form_class = GroupForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Created !")
        else:
            print(form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        groups = Group.objects.all()
        return render(request, self.template_name, {"groups": groups, "form": self.form_class})


class AccountView(TemplateView):
    template_name = "core/account.html"


class ClassroomView(TemplateView):
    template_name = "core/classroom.html"


class TeacherView(TemplateView):
    template_name = "core/teacher.html"


class UnitView(TemplateView):
    template_name = "core/unit.html"


class TimetableView(TemplateView):
    template_name = "core/timetable.html"


class NotFoundView(TemplateView):
    template_name = "core/notFound.html"
