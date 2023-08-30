from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import connections
from django.core.files.storage import FileSystemStorage
from random import randint

# Create your views here.

# Home

def home(request):
    context = {}
    if 'admin' in request.session:
        context['admin_data']=request.session['admin']
        return render(request,'main/index.html',context)
    return render(request,'main/index.html')


# Registration and login

def register(request):
    if request.POST:
        if request.POST.get("submit")=="artist":
            if request.POST.get("password")==request.POST.get("c_password"):
                name = request.POST.get("name")
                id = request.POST.get("artist_id")
                d_name = request.POST.get("d_name")
                email = request.POST.get("email")
                contact = request.POST.get("contact")
                address = request.POST.get("address")
                gender = request.POST.get("gender")
                password = request.POST.get("password")
                fs = FileSystemStorage()
                image = request.FILES['pic']
                image_name = id+str(randint(1,10000))+image.name
                fs.save("artist/profile_pic/"+image_name,image)
                sql = "insert into artist_list(name,artist_id,email,password,contact,profile_pic,gender,display_name,address,status)values('"+name+"','"+id+"','"+email+"','"+password+"','"+contact+"','"+image_name+"','"+gender+"','"+d_name+"','"+address+"','0')"
                connections.insert(sql)
                sql = "insert into logintb(user_id,user_type,status,password)values('"+id+"','artist','0','"+password+"')"
                connections.insert(sql)
                return render(request,'main/login.html',{'msg':"Registration Successful"})
            else:
                pass
    return render(request,'main/register.html')

def login(request):
    if 'admin' in request.session.keys():
        return HttpResponseRedirect('home')
    else:
        context={}
        if request.POST:
            user_name = request.POST.get('username')
            password = request.POST.get('password')
            sql = "select * from logintb where user_id='"+user_name+"' and password='"+password+"'"
            user = connections.select(sql)
            if user:
                if user[2]=='artist' and user[3]==1:
                    request.session['artist']=user
                    context['user_data']=user
                    return render(request,'main/index.html',context)
                elif user[2]=='admin':
                    request.session['admin']=user
                    return HttpResponseRedirect('administrator')
                else:
                    return render(request,'main/login.html',{'error':"Invalid Credentials"})
            else:
                return render(request,'main/login.html',{'error':"Invalid Credentials"})
        return render(request,'main/login.html')

def logout(request):
    if 'artist' in request.session.keys():
        del request.session['artist']
    elif 'admin' in request.session.keys():
        del request.session['admin']
    return HttpResponseRedirect('home')


# Admin

def admin(request):
    context ={}
    if request.session['admin']:
        context['admin']=request.session['admin']
        sql = "select * from artist_list where status=0"
        artist_aprovals = connections.selectall(sql)
        context['aprovals']=artist_aprovals
        context['aprovals_len']=len(artist_aprovals)
        return render(request,'administrator/index.html',context)

def artistAp(request):
    context ={}
    if request.session['admin']:
        context['admin']=request.session['admin']
        sql = "select * from artist_list where status=0"
        artist_aprovals = connections.selectall(sql)
        context['aprovals']=artist_aprovals
        return render(request,'administrator/artistAprovals.html',context)
    return render(request,'error')

def viewArtist(request):
    context ={}
    if request.session['admin']:
        id = request.GET.get('id')
        context['admin']=request.session['admin']
        sql = "select * from artist_list where artist_id='"+id+"'"
        artist_details = connections.select(sql)
        context['details']=artist_details
        return render(request,'administrator/artistView.html',context)
    return render(request,'error')


def error(request):
    return HttpResponseRedirect('404_error.html')

def test(request):
    return render(request,'test.html',{'admin':request.session['admin']})
