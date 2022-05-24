from django.urls import path
from core.views import HomeView, AccountView, BranchView, ClasseView, ClassroomView, CourseView, LevelView, TeacherView, UnitView, TimetableView, NotFoundView

app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('account/', AccountView.as_view(), name='account'),
    path('branch/', BranchView.as_view(), name='branch'),
    path('classe/', ClasseView.as_view(), name='classe'),
    path('classroom/', ClassroomView.as_view(), name='classroom'),
    path('course/', CourseView.as_view(), name='course'),
    path('level/', LevelView.as_view(), name='level'),
    path('teacher/', TeacherView.as_view(), name='teacher'),
    path('unit/', UnitView.as_view(), name='contact'),
    path('timetable/', TimetableView.as_view(), name='timetable'),
    path('error/', NotFoundView.as_view(), name='notFound'),
]
