from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.db.models import Q
from django.views.generic import TemplateView, UpdateView
from authentication.models import Institution
from .models import Classroom, Field, Grade, Group, Level, Planning, Teacher, Unit
from .forms import (
    AccountForm,
    ClassroomForm,
    FieldForm,
    GradeForm,
    GroupForm,
    LevelForm,
    PlanningForm,
    TeacherForm,
    UnitForm,
)
import json

decorators = [
    login_required(login_url="authentication:login", redirect_field_name="next")
]


@method_decorator(decorators, name="get")
class HomeView(View):
    template_name = "core/home.html"
    form_class = PlanningForm

    def post(self, request, *args, **kwargs):
        # Récupération de l'utilisateur courant
        current_user = get_object_or_404(User, id=request.user.id)
        # Récupération de l'institution liée à cet utilisateur
        institution = get_object_or_404(Institution, user=current_user)
        form = self.form_class(data=request.POST)
        if form.is_valid():
            # Sauvegarde temporaire sans mise en BD
            planning = form.save(commit=False)
            # Mise à jour de la valeur institution
            planning.institution = institution
            # Sauvegarde définitive en BD
            planning.save()
            return render(
                request,
                self.template_name,
                {"plannings": Planning.objects.all(), "grades": Grade.objects.all()},
            )
        else:
            messages(request, form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        plannings = Planning.objects.all()
        grades = Grade.objects.all()
        return render(
            request, self.template_name, {"plannings": plannings, "grades": grades}
        )


@method_decorator(decorators, name="get")
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
            messages(request, form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        print(request.user.institution.name)
        form = self.form_class()
        fields = Field.objects.all()
        return render(request, self.template_name, {"fields": fields, "form": form})


@method_decorator(decorators, name="get")
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
            messages(request, form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        levels = Level.objects.all()
        return render(request, self.template_name, {"levels": levels, "form": form})


@method_decorator(decorators, name="get")
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
            messages(request, form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        grades = Grade.objects.all()
        return render(request, self.template_name, {"grades": grades, "form": form})


@method_decorator(decorators, name="get")
class GroupView(View):
    """Cette vue c'est pour les groupes (exemple : Informatique L3 - Genie Logiciel)."""

    template_name = "core/group.html"
    form_class = GroupForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.template_name, {"groups": Group.objects.all(), "grades":Grade.objects.all()})
        else:
            messages(request, form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        searched = request.GET.get("searched")
        trier_par_nom = request.GET.get("trier_par_nom")
        if searched:
            print(searched)
            groups = Group.objects.filter(name__icontains=searched)
        if trier_par_nom == "a-z":
            groups = Group.objects.order_by("name")
        elif trier_par_nom == "z-a":
            groups = Group.objects.order_by("-name")
        # if filtrer_par_grade:
        groups = Group.objects.all()
        grades = Grade.objects.all()
        return render(request, self.template_name, {"groups": groups, "grades": grades})


@method_decorator(decorators, name="get")
class AccountView(View):
    template_name = "core/account.html"
    form_class = AccountForm

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


@method_decorator(decorators, name="get")
class ClassroomView(View):
    """Cette vue c'est pour les salles de classe (exemple : Amphi 350, A250)."""

    template_name = "core/classroom.html"
    form_class = ClassroomForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            return render(
                request, self.template_name, {"classrooms": Classroom.objects.all()}
            )
        else:
            messages(request, form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        classrooms = Classroom.objects.all()
        return render(request, self.template_name, {"classrooms": classrooms})


@method_decorator(decorators, name="get")
class TeacherView(View):
    """Cette vue c'est pour les enseignants."""

    template_name = "core/teacher.html"
    form_class = TeacherForm

    def post(self, request, *args, **kwargs):
        current_user = get_object_or_404(User, id=request.user.id)
        institution = get_object_or_404(Institution, user=current_user)
        form = self.form_class(data=request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.institution = institution
            teacher.save()
            return render(
                request, self.template_name, {"teachers": Teacher.objects.all()}
            )
        else:
            messages(request, form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        searched = request.GET.get("searched")
        trier_par_nom = request.GET.get("trier_par_nom")
        if searched:
            print(searched)
            # je fais un filtre selon deux valeur, il s'agit enfait d'une Union
            teachers = Teacher.objects.filter(
                Q(name__icontains=searched) | Q(numero__icontains=searched)
            )
        if trier_par_nom == "a-z":
            teachers = Teacher.objects.order_by("name")
        elif trier_par_nom == "z-a":
            teachers = Teacher.objects.order_by("-name")

        teachers = Teacher.objects.all()
        return render(request, self.template_name, {"teachers": teachers})


@method_decorator(decorators, name="get")
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
            return render(request, self.template_name, {"form": form})

    def get(self, request, *args, **kwargs):
        grades = Grade.objects.all()
        units = Unit.objects.all()
        serializer_data = []
        return render(
            request,
            self.template_name,
            {
                "units": units,
                "grades": grades,
            },
        )


@method_decorator(decorators, name="get")
class UnitUpdateView(View):

    template_name = "core/unit.html"
    form_class = UnitForm
    grades = Grade.objects.all()
    units = Unit.objects.all()

    def post(self, request, *args, **kwargs):

        unit = Unit.objects.get(id=kwargs["pk"])
        form = self.form_class(request.POST, instance=unit)
        if form.is_valid():
            form = form.save()
            return redirect("core:create_unit")
        else:
            print(form.errors)
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "units": self.units,
                    "grades": self.grades,
                },
            )

    def get(self, request, *args, **kwargs):

        unit = Unit.objects.get(id=kwargs["pk"])
        form = self.form_class(request.POST, instance=unit)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "units": self.units,
                "grades": self.grades,
            },
        )


@method_decorator(decorators, name="get")
class TimetableView(TemplateView):
    """Cette vue c'est pour les emplois du temps."""

    template_name = "core/timetable.html"


class NotFoundView(TemplateView):
    template_name = "core/notFound.html"
