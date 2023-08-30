from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import connections

# Create your views here.

def home(request):
    return render(request,'main/index.html')

def login(request):
    if request.POST:
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        sql = "select * from logintb where user_id='"+user_name+"' and password='"+password+"'"
        user = connections.select(sql)
        if user:
            if user[2]=='admin':
                request.session['admin']=user
                return HttpResponseRedirect('administrator')
        else:
            return render(request,'main/login.html',{'error':"Invalid Credentials"})
    return render(request,'main/login.html')

def admin(request):
    return render(request,'administrator/index.html')

def artistAp(request):
    return render(request,'administrator/artistAprovals.html')

