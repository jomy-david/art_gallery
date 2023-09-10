from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import connections
from django.core.files.storage import FileSystemStorage
from random import randint

# Create your views here.

# Home

def home(request):
    context = {}
    sql = "select * from category_list"
    context['cat']=connections.selectall(sql)
    if 'admin' in request.session:
        context['admin_data']=request.session['admin']
        return render(request,'main/index.html',context)
    elif 'artist' in request.session:
        context['user_data']=request.session['artist']
        return render(request,'main/index.html',context)
    return render(request,'main/index.html',context)

def Gallery(request):
    context = {}
    if request.GET:
        id = request.GET['id']
        sql = "select * from category_list"
        context['cat']=connections.selectall(sql)
        sql = "select * from post_list where cat_id='"+id+"'"
        post_details = connections.selectall(sql)
        context['post']=post_details
        if 'admin' in request.session:
            context['admin_data']=request.session['admin']
            return render(request,'main/gallery.html',context)
        elif 'artist' in request.session:
            context['user_data']=request.session['artist']
            return render(request,'main/gallery.html',context)
        else:
            return render(request,'main/gallery.html',context)
    return HttpResponseRedirect('error')

def post(request):
    context={}
    
    if request.session.keys():
        if request.GET.get('id'):
            id = request.GET['id']
            sql = "select * from category_list"
            context['cat']=connections.selectall(sql)
            sql = "select * from post_list where post_id='"+id+"'"
            post_details = connections.select(sql)
            context['post']=post_details
            sql = "select user_id from like_list where post_id='"+id+"'"
            post_like = connections.selectall(sql)
            likes_count=str(len(post_like))
            sql = "update post_list set likes='"+likes_count+"' where post_id='"+id+"'"
            connections.update(sql)
            context['likes']=likes_count
            if 'admin' in request.session:
                context['admin_data']=request.session['admin']
                if request.session['admin'][1] in post_like:
                    context['like'] = True
                else:
                    context['like'] = False
                return render(request,'main/post.html',context)
            elif 'artist' in request.session:
                context['user_data']=request.session['artist']
                if request.session['artist'][2] in post_like:
                    context['like'] = True
                else:
                    context['like'] = False
                return render(request,'main/post.html',context)
            else:
                return render(request,'main/post.html',context)
    
    return HttpResponseRedirect('Login')

def likePost(request):
    context={}
    if request.GET.get('id'):
        post_id = str(request.GET['id'])
        if 'artist' in request.session.keys():
            user_id = request.session['artist'][2]
        elif 'admin' in request.session.key():
            user_id = request.session['admin'][1]
        else:
            return HttpResponseRedirect('Login')
        sql = "select * from like_list where post_id='"+post_id+"' and user_id='"+user_id+"'"
        like = connections.select(sql)
        if like:
            sql = "delete from like_list where post_id='"+post_id+"' and user_id='"+user_id+"'"
            connections.delete(sql)
        else:
            sql = "insert into like_list(user_id,post_id)values('"+user_id+"','"+post_id+"')"
            connections.insert(sql)
        return HttpResponseRedirect('viewPost?id='+post_id)
    
def addComment(request):
    context={}
    if request.GET.get('post'):
        post_id = str(request.GET.get('post'))
        comment = request.GET.get('comment')
        if 'artist' in request.session.keys():
            user_id = request.session['artist'][2]
        elif 'admin' in request.session.key():
            user_id = request.session['admin'][1]
        else:
            return HttpResponseRedirect('Login')
        # Comment Check for spam
        sql = "select * from comments where user_id='"+user_id+"' and post_id='"+post_id+"' and comment='"+comment+"'"
        spam_check = connections.select(sql)

        if spam_check:
            return HttpResponseRedirect('viewPost?id='+post_id)
        else:
            sql = "insert into comments(post_id,user_id,comment,spam)values('"+post_id+"','"+user_id+"','"+comment+"','0')"
            connections.insert(sql)
            return HttpResponseRedirect('viewPost?id='+post_id)


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
                return render(request,'main/login.html',{'msg':"Registration Successful"})
    return render(request,'main/register.html')

