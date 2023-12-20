from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect,get_object_or_404
from shared_app.form import LoginForm,ReportForm
from django.contrib import messages
from blogger.form import RegistrationForm
from blogger.form import BlogForm,BlogUpdateForm
from shared_app.models import Like_blog,Blog,Comment,report
from blogger.models import blog_maker
from django.contrib import messages
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            blogger = blog_maker.objects.get(username=username)
            if password == blogger.password:
                if not blogger.status:
                    messages.error(request, 'Your registration request is under approval, please wait for approval.')
                    return redirect('home')
                else:
                    messages.success(request, 'Login successful!')
                    return redirect('blogger_portal', blogger_id=blogger.id)
            else:
                messages.error(request, 'Invalid username or password.')
        except blog_maker.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html', {'user_role': 'blogger'})

def blogger_portal(request, blogger_id):
    blogger = get_object_or_404(blog_maker, id=blogger_id)
    blogs = Blog.objects.all().order_by('-created_at')
    liked_blog_ids = Like_blog.objects.filter(blogger_id=blogger.id).values_list('blog_id', flat=True)
    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'blogging_portal.html', {'blogger': blogger, 'blogs': blogs ,'like_blogs': liked_blog_ids,'comments': comments})

def like_blog(request, blogger_id, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blogger = get_object_or_404(blog_maker, id=blogger_id)
    blogger_id = int(blogger_id)
    like_blog = Like_blog(blog=blog, blogger_id=blogger_id)
    like_blog.save()
    print('done')
    messages.success(request, 'Post Liked successfully!')
    return redirect('blogger_portal', blogger_id=blogger_id)



def delete_like_blog(request, blogger_id, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blogger = get_object_or_404(blog_maker, id=blogger_id)
    
    try:
        like_blog = Like_blog.objects.get(blog=blog, blogger_id=blogger_id)
        messages.success(request, 'Like Remove Successfully!')
    except Like_blog.DoesNotExist:
        return redirect('blogger_portal', blogger_id=blogger_id)
    like_blog.delete()
    return redirect('blogger_portal', blogger_id=blogger_id)

def add_comment(request, blog_id ,blogger_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blogger = get_object_or_404(blog_maker, pk=blogger_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(blog=blog, user=blogger, text=text)
            messages.success(request, 'Blog Commented successfully!')
    return redirect('blogger_portal', blogger_id=blogger.id)

def report_blog(request, blogger_id, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blogger = get_object_or_404(blog_maker, pk=blogger_id)

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data['text']
            image = form.cleaned_data['image']
            report.objects.create(blog=blog, user=blogger, text=text, image=image)
            messages.success(request, 'Blog Reported successfully!')
    else:
        form = ReportForm()    
    return redirect('blogger_portal', blogger_id=blogger.id)

def view_blogs(request, blogger_id):
    blogger = get_object_or_404(blog_maker, id=blogger_id)
    blogs = Blog.objects.filter(blogger_id=blogger).order_by('-created_at')
    liked_blog_ids = Like_blog.objects.filter(blogger_id=blogger.id).values_list('blog_id', flat=True)
    comments = Comment.objects.all().order_by('-created_at')    
    return render(request, 'my_blogs.html', {'blogger': blogger, 'blogs': blogs, 'like_blogs': liked_blog_ids, 'comments': comments})

def delete_blog(request, blogger_id, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, blogger_id=blogger_id) 
    blog.delete()
    messages.success(request, 'Blog deleted successfully!')
    return redirect('view_blogs', blogger_id=blogger_id)

def update_blog(request, blogger_id, blog_id):
    blogger = get_object_or_404(blog_maker, id=blogger_id)
    blog = get_object_or_404(Blog, id=blog_id, blogger_id=blogger_id)

    if request.method == 'POST':
        form = BlogUpdateForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            updated_blog = form.save(commit=False)

            if 'image' in request.FILES:
                image = request.FILES['image']
                img = Image.open(image)
                buffer = BytesIO()
                img.save(buffer, format="WEBP")
                webp_image = ContentFile(buffer.getvalue(), name=f'{image.name.split(".")[0]}.webp')
                updated_blog.image = webp_image

            updated_blog.save()
            messages.success(request, 'Blog Updated successfully!')
            return redirect('view_blogs', blogger_id=blogger_id)
            
    else:
        form = BlogUpdateForm(instance=blog)

    return render(request, 'update_blog.html', {'form': form, 'blogger': blogger, 'blog': blog})
    
def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)

            if 'profile_image' in request.FILES:
                profile_image = request.FILES['profile_image']
                img = Image.open(profile_image)

                buffer = BytesIO()
                img.save(buffer, format="WEBP")
                webp_profile_image = ContentFile(buffer.getvalue(), name=f'{profile_image.name.split(".")[0]}.webp')
                user.profile_image = webp_profile_image

            user.save()
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'user_registration.html', {'form': form})


def create_blog(request, blogger_id):
    if blogger_id is None:
        raise ValueError("blogger_id is required.")
    
    Blogger = get_object_or_404(blog_maker, id=blogger_id)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.blogger_id = Blogger

            if 'image' in request.FILES:
                image = request.FILES['image']
                img = Image.open(image)

                buffer = BytesIO()
                img.save(buffer, format="WEBP")
                webp_image = ContentFile(buffer.getvalue(), name=f'{image.name.split(".")[0]}.webp')
                blog.image = webp_image

            blog.save()
            print('Work done')
    else:
        form = BlogForm()

    return render(request, 'add_blog.html', {'form': form, 'blogger': Blogger})