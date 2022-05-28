from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView
from .models import Classroom, Field, Grade, Group, Level, Teacher, Unit
from .forms import (
    ClassroomForm,
    FieldForm,
    GradeForm,
    GroupForm,
    LevelForm,
    TeacherForm,
    UnitForm,
)


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
            return render(request, self.template_name, {"fields": Field.objects.all()})
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
            return render(request, self.template_name, {"levels": Level.objects.all()})
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
            return render(request, self.template_name, {"grades": Grade.objects.all()})
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
            return render(request, self.template_name, {"groups": Group.objects.all()})
        else:
            print(form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        groups = Group.objects.all()
        return render(request, self.template_name, {"groups": groups})


class AccountView(TemplateView):
    template_name = "core/account.html"


class ClassroomView(View):
    """Cette vue c'est pour les salles de classe (exemple : Amphi 350, A250)."""

    template_name = "core/classroom.html"
    form_class = ClassroomForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.template_name, {"classrooms": Classroom.objects.all()})
        else:
            print(form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        classrooms = Classroom.objects.all()
        return render(request, self.template_name, {"classrooms": classrooms})


class TeacherView(View):
    """Cette vue c'est pour les enseignants."""

    template_name = "core/teacher.html"
    form_class = TeacherForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.template_name, {"teachers": Teacher.objects.all()})
        else:
            print(form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        teachers = Teacher.objects.all()
        return render(request, self.template_name, {"teachers": teachers})


class UnitView(View):
    """Cette vue c'est pour les unitées d'enseignement (exemple : Algorithmique)."""

    template_name = "core/unit.html"
    form_class = UnitForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.template_name, {"units": Unit.objects.all()})
        else:
            print(form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        units = Unit.objects.all()
        return render(request, self.template_name, {"units": units})


class TimetableView(TemplateView):
    """Cette vue c'est pour les emplois du temps."""

    template_name = "core/timetable.html"


class NotFoundView(TemplateView):
    template_name = "core/notFound.html"