def login(request):
    if 'admin' in request.session.keys():
        return HttpResponseRedirect('home')
    elif 'artist' in request.session.keys():
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
                    sql = "select * from artist_list where artist_id = '"+user_name+"'"
                    user_data = connections.select(sql)
                    request.session['artist']=user_data
                    return HttpResponseRedirect('home')
                elif user[2]=='admin':
                    request.session['admin']=user
                    return HttpResponseRedirect('administrator')
                elif user[2]=='user' and user[3]==1:
                    request.session['user']=user
                    return HttpResponseRedirect('home')
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
        sql = "select * from post_list where status=0"
        post_aprovals = connections.selectall(sql)
        context['post_len']=len(post_aprovals)
        context['posts']=post_aprovals
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

def aproveArtist(request):
    if request.session['admin']:
        id = request.GET.get('id')
        sql = "update logintb set status='1' where user_id='"+id+"'"
        connections.update(sql)
        sql = "update artist_list set status='1' where artist_id='"+id+"'"
        connections.update(sql)
        return HttpResponseRedirect('artistAprovals')
    return HttpResponseRedirect('error')

def denyArtist(request):
    if request.session['admin']:
        id = request.GET.get('id')
        sql = "update logintb set status='2' where user_id='"+id+"'"
        connections.update(sql)
        sql = "update artist_list set status='2' where artist_id='"+id+"'"
        connections.update(sql)
        return HttpResponseRedirect('artistAprovals')
    return HttpResponseRedirect('error')

def editGallery(request):
    if request.POST:
        cat_name=request.POST.get('cat')
        sql = "insert into category_list(name,posts)values('"+cat_name+"','0')"
        connections.insert(sql)
    context ={}
    if request.session['admin']:
        context['admin']=request.session['admin']
        sql = "select * from category_list"
        category_details = connections.selectall(sql)
        context['category']=category_details
        return render(request,'administrator/categoryEdit.html',context)
    return render(request,'error')

def postAp(request):
    context ={}
    if request.session['admin']:
        context['admin']=request.session['admin']
        sql = "select * from post_list where status=0"
        post_aprovals = connections.selectall(sql)
        context['aprovals']=post_aprovals
        return render(request,'administrator/postAprovals.html',context)
    return render(request,'error')

def aprovePost(request):
    if request.session['admin']:
        id = request.GET.get('id')
        sql = "update post_list set status='1' where post_id='"+id+"'"
        connections.update(sql)
        return HttpResponseRedirect('postAprovals')
    return HttpResponseRedirect('error')

def denyPost(request):
    if request.session['admin']:
        id = request.GET.get('id')
        sql = "update post_list set status='2' where post_id='"+id+"'"
        connections.update(sql)
        return HttpResponseRedirect('postAprovals')
    return HttpResponseRedirect('error')

# Artist

def artistHome(request):
    context ={}
    if request.session['artist']:
        context['artist']=request.session['artist']
        artist = request.session['artist']
        sql = "select * from post_list where artist_id='"+artist[2]+"'"
        context['data'] = connections.selectall(sql)
        return render(request,'artist/myGallery.html',context)
    
def editArtist(request):
    context ={}
    if request.session['artist']:
        id = request.session['artist'][2]
        context['artist']=request.session['artist']
        sql = "select * from artist_list where artist_id='"+id+"'"
        artist_details = connections.select(sql)
        context['details']=artist_details
        return render(request,'artist/editProfile.html',context)
    return render(request,'error')

def addPost(request):
    context={}
    if request.session['artist']:
        context['artist']=request.session['artist']
        artist_data = request.session['artist']
        sql = "select * from category_list"
        context['cat']=connections.selectall(sql)
        if request.POST:
            title = request.POST.get('title')
            cat = request.POST.get('cat')
            cat_id = connections.select("select cat_id from category_list where name='"+cat+"'")
            cat_id = str(cat_id[0])
            fs = FileSystemStorage()
            image = request.FILES['img']
            image_name = artist_data[1]+str(randint(1,10000))+image.name
            sql = "insert into post_list(file_name,artist_name,artist_id,category,cat_id,status,title)values('"+image_name+"','"+artist_data[1]+"','"+artist_data[2]+"','"+cat+"','"+cat_id+"','0','"+title+"')"
            connections.insert(sql)
            fs.save("artist/uploads/"+image_name,image)
            return HttpResponseRedirect('artistHome')
        return render(request,'artist/addPost.html',context)

# Error Page
def error(request):
    return render(request,'404_error.html')

def test(request):
    sql = "select * from category_list"
    cat_id=2
    sql = "insert into test(new_id)values('"+cat_id+"')"
    connections.insert(sql)
    return render(request,'test.html',{'admin':admin})
