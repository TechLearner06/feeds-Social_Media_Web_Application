from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User 
from .models import Profile,Post,LikePost,FollowersList,Comment
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from itertools import chain
import random



# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already taken")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                
                # Manually create a profile for the new user
                Profile.objects.create(user=user)

                # Authenticate and log in the user
                user_login = authenticate(request, username=username, password=password)
                if user_login is not None:
                    login(request, user_login)

                return redirect('edit_profile')
                  
        else:
            messages.info(request, "Password did not match")
            return redirect('signup')
    else:
        return render(request, 'registration.html')



def loginPage(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                return redirect('admin/')
            else:
                login(request, user)
                return redirect('index')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')



@login_required
def feeds(request):
    profile = request.user.profile

    #These lists are initialized to store 
    
    user_following_list=[]  #the users the logged-in user is following
    feed=[]  #the posts from these users.
    

    #Get the List of Users the Logged-in User is Following
    user_following_relations = FollowersList.objects.filter(follower=request.user.id)  # imagine i am the user i am following three peoples so my id will be in the followers table under the follower column of these three peoples.

    #Here, the code iterates through the user_following_list (which currently contains FollowersList objects) and appends the actual user objects (i.e., the users that the logged-in user is following) to the same list.
    for relation in user_following_relations:
        user_following_list.append(relation.following_user)

    

    #In this loop, the code iterates through the user_following_list (now containing user objects). For each user, it fetches their posts from the Post model. The fetched posts (feed_lists) are then appended to the feed list.
    for user in user_following_list:
        feed_lists = Post.objects.filter(user=user)
        feed.append(feed_lists)

    user_posts = Post.objects.filter(user=request.user)
    feed.append(user_posts)

    

    #Flattening a list means converting a list of lists into a single list containing all the elements. In this context, flattening is used to take the list of posts from multiple users and combine them into a single list of posts, which can then be displayed as a unified feed.

    feed_list = list(chain(*feed))


    #user-suggestions
    all_users=User.objects.all().exclude(is_staff = True)#This variable likely contains a list of all users on your social media platform.
    user_following =[]


    for user in user_following_relations:
        user_list=User.objects.get(followers=user.id)
        user_following.append(user_list)

    #users not following yet  also we have to exclude the login user
    new_suggestions = [ x for x in list(all_users) if (x not in list(user_following))]
    login_user = User.objects.filter(username=request.user.username)
    user_suggestion =[ x for x in list(new_suggestions) if (x not in list(login_user))]

    # random user suggestions - refresh option
    #we are only showing 5 or 4 out of the all users 
    random.shuffle(user_suggestion)
    #Limit the number of suggestions to 5:
    limit_user_suggestions=user_suggestion[:5]


    # now we have to access the profile object of each of the list

    
    user_suggest_profile_list=[]

    for users in limit_user_suggestions:
        suggest_profile_lists=Profile.objects.filter(user_id=users.id)
        user_suggest_profile_list.append(suggest_profile_lists)

        final_list=list(chain(*user_suggest_profile_list))


    
    return render(request, 'index.html',{'profile': profile,'posts':feed_list,'final_list':final_list})


@login_required
def profile(request, user_id):
    
    user_object=User.objects.get(id=user_id)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=user_object)
    user_post_len = user_posts.count()

    
    follower=request.user.id #user_id of the logged in user
    following_user=user_id #user_id of the profile being followed

    if FollowersList.objects.filter(follower=follower,following_user=following_user).first():
        button_text='following'
    else:
        button_text='follow'


    no_of_following= len(FollowersList.objects.filter(follower=user_id))  # imagine i am the one logging in and select a profile to follow(user2) here i am the follower and the user2 is being followed,This gives the number of users that user_id is following.
    no_of_followers = len(FollowersList.objects.filter(following_user=user_id))  #  This gives the number of followers the user_id has.



    context={
        'user_object':user_object,
        'user_profile' : user_profile,
        'user_posts':user_posts,
        'user_post_len':user_post_len,
        'button_text' : button_text,
        'no_of_followers' : no_of_followers,
        'no_of_following' : no_of_following,
    }

    return render(request, 'profile.html',context)



@login_required
def edit_profile(request):
    if request.method == "POST":
        #Get data from the form
        username=request.POST['username']
        name=request.POST['name']
        profile_img=request.FILES.get('profile_img')
        bio=request.POST['bio']
        gender=request.POST['gender']
        

        user=request.user
        profile = request.user.profile


        # Check if the username is being changed and if it is unique
        if username and username != user.username:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('edit_profile')
        
        # Update user information
        if username:
            user.username = username
        user.save()
        
        #update profile information
        profile.name=name
        profile.bio=bio
        profile.gender=gender
        if profile_img:
            profile.profile_img = profile_img
        profile.save()

        return redirect('index')
    
    
    else:
        user=request.user
        profile = request.user.profile  # Fetch the profile using the user


        context = {
            'user':user,
            'profile': profile
        }
    
        return render(request,"account_settings.html",context)


