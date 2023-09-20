from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import connections
from django.core.files.storage import FileSystemStorage
from random import randint

# Create your views here.

# Home

def home(request):
    context = {}
    # Category Select For navbar
    sql = "select * from category_list"
    context['cat']=connections.selectall(sql)
    # Top 3 Liked
    sql = "select * from post_list where status='1' order by likes desc"
    top_likes = connections.selectall(sql)
    # home Page Posts
    sql = "select * from post_list where status='1'"
    context['posts']=connections.selectall(sql)
    if len(top_likes)>3:
        context['top_like']=top_likes[0:3]
    else:
        context['top_like']=top_likes
    # Initializing Posts in a Category
    for i in context['cat']:
        p=0
        for j in context['posts']:
            if i[0]==j[5]:
                p+=1
        p = str(p)        
        sql="update category_list set posts='"+p+"' where cat_id='"+str(i[0])+"'"
        connections.update(sql)
    if 'admin' in request.session:
        context['admin_data']=request.session['admin']
        return render(request,'main/index.html',context)
    elif 'artist' in request.session:
        context['user_data']=request.session['artist']
        return render(request,'main/index.html',context)
    elif 'user' in request.session:
        context['user_data']=request.session['user']
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
        elif 'user' in request.session:
            context['user_data']=request.session['user']
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
            # Updating Likes Count
            sql = "select user_id from like_list where post_id='"+id+"'"
            post_like = connections.selectall(sql)
            likes_count=str(len(post_like))
            sql = "update post_list set likes='"+likes_count+"' where post_id='"+id+"'"
            connections.update(sql)
            # Updating Comments Count
            sql = "select * from comments where post_id='"+id+"'"
            comments = connections.selectall(sql)
            context['comments']=comments
            comment_count=str(len(comments))
            sql = "update post_list set comments='"+comment_count+"' where post_id='"+id+"'"
            connections.update(sql)

            context['likes']=likes_count
            sql = "select * from artist_list where artist_id='"+post_details[3]+"'"
            artist_data=connections.select(sql)
            context['artist_data']=artist_data
            if 'admin' in request.session:
                context['admin_data']=request.session['admin']
                if request.session['admin'][1] in post_like:
                    context['like'] = True
                else:
                    context['like'] = False
                return render(request,'main/post.html',context)
            elif 'artist' in request.session:
                context['user_data']=request.session['artist']
                if request.session['artist'][1] in post_like:
                    context['like'] = True
                else:
                    context['like'] = False
                return render(request,'main/post.html',context)
            elif 'user' in request.session:
                context['user_data']=request.session['user']
                if request.session['user'][1] in post_like:
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
            user_id = request.session['artist'][1]
        elif 'admin' in request.session.keys():
            user_id = request.session['admin'][1]
        elif 'user' in request.session.keys():
            user_id = request.session['user'][1]
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
            user_id = request.session['artist'][1]
        elif 'admin' in request.session.keys():
            user_id = request.session['admin'][1]
        elif 'user' in request.session.keys():
            user_id = request.session['user'][1]
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
            return HttpResponseRedirect('http://127.0.0.1:8000/viewPost?id='+post_id)

def spamComment(request):
    context={}
    if request.GET.get('comment_id'):
        comment_id = request.GET.get('comment_id')
        post_id=request.GET.get('post_id')
        if 'artist' in request.session.keys():
            user_id = request.session['artist'][1]
        elif 'admin' in request.session.keys():
            user_id = request.session['admin'][1]
        elif 'user' in request.session.keys():
            user_id = request.session['user'][1]
        else:
            return HttpResponseRedirect('Login')
        sql = "select * from commentSpam where comment_id='"+comment_id+"' and user_id='"+user_id+"'"
        spam_check = connections.select(sql)
        if spam_check:
            return HttpResponseRedirect('viewPost?id='+post_id)
        else:
            sql = "insert into commentSpam(comment_id,user_id)values('"+comment_id+"','"+user_id+"')"
            connections.insert(sql)
            sql = "update comments set spam=spam+1 where id='"+comment_id+"'"
            connections.update(sql)
            return HttpResponseRedirect('viewPost?id='+post_id)
        
