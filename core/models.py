from django.db import models


class Field(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    abr = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    abr = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
        unique=True,
    )
    capacity = models.IntegerField(null=False)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.field.abr}-{self.level.abr}"


class Group(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    capacity = models.IntegerField(null=False)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.grade.name}-{self.name}"


class Classroom(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    capacity = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.name}-{self.capacity}"


class Teacher(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, null=True, blank=True)
    number = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.name}"


class Type(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Unit(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    code = models.CharField(max_length=100, null=False, unique=True)
    unit_type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code}-{self.name}"


class Provide(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    day = models.CharField(
        max_length=100,
        choices=[
            (day, day)
            for day in [
                "Lundi",
                "Mardi",
                "Mercredi",
                "Jeudi",
                "Vendredi",
                "Samedi",
                "Dimanche",
            ]
        ],
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.teacher}|{self.unit.code}|{self.classroom}|{self.group.name}"
