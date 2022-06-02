from django.db import models
from authentication.models import Institution


class Field(models.Model):
    name = models.CharField(max_length=100, null=False)
    abr = models.CharField(max_length=50, null=True, blank=True)
    institution = models.ForeignKey(Institution, models.CASCADE)

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=100, null=False)
    abr = models.CharField(max_length=50, null=False)
    institution = models.ForeignKey(Institution, models.CASCADE)

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
        unique=True,
    )
    capacity = models.IntegerField(null=False, default=100)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.field.abr}-{self.level.abr}"


class Group(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    capacity = models.IntegerField(null=False, default=100)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.grade.name}-{self.name}"


class Classroom(models.Model):
    name = models.CharField(max_length=100, null=False)
    capacity = models.IntegerField(null=False, default=100)
    institution = models.ForeignKey(Institution, models.CASCADE)

    def __str__(self):
        return f"{self.name}-{self.capacity}"


class Teacher(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, null=True, blank=True)
    number = models.IntegerField(null=True)
    institution = models.ForeignKey(Institution, models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Unit(models.Model):
    TYPE = [("TP", "TP"), ("TD", "TD"), ("Cours", "Cours")]

    name = models.CharField(max_length=255, null=False, unique=True)
    code = models.CharField(max_length=100, null=False, unique=True)
    type = models.CharField(max_length=10, choices=TYPE, default="Cours")
    grade = models.ForeignKey(Grade, models.CASCADE)
    institution = models.ForeignKey(Institution, models.CASCADE)

    def __str__(self):
        return f"{self.code}-{self.name}--{self.type}"


class Planning(models.Model):
    name = models.CharField(max_length=100, null=False)
    school_year = models.CharField(max_length=50, null=False)
    semestre = models.CharField(max_length=20, null=False)
    institution = models.ForeignKey(Institution, models.CASCADE)
    grade = models.ForeignKey(Grade, models.CASCADE)

    def __str__(self):
        return self.name


class Provide(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    planning = models.ForeignKey(Planning, on_delete=models.CASCADE)
    day = models.CharField(
        max_length=100,
        choices=[(day, day) for day in [
            "Lundi",
            "Mardi",
            "Mercredi",
            "Jeudi",
            "Vendredi",
            "Samedi",
            "Dimanche",
        ]],
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.teacher}|{self.unit.code}|{self.classroom}|{self.group.name}"