def ArtistsList(request):
    context={}
    sql = "select * from post_list where status='1'"
    post_data = connections.selectall(sql)
    sql = "select artist_id from artist_list"
    artists_data= connections.selectall(sql)
    for artist in artists_data:
        counter = 0
        for post in post_data:
            if artist[0]==post[3]:
                counter+=1
        sql = "update artist_list set posts='"+str(counter)+"' where artist_id='"+artist[0]+"'"
        connections.update(sql)
    sql = "select * from artist_list"   
    context['artist_data']=connections.selectall(sql)
    if 'admin' in request.session:
        context['admin_data']=request.session['admin']
        return render(request,'main/artists.html',context)
    elif 'artist' in request.session:
        context['user_data']=request.session['artist']
        return render(request,'main/artists.html',context)
    elif 'user' in request.session:
        context['user_data']=request.session['user']
        return render(request,'main/artists.html',context)
    else:
        return HttpResponseRedirect('error')
    
    
# Registration and login

def register(request):
    if request.POST:
        if request.POST.get("submit")=="artist":
            if request.POST.get("password")==request.POST.get("c_password"):
                name = request.POST.get("name")
                id = request.POST.get("artist_id")
                sql = "select artist_id from artist_list where artist_id='"+id+"'"
                check_id = connections.select(sql)
                if check_id:
                    return render(request,'main/register.html',{'error':"Id Already Exits"})
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
            
        elif request.POST.get("submit")=="user":
            if request.POST.get("password")==request.POST.get("c_password"):
                name = request.POST.get("name")
                id = request.POST.get("user_id")
                sql = "select user_id from user_list where user_id='"+id+"'"
                check_id = connections.select(sql)
                if check_id:
                    return render(request,'main/register.html',{'error':"Id Already Exits"})
                email = request.POST.get("email")
                contact = request.POST.get("contact")
                gender = request.POST.get("gender")
                password = request.POST.get("password")
                image_name="blank-profile-picture-973460_1280.png"
                sql = "insert into user_list(name,user_id,email,password,contact,profile_pic,gender,status)values('"+name+"','"+id+"','"+email+"','"+password+"','"+contact+"','"+image_name+"','"+gender+"','1')"
                connections.insert(sql)
                sql = "insert into logintb(user_id,user_type,status,password)values('"+id+"','user','1','"+password+"')"
                connections.insert(sql)
                return render(request,'main/login.html',{'msg':"Registration Successful"})
    return render(request,'main/register.html')

def login(request):
    if 'admin' in request.session.keys():
        return HttpResponseRedirect('home')
    elif 'artist' in request.session.keys():
        return HttpResponseRedirect('home')
    elif 'user' in request.session.keys():
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
                    return HttpResponseRedirect('home')
                elif user[2]=='admin':
                    request.session['admin']=user
                    return HttpResponseRedirect('administrator')
                elif user[2]=='user':
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
    elif 'user' in request.session.keys():
        del request.session['user']
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
    
def adminEdit(request):
    context={}
    uid = request.session['admin'][1]
    sql = "select * from logintb where user_id='"+uid+"'"
    context['details']=connections.select(sql)
    sql = "select * from logintb where user_id='"+uid+"'"
    context['admin']=connections.select(sql)
    if request.POST:
        if request.POST.get("password")==request.POST.get("c_password"):
            id = request.POST.get("id")
            if id!=uid:
                sql = "select user_id from logintb where user_id='"+id+"'"
                check_id = connections.select(sql)
                if check_id:
                    context['error']="User ID Already Exists"
                    return render(request,'administrator/editDetails.html',context)
            password = request.POST.get("password")
            sql = "update logintb set user_id='"+id+"',password='"+password+"' where user_id='"++"'"
            connections.update(sql)
            return HttpResponseRedirect('adminEdit')
    sql = "select * from logintb where user_id='"+uid+"'"
    context['details']=connections.select(sql)
    sql = "select * from logintb where user_id='"+uid+"'"
    context['admin']=connections.select(sql)
    return render(request,'administrator/editDetails.html',context)

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

