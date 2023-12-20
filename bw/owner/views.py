import sys
from shared_app.form import LoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from shared_app.models import Like_blog,Blog,Comment,report
from blogger.models import blog_maker
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage

def owner_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.is_superuser:
                login(request, user)
                print('Login successful', file=sys.stdout)
                
                # Set session variables
                request.session['user_id'] = user.id
                request.session['user_role'] = 'Owner'
                
                return redirect('owner_portal')
                messages.success(request, 'Owner Login successfully!')
            else:
                print('Login failed', file=sys.stdout)
                messages.error(request, 'Owner Login Failled!')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'user_role': 'Owner'})

def owner_portal(request):
    blogs = Blog.objects.all().order_by('-created_at')
    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'owner_portal.html', {'blogs': blogs ,'comments': comments})


def reported_blogs(request):
    reports = report.objects.all()
    blogs = Blog.objects.filter(repoted__in=reports).distinct()
    return render(request, 'reported_blogs.html', {'blogs': blogs, 'reports': reports})

def reject_request(request, report_id):
    report_instance = get_object_or_404(report, id=report_id)

    report_instance.delete()

    subject = 'Your Report Request Update'
    
    message = (
        f"Hello {report_instance.user.username},\n\n"
        "We hope this message finds you well. We wanted to update you regarding your recent report request.\n\n"
        f"Unfortunately, your report for the blog titled '{report_instance.blog.title}' has been rejected. "
        "Our team reviewed the report, and after careful consideration, we determined that it does not violate our guidelines.\n\n"
        "If you have any further concerns or questions, please feel free contact us.\n\n"
        "Thank you for your understanding and cooperation.\n\n"
        "Best regards,\nOK Blog Support Team"
    )

    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = report_instance.user.email

    send_mail(subject, message, from_email, [to_email])
    messages.success(request, 'Blog Report Request rejected and record deleted successfully!')
    return redirect('reported_blogs')

def accept_request(request, report_id):
    report_instance = get_object_or_404(report, id=report_id)

    # Delete the reported blog
    blog_instance = report_instance.blog
    blog_instance.delete()

    # Delete the report
    report_instance.delete()

    # Send email to the user who reported
    reporter_subject = 'Your Report Request Update'
    reporter_message = (
        f"Hello {report_instance.user.username},\n\n"
        "We hope this message finds you well. We wanted to update you regarding your recent report request.\n\n"
        f"Good news! Your report for the blog titled '{report_instance.blog.title}' has been reviewed and accepted. "
        "Our team has taken appropriate action to address the reported issue.\n\n"
        "Thank you for helping us maintain a safe and positive community.\n\n"
        "Best regards,\nYour Blog Support Team"
    )
    send_mail(reporter_subject, reporter_message, settings.DEFAULT_FROM_EMAIL, [report_instance.user.email])

    blogger_subject = 'Your Blog Update'
    blogger_message = (
        f"Hello {blog_instance.blogger_id.username},\n\n"
        "We hope this message finds you well. We wanted to inform you that your blog titled "
        f"'{blog_instance.title}' has been flagged for review, and unfortunately, it has been deleted.\n\n"
        "Our team conducted a review based on a user report, and we found that the blog violated our guidelines. "
        "If you have any questions or concerns, please feel free to reach out to us.\n\n"
        "Thank you for your understanding and cooperation.\n\n"
        "Best regards,\nYour Blog Support Team"
    )
    send_mail(blogger_subject, blogger_message, settings.DEFAULT_FROM_EMAIL, [blog_instance.blogger_id.email])

    messages.success(request, 'Blog Report Request Approved and record deleted successfully!')
    return redirect('reported_blogs')

def view_blogger_to_approve(request):
    blogger = blog_maker.objects.filter(status=False)
    return render(request, 'bloggers_approval.html', {'bloggers': blogger})

def view_blogger(request):
    blogger = blog_maker.objects.all()
    return render(request, 'view_bloggers.html', {'bloggers': blogger})

def approve_blogger(request, blogger_id):
    try:
        blogger = blog_maker.objects.get(id=blogger_id)
        blogger.status = True
        blogger.save()
        send_response_to_student_email(blogger.id,'approve')
        messages.success(request, 'Blogger Approved successfully!')
    except blogger.DoesNotExist:
        messages.error(request, 'Blogger not found.')
    return redirect('view_blogger_to_approve')

def reject_blogger(request, blogger_id):
    try:
        blogger = blog_maker.objects.get(id=blogger_id)
        send_response_to_student_email(blogger.id,'reject')
        blogger.delete()
        messages.success(request, 'Blogger rejected and record deleted successfully!')
    except blogger.DoesNotExist:
        messages.error(request, 'Blogger not found.')
    return redirect('view_blogger_to_approve')

def send_response_to_student_email(blogger_id,status):
    blogger = get_object_or_404(blog_maker, id=blogger_id)
    if status=='approve':
        subject = f'Registration Request Accepted - Blogger Website'
    elif status=='reject':
        subject = f'Registration Request Rejected - Blogger Website'
    if status=='approve' :
        message = f"Dear {blogger.first_name},\n\n" \
                f"We hope this email finds you well. We are pleased to inform you that your registration request for Our bloggers website has been successfully accepted.\n\n" \
                f"Here are the details you need to access your portal:\n\n" \
                f"Username: {blogger.username}\n" \
                f"Password: {blogger.password}\n\n" \
                f"With these credentials, you can now log in to your portal and manage your Posts and view other posts. Here are a few things you can do through your portal:\n\n" \
                f"- Update Blogs: Make changes to your Blogs information such as your blogs image ,content etc. Please note that any changes should be made well in advance.\n" \
                f"- Receive Alerts: Stay informed about any important updates or announcements related to any requests.\n\n" \
                f"We are committed to providing a safe and efficient blogging experience for our community, and we believe that this website will help streamline the process and enhance your overall experience.\n\n" \
                f"If you encounter any issues or have questions about using the portal, please do not hesitate to contact us.\n\n" \
                f"We look forward to ensuring a smooth and comfortable Blogging experience for you.\n\n" \
                f"Best regards,\n\n" \
                f"Osama Khursheed\n" \
                f"Owner"
    elif status=='reject':
        message=f"Dear {blogger.first_name},\n\n" \
              f"I hope this message finds you well. We regret to inform you that your registration request for our Blogging Website has not been approved at this time. After careful consideration, we are unable to accommodate your request for the following reason:\n\n" \
              f"We cannot process your request now; please try again later.\n\n" \
              f"We understand that reliable transportation is crucial for students, and we sincerely apologize for any inconvenience this may cause. Please note that our decision is based on factors beyond our control, and we have made every effort to prioritize the safety and efficiency of our Blogging Website.\n\n" \
              f"If you have any questions or require further clarification regarding this decision, please do not hesitate to reach out to us. we will be happy to assist you and provide any necessary information.\n\n" \
              f"Thank you for considering our Blogging Website, and we wish you a successful and enjoyable academic year.\n\n" \
              f"Best regards,\n\n" \
              f"Osama Khursheed\n" \
              f"Owner"
    from_email = 'uitvanowner@gmail.com'
    recipient_list = [blogger.email]

    try:
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.send()
        print('Email sent successfully')
    except Exception as e:
        print(f'Email sending failed: {str(e)}')
