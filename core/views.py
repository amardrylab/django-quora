from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from questions.models import Questions, Answers, QuestionGroups
from .forms import RegisterForm, LoginForm
from .models import User
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

# Create your views here.

class DashboardView(FormView):
    def get(self, request):
        content={}
        if request.user.is_authenticated:
            user = request.user
            user.backend='django.contrib.core.backends.ModelBackend'
            ques_obj=Questions.objects.filter(user=user)
            content['userdetail']=user
            content['questions']=ques_obj
            ans_obj=Answers.objects.filter(question=ques_obj[0])
            content['answer']=ans_obj
            return render(request, 'dashboard.html',content)
        else:
            return redirect(reverse('login-view'))


class RegisterView(FormView):
    def get(self, request):
        content={}
        content['form']=RegisterForm
        return render(request,'register.html', content)
    
    def post(self, request):
        content={}
        form=RegisterForm(request.POST, request.FILES or None)
        if form.is_valid():
            save_it=form.save(commit=False)
            save_it.password=make_password(form.cleaned_data['password'])
            save_it.save()
            return redirect(reverse('dashboard-view'))
        content['form']=form
        template='register.html'
        return render(request, template, content)

class LoginView(FormView):
    content={}
    content['form']=LoginForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        content={}
        if request.user.is_authenticated:
            return redirect(reverse('dashboard-view'))
        content['form']=LoginForm
        return render(request, 'login.html', content)

    def post(self, request):
        content={}
        email=request.POST['email']
        password=request.POST['password']
        try:
            users=User.objects.filter(email=email)
            user=authenticate(request, username=users.first().username, password=password)
            login(request, user)
            return redirect(reverse('dashboard-view'))
        except Exception as e:
            content={}
            content['form']=LoginForm
            content['error']='Unable to login with provided credentials'+e
            return render_to_response('login.html', content)

class LogoutView(FormView):
    def get(self, request):
        logout(request)
        return redirect(reverse('login-view'))