def artistList(request):
    context ={}
    if request.session['admin']:
        context['admin']=request.session['admin']
        sql = "select * from artist_list"
        artist_list = connections.selectall(sql)
        context['artist_list']=artist_list
        return render(request,'administrator/artistList.html',context)
    return render(request,'error')

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
        print(category_details)
        context['category']=category_details
        return render(request,'administrator/categoryEdit.html',context)
    return render(request,'error')

def delCat(request):
    context={}
    if request.session['admin']:
        if request.GET.get('id'):
            did = request.GET.get('id')
            sql = "select posts from category_list where cat_id='"+did+"'"
            post_check = connections.select(sql)
            
            if post_check[0]>0:               
                context['admin']=request.session['admin']
                sql = "select * from category_list"
                category_details = connections.selectall(sql)
                context['category']=category_details
                context['msg']="Cannot Delete Categories containing posts"
                return render(request,'administrator/categoryEdit.html',context)
            else:
                sql = "delete from category_list where cat_id='"+did+"'"
                connections.delete(sql)
                return HttpResponseRedirect('editGallery')

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
        id = request.session['artist'][1]
        sql = "select * from artist_list where artist_id='"+id+"'"
        context['artist']=connections.select(sql)
        sql = "select * from post_list where artist_id='"+id+"'"
        context['data'] = connections.selectall(sql)
        return render(request,'artist/myGallery.html',context)

def artistProfile(request):
    context={}
    if request.GET.get('id'):
        id = request.GET.get('id')
        sql = "select * from category_list"
        context['cat']=connections.selectall(sql)
        sql = "select * from post_list where artist_id='"+id+"' and status='1'"
        gallery = connections.selectall(sql)
        context['gallery']=gallery
        context['len_gallery']=len(gallery)
        sql = "select * from artist_list where artist_id='"+id+"'"
        artist_data = connections.select(sql)
        context['artist_data']=artist_data
        if 'admin' in request.session:
            context['admin_data']=request.session['admin']
            return render(request,'artist/myProfile.html',context)
        elif 'artist' in request.session:
            context['user_data']=request.session['artist']
            return render(request,'artist/myProfile.html',context)
        elif 'user' in request.session:
            context['user_data']=request.session['user']
            return render(request,'artist/myProfile.html',context)
        else:
            return render(request,'artist/myProfile.html',context)
    else:
        return HttpResponseRedirect('error')
    
    
def editArtist(request):
    context ={}
    uid = request.session['artist'][1]
    if request.session['artist']:
        if request.POST:
            name = request.POST.get("name")
            id = request.POST.get("artist_id")
            if id != uid:
                sql = "select user_id from logintb where user_id='"+id+"'"
                check_id = connections.select(sql)
                if check_id:
                    context['msg']="ID already exists"
                    sql = "select * from artist_list where artist_id='"+request.session['artist'][1]+"'"
                    user_details = connections.select(sql)
                    context['details']=user_details
                    return render(request,'artist/editProfile.html',context)
            email = request.POST.get("email")            
            contact = request.POST.get("contact")
            password = request.POST.get("password")
            if request.POST.get('img'):
                fs = FileSystemStorage()
                image = request.FILES['img']
                image_name = id+str(randint(1,10000))+image.name
                fs.save("user/profile_pic/"+image_name,image)
                sql = "update artist_list set name='"+name+"',user_id='"+id+"',email='"+email+"',contact='"+contact+"',password='"+password+"',profile_pic='"+image_name+"' where user_id='"+uid+"' "
                connections.update(sql)
            else:
                sql = "update artist_list set name='"+name+"',user_id='"+id+"',email='"+email+"',contact='"+contact+"',password='"+password+"' where user_id='"+uid+"' "
                connections.update(sql)           
            sql = "update logintb set user_id='"+id+"',password='"+password+"' where user_id='"+uid+"' "
            connections.update(sql)
            sql = "select * from logintb where user_id='"+id+"'"
            user = connections.select(sql)
            request.session['artist']=user
            context['msg']="updated"
        sql = "select * from artist_list where artist_id='"+request.session['artist'][1]+"'"
        data = connections.select(sql)
        context['artist']=data
        sql = "select * from artist_list where artist_id='"+request.session['artist'][1]+"'"
        user_details = connections.select(sql)
        context['details']=user_details
        return render(request,'artist/editProfile.html',context)
    return render(request,'error')

