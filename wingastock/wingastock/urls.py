"""
URL configuration for winga_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import ProductSitemap, StaticViewSitemap



def robots_txt(request):
    content = """User-agent: *
Allow: /

Disallow: /admin/
Disallow: /login/
Disallow: /logout/
Disallow: /register/
Disallow: /accounts/
Disallow: /search/

Sitemap: https://wingastock.onrender.com/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")


sitemaps = {
    "products": ProductSitemap,
    "static": StaticViewSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path("robots.txt", robots_txt),
    path('', include('core.urls')),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
