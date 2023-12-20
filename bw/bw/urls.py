"""
URL configuration for bw project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shared_app import views as share
from owner import views as owner
from blogger import views as user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', share.home_page, name='home'),
    path('about_us/', share.about_page, name='about_us'),
    path('contact_us/', share.contact_page, name='contact_us'),
    path('user_login/', user.user_login, name='user_login'),
    path('blogger_portal/<int:blogger_id>/', user.blogger_portal, name='blogger_portal'),
    path('view_blogs/<int:blogger_id>/', user.view_blogs, name='view_blogs'),
    path('owner_login/', owner.owner_login, name='owner_login'),
    path('owner_portal/', owner.owner_portal, name='owner_portal'),
    path('view_blogger_to_approve/', owner.view_blogger_to_approve, name='view_blogger_to_approve'),
    path('view_blogger/', owner.view_blogger, name='view_blogger'),
    path('reported_blogs/', owner.reported_blogs, name='reported_blogs'),
    path('reject_request/<int:report_id>/', owner.reject_request, name='reject_request'),
    path('accept_request/<int:report_id>/', owner.accept_request, name='accept_request'),
    path('approve_blogger/<int:blogger_id>/', owner.approve_blogger, name='approve_blogger'),
    path('reject_blogger/<int:blogger_id>/', owner.reject_blogger, name='reject_blogger'),
    path('register/', user.user_registration, name='register'),
    path('create_blog/<int:blogger_id>/', user.create_blog, name='create_blog'),
    path('like_blog/<int:blogger_id>/<int:blog_id>/', user.like_blog, name='like_blog'),
    path('delete_like_blog/<int:blogger_id>/<int:blog_id>/', user.delete_like_blog, name='delete_like_blog'),
    path('add_comment/<int:blog_id>/<int:blogger_id>/', user.add_comment, name='add_comment'),
    path('report_blog/<int:blog_id>/<int:blogger_id>/', user.report_blog, name='report_blog'),
    path('delete_blog/<int:blogger_id>/<int:blog_id>/', user.delete_blog, name='delete_blog'),
    path('update_blog/<int:blogger_id>/<int:blog_id>/', user.update_blog, name='update_blog'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)