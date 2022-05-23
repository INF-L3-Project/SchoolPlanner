from .models import Field, Grade, Group, Level
from django import forms


class FieldForm(forms.Form):
    class Meta:
        model = Field
        fields = ("name", "abr")

    def save(self, commit=True):
        name = self.cleaned_data["name"]
        abr = self.cleaned_data["abr"]
        return Field.objects.create(name=name, abr=abr)


class LevelForm(forms.Form):
    class Meta:
        model = Level
        fields = ("name", "abr")

    def save(self, commit=True):
        name = self.cleaned_data["name"]
        abr = self.cleaned_data["abr"]
        return Level.objects.create(name=name, abr=abr)


class GradeForm(forms.Form):
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


class GroupForm(forms.Form):
    class Meta:
        model = Group
        fields = ("name", "capacity", "grade")

    def clean_capacity(self):
        """Check if the capacity of the group is possible for the selected grade."""
        groups = Group.objects.all().filter(grade=self.cleaned_data["grade"])
        capacity = self.cleaned_data["capacity"]
        if groups:
            all_capacity = 0
            for group in groups:
                all_capacity += group.capacity
            if (all_capacity + capacity) > self.cleaned_data["grade"].capacity:
                raise forms.ValidationError(
                    "La capacité est trop grande pour ce groupe"
                )
        elif capacity > self.cleaned_data["grade"].capacity:
            raise forms.ValidationError(
                "La capacité du groupe ne peut pas être plus grande que celle de la classe."
            )
        return capacity

    def save(self, commit=True):
        name = self.cleaned_data["name"]
        capacity = self.cleaned_data["capacity"]
        grade = self.cleaned_data["grade"]
        return Group.objects.create(name=name, capacity=capacity, grade=grade)
