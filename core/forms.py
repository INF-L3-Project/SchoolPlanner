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
        field_data = str(self.cleaned_data["field"])[0:4].upper()
        name = field_data + "-" + str(self.cleaned_data["level"]).upper()
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
        fields = ("name", "code", "unit_type")


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
        
        # Verify that a group is not doing 2 classes at the same time

        # Check that several groups are not teaching in the same classroom

        # Verify that a teacher does not teach in 2 classrooms at the same time
        
