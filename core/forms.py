from django.shortcuts import get_object_or_404
from .models import Classroom, Field, Grade, Group, Level, Provide, Teacher, Unit
from django import forms


class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ("name", "abr")


class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = ("name", "abr")


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ("field", "level", "capacity")

    def save(self, commit=True):
        field = get_object_or_404(Field, id=self.cleaned_data["field"])
        level = get_object_or_404(Level, id=self.cleaned_data["level"])
        name = str(field.abr).upper() + "-" + str(level.abr).upper()
        return Grade.objects.create(
            name=name,
            capacity=self.cleaned_data["capacity"],
            field=self.cleaned_data["field"],
            level=self.cleaned_data["level"],
        )


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("name", "capacity", "grade")

    def clean_capacity(self):
        """Check if the capacity of the group is possible for the selected grade."""
        groups = Group.objects.all().filter(grade=self.data["grade"])
        grade = get_object_or_404(Grade, id=self.data["grade"])
        capacity = int(self.data["capacity"])
        if groups:
            all_capacity = 0
            for group in groups:
                all_capacity += group.capacity
            if (all_capacity + capacity) > grade.capacity:
                raise forms.ValidationError(
                    "La capacité est trop grande pour ce groupe"
                )
        elif capacity > grade.capacity:
            raise forms.ValidationError(
                "La capacité du groupe ne peut pas être plus grande que celle de la classe."
            )
        return capacity


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ("name", "capacity")


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ("name", "email", "number")


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ("name", "code", "_type", "grade")


class ProvideForm(forms.ModelForm):
    class Meta:
        model = Provide
        fields = "__all__"

    def clean(self):
        # Check if the group selected can doing course at the selected classroom
        group = get_object_or_404(Group, id=self.data["group"])
        classroom = get_object_or_404(Classroom, id=self.data["classroom"])
        if group.capacity > classroom.capacity:
            raise forms.ValidationError(
                "Cette salle ne peut pas contenir un groupe avec une telle capacité."
            )
        # Check if a classroom is already taken at the selected range
        if (
            Provide.objects.all()
            .filter(
                classroom=self.data["classroom"],
                day=self.data["day"],
                start_time=self.data["start_time"],
                end_time=self.data["end_time"],
            )
            .exists()
        ):
            raise forms.ValidationError(
                "Cette salle de classe est déjà occupé à cette plage horaire."
            )
        # Verify that a group is already taken at the selected range
        if (
            Provide.objects.all()
            .filter(
                group=self.data["group"],
                day=self.data["day"],
                start_time=self.data["start_time"],
                end_time=self.data["end_time"],
            )
            .exists()
        ):
            raise forms.ValidationError(
                "Ce groupe fait déjà cours à cette plage horaire."
            )
        # Verify that a teacher is already taken at the selected range
        if (
            Provide.objects.all()
            .filter(
                teacher=self.data["teacher"],
                day=self.data["day"],
                start_time=self.data["start_time"],
                end_time=self.data["end_time"],
            )
            .exists()
        ):
            raise forms.ValidationError(
                "Ce professeur est déjà pris à cette plage horaire."
            )
