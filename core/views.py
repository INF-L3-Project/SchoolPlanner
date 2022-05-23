from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    
class LoginView(TemplateView):
    template_name = 'core/login.html'


class SignupView(TemplateView):
    template_name = 'core/signup.html'
    
    
class AccountView(TemplateView):
    template_name = 'core/account.html'
    
class BranchView(TemplateView):
    template_name = 'core/branch.html'
    
  
class ClasseView(TemplateView):
    template_name = 'core/classe.html'
    
    
class ClassroomView(TemplateView):
    template_name = 'core/classroom.html'
    
    
class CourseView(TemplateView):
    template_name = 'core/course.html'
    
    
class LevelView(TemplateView):
    template_name = 'core/level.html'
    
    
class TeacherView(TemplateView):
    template_name = 'core/teacher.html'
    
    
class UnitView(TemplateView):
    template_name = 'core/unit.html'
    
    
class TimetableView(TemplateView):
    template_name = 'core/timetable.html'
    
    
class NotFoundView(TemplateView):
    template_name = 'core/notFound.html'
