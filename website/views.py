from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import Friends, ResourceLink, VideoLink, Student, Bucket, Scholarship, Messages
from .serializers import MessageSerializer
from .forms import ResourceForm, VideoForm, addBucket, addScholarship, CustomAuthenticate, CustomCreate
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from statistics import mean
import ast

def helper_login(request, username, password):
    """
    helper function to authenticate user given username and password
    """
    user = authenticate(request, username=username, password=password)
    login(request, user)
    

def new_login(request):
    """
    view that authenticates login. this is the default view upon entering the website
    """
    if len(Bucket.objects.all()) == 0: 
                Bucket().save() #this initializes a single bucket object that has the initial categories. required to stop website from crashing on the first time it's run

    form = CustomAuthenticate

    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html', {"form": form, "info": "Succesfully logged in"})
        else:
            return render(request, 'index.html', {"form":form, "error": "Invalid username or password"})
    else:
        return render(request, 'index.html', {"form": form})

def newsignup(request):
    """
    view that creates new user. called when sign up button pressed in original login page
    """ 
    if request.method=="POST": 
        username = request.POST.get('username')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        grade = request.POST.get('grade')
        nk_id = request.POST.get('nk_id')
        if password == password2: 
            
            try: #create student object from user
                save_user = User.objects.create_user(username, password=password)
                student_user = Student(user=save_user, username=username, resource_rating={}, seen_resource={}, grade=grade, nk_id=nk_id)
                save_user.save()
                student_user.save()
                helper_login(request, username, password)
            except IntegrityError: #except user is already in the database. Note: Integrity error is not case sensitive
                return render(request, 'index.html', {"form": CustomCreate, "error":"The username " + username + " already exists"})                    
            
            #user is unique
            return render(request, 'index.html', {"form": CustomCreate, "info":"The user " + username + " is created succesfully"})

        else: #passwords don't match
            return render(request, 'index.html', {"form": CustomCreate, "error":"The passwords are not matching"})
    
    else: #if form is not being submitted
        return render(request, 'index.html', {"form": CustomCreate}) #this is going to be the signup form

@csrf_exempt
def resources(request):
    user = Student.objects.get(user=request.user.id)
    seen = ast.literal_eval(user.seen_resource)
    

    if request.is_ajax(): #recieve rating submitted by user
        seen = ast.literal_eval(user.seen_resource)
        user.points += 10 #point system was created such that users would get points from clicking links. This is currently not shown in the website, but the infrastucture for it exists
        
        rating = request.POST.get('rating')
        category = request.POST.get('category')
        title = request.POST.get('title')
        
        try:
            int(rating) #should throw error if star isnt chosen

            existing = ast.literal_eval(user.resource_rating) #find list of existing resource ratings by user
            
            res_obj = ResourceLink.objects.filter(title=title.strip()).first() #get Resource object chosen
            res_existing = ast.literal_eval(res_obj.rating) #get existing ratings for that object
            res_existing.append(int(rating)) #add current rating to that list
            res_obj.rating = res_existing
            res_obj.save()

            if category not in existing: #add category to resource rating list if it doesn't exist
                existing[category] = []
            existing[category].append(rating)
            user.resource_rating = existing

            
            seen[title.strip()] = rating #append {title: rating} to seen dictionary
            user.seen_resource = seen #the seen resources attribute is currently not used (except to find a Nanhi Kali's favourite resourceS) but can be used in future as part of a resource filtering system

            user.save()
        except ValueError: 
            pass
    
    """
    Return list of resources
    """
    try:
        topics = [x.capitalize() for x in ast.literal_eval(Bucket.objects.all().first().buckets)]
    except AttributeError:
        Bucket().save() #create new Bucket object
        topics = [x.capitalize() for x in ast.literal_eval(Bucket.objects.all().first().buckets)]


    initialization = ['' for _ in range(len(topics))]
    information_dict = dict(zip(topics, initialization)) #initialize empty dictionary with keys being topic names
    #TODO: For the user, each category should have a list for its ratings
    #TODO: Each resource should have the total ratings of it
    
    favorites = [k if int(v)>4 else 0 for k,v in seen.items()] #all resources rated higher than 4 stars get added to the favourites list
    favorites = list(filter(lambda a: a != 0, favorites))
    favorites = [ResourceLink.objects.filter(title=x).first() for x in favorites]


    for i in topics:
        information_dict[i] = ResourceLink.objects.filter(topic=i.lower()) #add list of resources for a specific topic to dictionary. So dictionary is of the form {topic1: [resource1, resource 2]...}
    
    all_information = {}

    all_information['resources'] = list(information_dict.items())


    all_information['person'] = user
    all_information['favorites'] = favorites

    return render(request, 'resources.html',all_information) 

