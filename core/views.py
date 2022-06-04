import re
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.db.models import Q
from django.views.generic import TemplateView
from django.contrib.auth.models import User
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
        user = get_object_or_404(User, id=request.user.id)
        institution = get_object_or_404(Institution, user=user)
        form = self.form_class(data=request.POST)
        if form.is_valid():
            field = form.save(commit=False)
            field.institution = institution
            field.save()
            return redirect("core:field")
        else:
            print(form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):

        print(request.user.institution.name)
        form = self.form_class()
        fields = Field.objects.all()
        return render(request, self.template_name, {"fields": fields, "form": form})


@method_decorator(decorators, name="get")
class FieldUpdateView(View):

    template_name = "core/field.html"
    form_class = FieldForm
    field = Field.objects.all()

    def post(self, request, *args, **kwargs):

        field = Field.objects.get(id=kwargs["pk"])
        form = self.form_class(request.POST, instance=field)
        if form.is_valid():
            form = form.save()
            return redirect("core:field")
        else:
            print(form.errors)
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "field": self.field,
                },
            )

    def get(self, request, *args, **kwargs):

        field = Field.objects.get(id=kwargs["pk"])
        form = self.form_class(request.POST, instance=field)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "field": self.field,
            },
        )


@method_decorator(decorators, name="get")
class LevelView(View):
    """Cette vue c'est pour les niveaux (exemple : 3 ou L3)."""

    template_name = "core/level.html"
    form_class = LevelForm

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        institution = get_object_or_404(Institution, user=user)
        form = self.form_class(data=request.POST)
        if form.is_valid():
            field = form.save(commit=False)
            field.institution = institution
            field.save()
            return redirect("core:level")
        else:
            print(form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        levels = Level.objects.all()
        return render(request, self.template_name, {"levels": levels, "form": form})


@method_decorator(decorators, name="get")
class LevelUpdateView(View):

    template_name = "core/level.html"
    form_class = LevelForm
    level = Level.objects.all()

    def post(self, request, *args, **kwargs):

        level = Level.objects.get(id=kwargs["pk"])
        form = self.form_class(request.POST, instance=level)
        if form.is_valid():
            form = form.save()
            print(form)
            return redirect("core:level")
        else:
            print(form.errors)
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "level": self.level,
                },
            )

    def get(self, request, *args, **kwargs):

        level = Level.objects.get(id=kwargs["pk"])
        form = self.form_class(request.POST, instance=level)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "level": self.level,
            },
        )


@method_decorator(decorators, name="get")
class GradeView(View):
    """Cette vue c'est pour les classes (exemple : Informatique L3)."""

    template_name = "core/grade.html"
    form_class = GradeForm
    fields = Field.objects.all()
    levels = Level.objects.all()

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.name = str(grade.field.abr).upper() + "-" + str(grade.level.abr).upper()
            grade.save()
            return redirect("core:grade")
        else:
            print(form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        grade = Grade.objects.all()

        searched = request.GET.get("searched")
        trier = request.GET.get("trier")
        filtrer_par_capacite = request.GET.get("filtrer_par_capacite")
        if searched:
            print(searched)
            grade = Grade.objects.filter(
                Q(name__icontains=searched)
                | Q(field__name__icontains=searched)
                | Q(level__name__icontains=searched)
            )

        if filtrer_par_capacite == "gt_500":
            grade = Grade.objects.filter(capacity__gt=500)
        elif filtrer_par_capacite == "lt_500":
            grade = Grade.objects.filter(capacity__lt=500)
        elif filtrer_par_capacite == "lt_100":
            grade = Grade.objects.filter(capacity__lt=100)

        if trier == "niveau":
            grade = Grade.objects.order_by("level__abr")
        elif trier == "filiere":
            grade = Grade.objects.order_by("field__abr")
        form = self.form_class()
        return render(
            request,
            self.template_name,
            {
                "grades": grade,
                "form": form,
                "fields": Field.objects.all(),
                "levels": Level.objects.all(),
            },
        )


@method_decorator(decorators, name="get")
class GradeUpdateView(View):

    template_name = "core/grade.html"
    form_class = GradeForm
    grade = Grade.objects.all()

    def post(self, request, *args, **kwargs):
        fields = Field.objects.all()
        levels = Level.objects.all()
        grade = Grade.objects.get(id=kwargs["pk"])
        form = self.form_class(request.POST, instance=grade)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.name = str(grade.field.abr).upper() + "-" + str(grade.level.abr).upper()
            grade.save()
            return redirect("core:grade")
        else:
            print(form.errors)
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "grades": self.grade,
                    "fields": fields,
                    "levels": levels,
                },
            )

    def get(self, request, *args, **kwargs):
        fields = Field.objects.all()
        levels = Level.objects.all()
        grade = Grade.objects.get(id=kwargs["pk"])
        form = self.form_class(request.POST, instance=grade)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "grades": self.grade,
                "fields": fields,
                "levels": levels,
            },
        )


