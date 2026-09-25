from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from student_report.models import FieldPlacement


# Field report
@login_required(login_url="login_admin")
def field_report_a(request):

    # Only staff/admin users can access this page
    if not request.user.is_staff:
        return redirect("login_admin")

    field_reports = (
        FieldPlacement.objects
        .select_related("student")
        .prefetch_related("daily_reports")
        .order_by("-created_at")
    )

    return render(request, "field_report_a.html", {
        "field_reports": field_reports,
        "total_field_reports": field_reports.count(),
    })




# Report preview
@login_required(login_url="login_admin")
def report_preview_a(request, id):
    # Only staff/admin users can access student report previews
    if not request.user.is_staff:
        return redirect("login_admin")

    placement = get_object_or_404(
        FieldPlacement.objects.select_related(
            "student",
            "generated_report",
        ),
        id=id,
    )

    # Get the generated report connected to this placement
    report = getattr(placement, "generated_report", None)

    # If the student has not generated/saved a report yet
    if report is None:
        return render(
            request,
            "report_preview_a.html",
            {
                "placement": placement,
                "report": None,
                "no_report": True,
            },
        )

    return render(
        request,
        "report_preview_a.html",
        {
            "placement": placement,
            "report": report,
            "no_report": False,
        },
    )