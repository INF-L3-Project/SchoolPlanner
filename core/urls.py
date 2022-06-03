from django.urls import path
from core.views import ClassroomUpdateView, FieldUpdateView, HomeView, AccountView, FieldView, GradeView, ClassroomView, GroupView, LevelUpdateView, LevelView, TeacherView, UnitUpdateView, UnitView, TimetableView, NotFoundView

app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('account/', AccountView.as_view(), name='account'),
    path('field/', FieldView.as_view(), name='field'),
    path('field/<int:pk>/update',FieldUpdateView.as_view(),name='update_field'),

    path('grade/', GradeView.as_view(), name='grade'),
    path('classroom/', ClassroomView.as_view(), name='classroom'),
    path('classroom/<int:pk>/update',ClassroomUpdateView.as_view(),name='update_classroom'),
    path('group/', GroupView.as_view(), name='group'),

    path('level/', LevelView.as_view(), name='level'),
    path('level/<int:pk>/update',LevelUpdateView.as_view(),name='update_level'),

    path('teacher/', TeacherView.as_view(), name='teacher'),
    path('unit/', UnitView.as_view(), name='create_unit'),
    path('unit/<int:pk>/update', UnitUpdateView.as_view(), name='update_unit'),
    path('timetable/', TimetableView.as_view(), name='timetable'),
    path('error/', NotFoundView.as_view(), name='notFound'),
]