@method_decorator(decorators, name="get")
class GroupView(View):
    """Cette vue c'est pour les groupes (exemple : Informatique L3 - Genie Logiciel)."""

    template_name = "core/group.html"
    form_class = GroupForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:group")
        else:
            print(form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        groups = Group.objects.all() 
        searched = request.GET.get("searched")
        trier = request.GET.get("trier")
        filtrer_par_capacite = request.GET.get("filtrer_par_capacite")
        if searched:
            print(searched)
            groups = Group.objects.filter(
                Q(name__icontains=searched) | Q(grade__name__icontains=searched)
            )

        if filtrer_par_capacite == "gt_500":
            groups = Group.objects.filter(capacity__gt=500)
        elif filtrer_par_capacite == "lt_500":
            groups = Group.objects.filter(capacity__lt=500)
        elif filtrer_par_capacite == "lt_100":
            groups = Group.objects.filter(capacity__lt=100)

        if trier == "classe":
            groups = Group.objects.order_by("grade__name")
        form = self.form_class()
        return render(
            request,
            self.template_name,
            {"groups": groups, "form": form, "grades": Grade.objects.all()},
        )


@method_decorator(decorators, name="get")
class GroupUpdateView(View):

    template_name = "core/group.html"
    form_class = GroupForm
    grades = Grade.objects.all()

    def post(self, request, *args, **kwargs):
        group = Group.objects.get(id=kwargs["pk"])
        form = self.form_class(request.POST, instance=group)
        print(form.data)
        if form.is_valid():
            form = form.save()
            print(form)
            return redirect("core:group")
        else:
            print(form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        group = Group.objects.get(id=kwargs["pk"])
        form = self.form_class(instance=group)
        return render(
            request,
            self.template_name,
            {"groups": self.groups, "form": form, "grades": self.grades},
        )


@method_decorator(decorators, name="get")
class AccountView(View):
    template_name = "core/account.html"
    form_class = AccountForm

    def post(self, request, *args, **kwargs):
        current_account = get_object_or_404(Institution, user=request.user.id)
        last_name = request.POST["last_name"]
        name = request.POST["name"]
        # if request.FILES['logo']:
        #     current_account.logo = request.FILES['logo']
        current_account.name = name
        request.user.last_name = last_name
        request.user.save()
        current_account.user = request.user
        current_account.save()
        messages.success(request, "mise a jour avec succès")
        return redirect("core:account")

    def get(self, request, *args, **kwargs):
        current_account = get_object_or_404(Institution, user=request.user.id)
        return render(request, self.template_name, {"current_account": current_account})


@method_decorator(decorators, name="get")
class ClassroomView(View):
    """Cette vue c'est pour les salles de classe (exemple : Amphi 350, A250)."""

    template_name = "core/classroom.html"
    form_class = ClassroomForm

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        institution = get_object_or_404(Institution, user=user)
        form = self.form_class(data=request.POST)
        if form.is_valid():
            field = form.save(commit=False)
            field.institution = institution
            field.save()
            return render(
                request, self.template_name, {"classrooms": Classroom.objects.all()}
            )
        else:
            print(form.errors)
            return render(request, self.template_name, {})

    def get(self, request, *args, **kwargs):
        classroom = Classroom.objects.all()

        searched = request.GET.get("searched")
        trier_par_capacite = request.GET.get("trier_par_capacite")
        filtrer_par_capacite = request.GET.get("filtrer_par_capacite")
        print(request.GET)

        if searched:
            print(searched)
            classroom = Classroom.objects.filter(name__icontains=searched)

        if filtrer_par_capacite == "gt_500":
            classroom = Classroom.objects.filter(capacity__gt=500)
        elif filtrer_par_capacite == "lt_500":
            classroom = Classroom.objects.filter(capacity__lt=500)
        elif filtrer_par_capacite == "lt_100":
            classroom = Classroom.objects.filter(capacity__lt=100)

        if trier_par_capacite == "cc":
            classroom = Classroom.objects.order_by("capacity")
        elif trier_par_capacite == "cd":
            classroom = Classroom.objects.order_by("-capacity")
        form = self.form_class()

        return render(
            request, self.template_name, {"classrooms": classroom, "form": form}
        )


@method_decorator(decorators, name="get")
class ClassroomUpdateView(View):

    template_name = "core/classroom.html"
    form_class = ClassroomForm
    classroom = Classroom.objects.all()

    def post(self, request, *args, **kwargs):

        classroom = Classroom.objects.get(id=kwargs["pk"])
        form = self.form_class(request.POST, instance=classroom)
        if form.is_valid():
            form = form.save()
            print(form)
            return redirect("core:classroom")
        else:
            print(form.errors)
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "classrooms": self.classroom,
                },
            )

    def get(self, request, *args, **kwargs):

        classroom = Classroom.objects.get(id=kwargs["pk"])
        form = self.form_class(request.POST, instance=classroom)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "classrooms": self.classroom,
            },
        )


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
        current_user = get_object_or_404(User, id=request.user.id)
        institution = get_object_or_404(Institution, user=current_user)
        form = self.form_class(data=request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.institution = institution
            unit.save()
            return render(request, self.template_name, {"units": Unit.objects.all()})
        else:
            print(form.errors)
            return render(request, self.template_name, {"form": form})

    def get(self, request, *args, **kwargs):
        grades = Grade.objects.all()
        units = Unit.objects.all()
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
