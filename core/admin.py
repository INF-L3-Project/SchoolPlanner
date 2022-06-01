from django.contrib import admin
from .models import Classroom, Field, Grade, Group, Level, Provide, Teacher, Planning, Unit


class GradeAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity", "level", "field")
    list_search = ("name", )
    list_filter = ("level__name", "field__name")


class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity", "grade")
    list_search = ("name", )
    list_filter = ("grade__name", )


class UnitAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "_type")
    list_search = ("name", "code")
    list_filter = ("_type", )




class ProvideAdmin(admin.ModelAdmin):
    list_display = ("planning", "teacher", "unit", "classroom", "group", "day",
                    "start_time", "end_time")
    list_filter = ("planning", "teacher__name", "unit__name",
                   "classroom__name", "group__grade__name", "day")


admin.site.register(Field)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Level)
admin.site.register(Group, GroupAdmin)
admin.site.register(Classroom)
admin.site.register(Teacher)
admin.site.register(Planning)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Provide, ProvideAdmin)