def privacy_settings(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to prevent logging out the user
            messages.success(request, 'Your password was successfully updated!')
            return redirect('privacy_settings')
        else:
            messages.error(request,"password did not match")
            return redirect('privacy_settings')
        
    else:  
        form=PasswordChangeForm(request.user)

        return render(request,"privacy_settings.html",{'form':form})

@login_required
def upload_post(request):

    if request.method == "POST":
        user=request.user
        post_image=request.FILES.get('image')
        video=request.FILES.get('video')
        caption=request.POST['caption']
        location=request.POST['location']


        new_post = Post.objects.create(user=user , image=post_image , video=video, caption = caption,location = location)
        
        if new_post:
            new_post.save()
            return redirect("index")
        else:
            messages.error(request,"There is some issue!..Try Again")
            return redirect("add_posts")

    else:
        
        return render(request,"addposts.html")



@login_required
def like_post(request):
    user=request.user
    post_id = request.GET.get('post_id')
    

    post = Post.objects.get(id=post_id)

    #to check if the user already liked the post or not

    like_filter=LikePost.objects.filter(post=post,user=user).first()
    if like_filter == None:
        new_like=LikePost.objects.create(post=post , user=user)
        new_like.save()
        post.no_of_likes +=1
        post.save()
        return redirect('index')
        
        
    else:
        like_filter.delete()
        post.no_of_likes -=1
        post.save()
        return redirect('index')
    


@login_required
def follow(request):
    if request.method == "POST":
        follower_id=request.POST.get('follower') #The user who is following someone
        user_id=request.POST.get('user') #The user being followed


        #retrieve user objects based on username
        follower = User.objects.get(id=follower_id)
        user = User.objects.get(id=user_id)

       
        # Check if the follower is already following the user
        if FollowersList.objects.filter(follower=follower,following_user=user).first():
            # If already following, un follow (delete the relationship)
            delete_follower = FollowersList.objects.get(follower=follower,following_user=user)
            delete_follower.delete()
             # Redirect to the profile page of the user with user_id
            return redirect('/profile/{}'.format(user_id))
           
           
        else:
            #new follower

            new_follower= FollowersList.objects.create(follower=follower,following_user=user)
            new_follower.save()
             # Redirect to the profile page of the user with user_id
            return redirect('/profile/{}'.format(user_id))
            

            

    else:
         # Redirect to the profile page of the user with user_id
        return redirect('/profile/{}'.format(user_id))
    


def view_followers(request,user_id):
    user=User.objects.get(id=user_id)
    followers_list=FollowersList.objects.filter(following_user=user)
    following_user_list=FollowersList.objects.filter(follower=user)


    context={
        'user_profile':user.profile,
        'followers_list':followers_list,
        'following_user_list':following_user_list,
    }

    return render(request,"friendslist.html",context)
    


@login_required
def postComments(request,post_id):
    post=Post.objects.get(id=post_id)
    comments=Comment.objects.filter(post=post).order_by(".date")

    if request.method == 'POST':
        user=request.user
        content=request.POST.get('content')

        if content:

            new_comment=Comment.objects.create(post=post,user=user,content=content)
            new_comment.save()
            return redirect('post_comments', post_id=post_id)
        else:
            return render(request, 'index.html', {  # Use your actual template file name here
                'post': post,
                'comments': comments,
                'error': 'Content is required.'
            })
    
    return render(request,'index.html',{'post':post,'comments':comments})



@login_required
def search(request):
    #This part fetches the logged-in user's object and their associated profile.
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)

    if request.method == 'POST':
        # fetching the search content
        search_content=request.POST.get('search-content')

        if search_content:
            search_user=User.objects.filter(username__icontains=search_content).exclude(is_staff=True) #The icontains lookup in Django's ORM is used to perform case-insensitive containment tests. When you use icontains, you're essentially checking if a certain substring exists within a field's value, ignoring case sensitivity.

            
            search_user_profile_list =[]

            #This loops through the found users and collects their IDs.
            #This loops through the collected user IDs and fetches profiles associated with those user IDs. 
            for users in search_user:
                profile_lists=Profile.objects.filter(user_id=users.id)
                search_user_profile_list.append(profile_lists)
            

            #It then flattens the list of profile querysets into a single list using chain.
            search_user_profile_list = list(chain(*search_user_profile_list))
                
            return render(request, "search.html", {
                'user_profile': user_profile,
                'search_user_profile_list': search_user_profile_list,
                'search_content': search_content
            })  

        else:
            # If no search content is provided, redirect to the same page or another page
            return redirect('index') 


    return render(request,"search.html",{'user_profile':user_profile})


@login_required
def delete_post(request,post_id):
    post=Post.objects.get(id=post_id)

    if request.user==post.user:
        post.delete()
    

    return redirect('/profile/{}'.format(request.user.id))

    
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')