def addPost(request):
    context={}
    if request.session['artist']:
        id = request.session['artist'][1]
        sql = "select * from artist_list where artist_id='"+id+"'"
        context['artist']=connections.select(sql)
        artistid = request.session['artist'][1]
        sql = "select * from artist_list where artist_id='"+artistid+"'"
        artist_data = connections.select(sql)
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
    
def adminContact(request):
    context ={}   
    if request.session['artist']:
        id = request.session['artist'][1]
        sql = "select * from artist_list where artist_id='"+id+"'"
        context['artist']=connections.select(sql)
        reciever = "Asura"
        if request.POST:
            content = request.POST.get('msg')
            sql = "insert into messages_table(sender_id,reciever_id,content,status)values('"+id+"','"+reciever+"','"+content+"','0')"
            connections.insert(sql)      
        sql = "select content from messages_table where sender_id='"+id+"' and reciever_id='"+reciever+"'"
        context['messages'] = connections.selectall(sql)
        return render(request,'artist/adminContact.html',context)

# User

def userHome(request):
    context={}
    try:
        if request.session['user']:
            sql = "select * from user_list where user_id='"+request.session['user'][1]+"'"
            user_data = connections.select(sql)
            context['user']=user_data
            sql = "select post_id from like_list where user_id='"+request.session['user'][1]+"'"
            like_posts=connections.selectall(sql)
            liked_list=[] 
            for id in like_posts:
                sql = "select * from post_list where post_id='"+id[0]+"'"
                get = connections.select(sql)
                liked_list.append(get)
            print(liked_list)
            context['data']=liked_list
            return render(request,'user/index.html',context)
    except:
        return render(request,'main/login.html')

def editUser(request):
    context ={}
    uid = request.session['user'][1]
    if request.session['user']:
        if request.POST:
            name = request.POST.get("name")
            id = request.POST.get("user_id")
            if id != uid:
                sql = "select user_id from logintb where user_id='"+id+"'"
                check_id = connections.select(sql)
                if check_id:
                    context['msg']="userid already exists"
                    sql = "select * from user_list where user_id='"+request.session['user'][1]+"'"
                    user_details = connections.select(sql)
                    context['details']=user_details
                    return render(request,'user/editProfile.html',context)
            email = request.POST.get("email")            
            contact = request.POST.get("contact")
            password = request.POST.get("password")
            if request.POST.get('img'):
                fs = FileSystemStorage()
                image = request.FILES['img']
                image_name = id+str(randint(1,10000))+image.name
                fs.save("user/profile_pic/"+image_name,image)
            else:
                image_name="blank-profile-picture-973460_1280.png"
            sql = "update user_list set name='"+name+"',user_id='"+id+"',email='"+email+"',contact='"+contact+"',password='"+password+"',profile_pic='"+image_name+"' where user_id='"+uid+"' "
            connections.update(sql)
            sql = "update logintb set user_id='"+id+"',password='"+password+"' where user_id='"+uid+"' "
            connections.update(sql)
            sql = "select * from logintb where user_id='"+id+"'"
            user = connections.select(sql)
            request.session['user']=user
            context['msg']="updated"
        sql = "select * from user_list where user_id='"+request.session['user'][1]+"'"
        data = connections.select(sql)
        context['user']=data
        sql = "select * from user_list where user_id='"+request.session['user'][1]+"'"
        user_details = connections.select(sql)
        context['details']=user_details
        print(uid)
        return render(request,'user/editProfile.html',context)
    return render(request,'error')

# Error Page
def error(request):
    return render(request,'404_error.html')

def test(request):
    if request.session['user']:
        print("ok")