def talks(request):
    """
    Return videos
    """
    user = Student.objects.get(user=request.user.id)
    video = VideoLink.objects.all()
    return render(request, 'videos.html', {'videos':video, "person":user})

def connection(request):
    """
    Return connection page
    """
    return render(request, 'connection.html')

def scholarship(request):
    """
    Return scholarship page
    """
    user = Student.objects.get(user=request.user.id)
    scholarships = Scholarship.objects.all()
    return render(request, 'scholarship.html', {"person":user, "scholarships":scholarships})


def personal(request):
    """
    This was meant to be a personalized page created for each user that would display their interests and points. It is currently used just to display a logout option
    """
    user = Student.objects.get(user=request.user.id)
    ratings = ast.literal_eval(user.resource_rating)
    mean_ratings = {k: mean([int(x) for x in v]) for k,v in ratings.items()}
    sorted_mean_ratings = {k: v for k, v in sorted(mean_ratings.items(), key=lambda item: item[1], reverse=True)} 
    return render(request, 'personal.html', {"person": user, "ratings": sorted_mean_ratings.items()})


def admin(request):
    """
    View that returns the admin page which allows an admin to add/delete resources, videos, and scholarships
    """
    form = addScholarship()
    resource = ResourceForm()
    video = VideoForm()
    bucket = addBucket()
    current_buckets = ", ".join(ast.literal_eval(Bucket.objects.all().first().buckets)) #get current topics
    all_resources = ResourceLink.objects.all()
    all_videos = VideoLink.objects.all()
    all_schols = Scholarship.objects.all()
    if request.method == 'POST':
        data = request.POST
        if 'resourceSubmit' in data: #add resource
            title = data['title']
            link = data['link'].strip()
            topic = data['topic'].strip().lower()
            new_resource = ResourceLink(title=title, link=link, topic=topic)
            new_resource.save()
        elif 'videoSubmit' in data: #add video
            name = data['name']
            link = data['link']
            link = link.replace('watch?v=','embed/')
            new_video = VideoLink(name=name, link=link)
            new_video.save()
        elif 'bucketSubmit' in data: #add topic
            bucket_obj = Bucket.objects.all().first()
            bucket_names = ast.literal_eval(bucket_obj.buckets)
            name = data['bucket'].strip().lower().capitalize()
            bucket_names.append(name)
            bucket_obj.buckets = bucket_names
            bucket_obj.save()
        elif 'scholSubmit' in data: #add scholarship
            name = data['name']
            link = data['link']
            description = data['description']
            obj = Scholarship(name=name, link=link, description=description)
            obj.save()
    info_dict = {'resource': resource, 'video':video, 'bucket':bucket, "current": current_buckets}
    info_dict['form'] = form
    info_dict['all_resources'] = all_resources
    info_dict['all_videos'] = all_videos
    info_dict['all_schols'] = all_schols
    return render(request, 'admin.html', info_dict)

def delete(request):
    if request.method == "POST":
        if "deleteResources" in request.POST:
            resc_vals = request.POST.getlist("resc")
            [ResourceLink.objects.filter(title=i).delete() for i in resc_vals]
        elif 'deleteVideo' in request.POST:
            resc_vals = request.POST.getlist("resc")
            [VideoLink.objects.filter(name=i).delete() for i in resc_vals]
        elif 'deleteSchol' in request.POST:
            resc_vals = request.POST.getlist("resc")
            [Scholarship.objects.filter(name=i).delete() for i in resc_vals]
    return admin(request)

