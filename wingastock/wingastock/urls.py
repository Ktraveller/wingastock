"""
URL configuration for winga_project project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap


from core.sitemaps import ProductSitemap, StaticViewSitemap


# ==========================================================
# ROBOTS.TXT
# ==========================================================

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
    return HttpResponse(
        content,
        content_type="text/plain"
    )


# ==========================================================
# SITEMAPS
# ==========================================================

sitemaps = {
    "products": ProductSitemap,
    "static": StaticViewSitemap,
}


# ==========================================================
# URL PATTERNS
# ==========================================================

urlpatterns = [

    # ------------------------------------------------------
    # Django Admin
    # ------------------------------------------------------
    path(
        "admin/",
        admin.site.urls
    ),


    # ------------------------------------------------------
    # Robots
    # ------------------------------------------------------
    path(
        "robots.txt",
        robots_txt
    ),


    # ------------------------------------------------------
    # LANGUAGE SWITCHING
    # ------------------------------------------------------
    path(
        "i18n/",
        include("django.conf.urls.i18n")
    ),


    # ------------------------------------------------------
    # CORE
    # ------------------------------------------------------
    path(
        "",
        include("core.urls")
    ),


    # ------------------------------------------------------
    # SELLERS
    # ------------------------------------------------------
    path(
        "sellers/",
        include("sellers.urls")
    ),


    # ------------------------------------------------------
    # ADMINISTRATORS
    # ------------------------------------------------------
    path(
        "administrators/",
        include("administrators.urls")
    ),


    # ------------------------------------------------------
    # MAILS
    # ------------------------------------------------------
    path(
        "mails/",
        include("mails.urls")
    ),


    # ------------------------------------------------------
    # DELIVERY
    # ------------------------------------------------------
    path(
        "deliver/",
        include("deliver.urls")
    ),


    # ------------------------------------------------------
    # E report
    # ------------------------------------------------------
    path(
        "ereport/",
        include("student_report.urls")
    ),


    # ------------------------------------------------------
    # SITEMAP
    # ------------------------------------------------------
    path(
        "sitemap.xml",
        sitemap,
        {
            "sitemaps": sitemaps
        },
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
