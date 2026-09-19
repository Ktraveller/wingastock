from datetime import timedelta
from django.utils import timezone

from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from student_report.models import DailyFieldReport



# Dashboard
@login_required(login_url="home")
def report_index(request):

    # All reports belonging to the logged-in user
    daily_reports = DailyFieldReport.objects.filter(
        placement__student=request.user
    )

    # Total daily reports
    total_daily_reports = daily_reports.count()

    # ---------------------------------------------
    # Total unique weeks
    # ---------------------------------------------

    report_dates = daily_reports.values_list(
        "date",
        flat=True
    ).distinct()

    weekly_report_weeks = set()

    for report_date in report_dates:
        week_start = (
            report_date
            - timedelta(days=report_date.weekday())
        )

        weekly_report_weeks.add(week_start)

    total_weekly_reports = len(
        weekly_report_weeks
    )

    # ---------------------------------------------
    # THIS WEEK'S DAILY REPORTS
    # ---------------------------------------------

    today = timezone.localdate()

    # Monday of this week
    this_week_start = (
        today - timedelta(days=today.weekday())
    )

    # Next Monday
    next_week_start = this_week_start + timedelta(
        days=7
    )

    this_week_reports = DailyFieldReport.objects.filter(
        placement__student=request.user,
        date__gte=this_week_start,
        date__lt=next_week_start,
    ).select_related(
        "placement"
    ).order_by(
        "-date"
    )

    return render(
        request,
        "index_re.html",
        {
            "total_daily_reports": total_daily_reports,
            "total_weekly_reports": total_weekly_reports,
            "this_week_reports": this_week_reports,
        }
    )