def logout_web(request):
    """
    logout
    """
    logout(request)
    return new_login(request)

def popular_resources(request):
    """
    View to evaluate and show the most popular resources
    """
    order = ResourceLink.objects.all()
    mean_list = {x.title : mean(ast.literal_eval(x.rating)) for x in order}
    ordered_resources = dict(sorted(mean_list.items(), key=lambda item: item[1],reverse=True)) #order in decreased order
    output = "\n".join([a + " : " + str(b) for a,b in ordered_resources.items()])
    return render(request, "analysis.html", {"resources": output})

def getFriendsList(id):
    """
    Get the list of friends of the  user
    """
    try:
        user = Student.objects.get(id=id)
        ids = list(user.friends_set.all())
        friends = []
        for id in ids:
            num = str(id)
            fr = Student.objects.get(id=int(num))
            friends.append(fr)
        return friends
    except:
        return []


def getUserId(username):
    """
    Get the user id by the username
    """
    use = Student.objects.get(username=username)
    id = use.id
    return id

def connection(request):
    username = request.user.username
    id = getUserId(username)
    friends = getFriendsList(id)
    return render(request, 'connection.html', {"friends":friends})

def friends_list():
    allFriends = Friends.objects.all()
    all_str = []
    for x in allFriends:
        person = x.user.username
        friends = getFriendsList(getUserId(person))
        friends = [x.username for x in friends]
        friend_str = person + ' : ' + ', '.join(friends)
        all_str.append(friend_str)
    return all_str

def search(request):
    """
    Search users page
    """
    users = list(Student.objects.exclude(username=request.user.username))
    existing = "\n".join(friends_list())

    if request.method == "POST":
        query = request.POST.get("search")
        user_ls = []
        for user in users:
            if query in user.username:
                user_ls.append(user)
        return render(request, "search.html", {'users': user_ls, })

    try:
        users = users[:10]
    except:
        users = users[:]
    id = getUserId(request.user.username)
    friends = getFriendsList(id)
    return render(request, "search.html", {'users': users, 'friends': friends, 'existing': existing})


def get_other(request, name):
    """
    Part of the friend search funcionality. View to find the other person in the create connection admin page
    """
    users = list(Student.objects.exclude(username=request.user.username).exclude(username=name))
    try:
        users = users[:10]
    except:
        users = users[:]
    
    if request.method == "POST":
        query = request.POST.get("search")
        user_ls = []
        for user in users:
            if query in user.username:
                user_ls.append(user)
        return render(request, "search2.html", {'users': user_ls, 'name':name})
    return render(request, "search2.html", {'users': users, 'name':name})


def addFriend(request, name1, name2):
    """
    Add a user to the friend's list
    """
    print(name1)
    print(name2)
    curr_user = Student.objects.get(username=name1)
    username = curr_user.username
    id = getUserId(username)
    friend = Student.objects.get(username=name2)
    # print(curr_user.name)
    ls = curr_user.friends_set.all()
    flag = 0
    for username in ls:
        if username.friend == friend.id:
            flag = 1
            break
    if flag == 0:
        print("Friend Added!!")
        curr_user.friends_set.create(friend=friend.id)
        friend.friends_set.create(friend=id)
    return redirect("/website/")

def chat(request, username):
    """
    Get the chat between two users.
    """
    friend = Student.objects.get(username=username)
    id = getUserId(request.user.username)
    curr_user = Student.objects.get(id=id)
    messages = Messages.objects.filter(sender_name=id, receiver_name=friend.id) | Messages.objects.filter(sender_name=friend.id, receiver_name=id)

    if request.method == "GET":
        friends = getFriendsList(id)
        return render(request, "messages.html",
                      {'messages': messages,
                       'friends': friends,
                       'curr_user': curr_user, 'friend': friend})



@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == 'GET':
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.seen = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)