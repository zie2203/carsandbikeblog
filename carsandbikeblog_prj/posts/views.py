from django.shortcuts import render,get_object_or_404,redirect
from .models import postsm,Reviews#import postsm models file
from .forms import MyLoginForm,UserRegistrationForm,PostAddForm,PostEditForm,ReviewsAddForm,ReviewerRegistrationForm
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.models import Group

#to make it such that the elemnts listed can to gone to next page if its too much
#import http in view
# Create your views here.
def posts_list (request):
    #to get the searchd item from the name in search bar
    search_term=request.GET.get('searchpost')
    if search_term:
        #there is a valid search term,filter the list of objects with it
        post_contentlist= postsm.objects.filter(post_title__icontains=search_term)
    else:
        post_contentlist = postsm.objects.all()
    #create a paginator class object
    #into the constructor pass the list as well as the max no of items per page
    paginator = Paginator(post_contentlist,per_page=3)
    #get the GET variable page
    page = request.GET.get('page')
    #handle exception using try except block
    try:
        posts = paginator.page(page)
        #is raised when page is having a value that is not an integer
    except PageNotAnInteger:
        posts = paginator.page(1)
        #is raised when page is having a valid value but no objects exist in that page
    except EmptyPage:
        #num pages returns the total number of pages
        posts = paginator.page(paginator.num_pages)
    #objects.all() fn will be returning a dictionary,we're savng that a variable
    print(post_contentlist)
    #passing the dictionary obtained into the html with context name postlist
    return render(request,"posts.html",{"search_term":search_term,"postlist":posts,'page':page})

def post_details(request,post_id):
    post=get_object_or_404(postsm,id=post_id)
    review_details = Reviews.objects.filter(post__in=[post_id])
    #get all the reviews for post_id field called 'Post' in the review model
    return render(request,"post_details.html",{"posts":post,"review_details":review_details})

def user_login_view(request):
        if request.method == 'POST':
            #it'll get the posted variables from the MyLoginForm
            login_form = MyLoginForm(request.POST)
            #checking if the post request parameters are valid
            if login_form.is_valid():#checking if the form submission was valid
                #using the cleaned_data attribute we're sanitizing the input
                cleaned_data = login_form.cleaned_data
                #now we can proceed with the authentication
                auth_user = authenticate(request,username = cleaned_data['username'],password = cleaned_data['password'])
                if auth_user is not None:
                    #if the authenticante fn returned a valid user
                    #perform the login
                    login(request, auth_user)
                    return HttpResponse('<h1>Authenticated</h1>')
                else:
                    return HttpResponse('<h1>Not Authenticated</h1>')
        else:
            login_form = MyLoginForm #if the form submission was not POST give login again

        return render(request, "useraccount/userlogin.html", {"login_form": login_form})


def register(request):
    if request.method == 'POST':
        # it'll get the posted variables from the MyLoginForm
        user_reg_form = UserRegistrationForm(request.POST)
        # checking if the post request parameters are valid
        if user_reg_form.is_valid():  #
            #receive the data,create the form,do not save it,just keep it temporarily without saving
            new_user = user_reg_form.save(commit=False)
            #set the password with cleaned data for password
            #cleaned_data will automatically be calling the form's clean_password2 function
            new_user.set_password(user_reg_form.cleaned_data['password'])
            #permanently save the new user modal data into database
            new_user.save()
            #after saving,render or display the template register_done.html
            return render(request,'account/register_done.html',{'user_reg_form':user_reg_form})

    else:#if the user registration form is not valid or not submitted
            #in that case give the user,the blank registration form from register.html
            user_reg_form=UserRegistrationForm()
    return render(request, "account/register.html", {"user_reg_form": user_reg_form})

@login_required
#define the view for adding the post
def add_post(request):
    #create an object of the form PostAddForm
    #with the post variables and also the posted image file
    add_post_form = PostAddForm(request.POST, request.FILES)
    #checking if the user posted the form by clicking submit
    if request.method == 'POST':
        if add_post_form.is_valid():
            #get the data,but do not save it now
            newpost = add_post_form.save(commit=False)
            #get the current user and add that info to the post_author field
            newpost.post_author = request.user
            #save the changes to database
            newpost.save()
            #if save successful redirect the user to home page or listing page
            return redirect('home_path')
        else:
            add_post_form = PostAddForm()#give a fresh blank form to user
            #if the user is not submitting the form render the fresh add post form
    return render(request, "account/add_post.html", {"add_post_form": add_post_form})
@login_required
def edit_post(request,passed_id):
    #with the post variables and also the posted image file
    post_detail=get_object_or_404(postsm,id=passed_id)
    edit_post_form = PostAddForm(request.POST or None, request.FILES or None,instance=post_detail)
    #checking if the user posted the form by clicking submit
    if edit_post_form.is_valid():
            edit_post_form.save()
            #if save successful redirect the user to home page or listing page
            return redirect('home_path')

    return render(request, "account/edit_post.html", {"edit_post_form": edit_post_form})

@login_required
def delete_post(request, passed_id):
    # with the post variables and also the posted image file
    post_detail = get_object_or_404(postsm, id=passed_id)
    post_detail.delete()
    return redirect('home_path')
@login_required
#define the view for adding the post
def add_review(request,passed_id):
    #create an object of the form PostAddForm
    #with the post variables and also the posted image file
    add_review_form = ReviewsAddForm(request.POST)
    #checking if the user posted the form by clicking submit
    if request.method == 'POST':
        if add_review_form.is_valid():
            #get the data,but do not save it now
            review = add_review_form.save(commit=False)
            #get the current user and add that info to the post_author field
            review.review_author = request.user
            review.post_id = passed_id#since post is a keyword we use the actual column name
            #save the changes to database
            review.save()
            #if save successful redirect the user to home page or listing page
            return redirect('post_details',passed_id)
        else:
            add_review_form = ReviewsAddForm()#give a fresh blank form to user
            #if the user is not submitting the form render the fresh add post form
    return render(request, "account/add_review.html", {"add_review_form": add_review_form})

def register_reviewer(request):
    if request.method == 'POST':
        # it'll get the posted variables from the MyLoginForm
        rev_reg_form = ReviewerRegistrationForm(request.POST)
        # checking if the post request parameters are valid
        if rev_reg_form.is_valid():
            #receive the data,create the form,do not save it,just keep it temporarily without saving
            new_user = rev_reg_form.save(commit=False)
            #set the password with cleaned data for password
            #cleaned_data will automatically be calling the form's clean_password2 function
            new_user.set_password(rev_reg_form.cleaned_data['password'])
            #permanently save the new user modal data into database
            new_user.save()
            reviewers_group = Group.objects.get(name='reviewers')
            new_user.groups.add(reviewers_group)
            #add the user by default to the reviewers group
            #after saving,render or display the template register_done.html
            return render(request,'account/register_done.html',{'rev_reg_form':rev_reg_form})

    else:#if the user registration form is not valid or not submitted
            #in that case give the user,the blank registration form from register.html
            rev_reg_form=ReviewerRegistrationForm()
    return render(request, "account/register_rev.html", {"rev_reg_form": rev_reg_form})




