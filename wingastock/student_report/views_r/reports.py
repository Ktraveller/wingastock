from django.shortcuts import redirect, render
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from student_report.models import DailyFieldReport, FieldPlacement, GeneratedFieldReport
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import json
from datetime import date
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from collections import OrderedDict
from datetime import timedelta
from django.http import JsonResponse

from io import BytesIO

from bs4 import BeautifulSoup, NavigableString, Tag
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt




# Add placement 
@login_required(login_url="home")
def add_placement(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid request method."
            },
            status=405
        )

    # ---------------------------------
    # Read JSON data
    # ---------------------------------

    try:
        data = json.loads(request.body)

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid JSON data."
            },
            status=400
        )

    organization = str(data.get("organization", "")).strip()
    department = str(data.get("department", "")).strip()
    supervisor_name = str(data.get("supervisor_name", "")).strip()
    supervisor_phone = str(data.get("supervisor_phone", "")).strip()
    start_date = str(data.get("start_date", "")).strip()
    end_date = str(data.get("end_date", "")).strip()

    # ---------------------------------
    # Basic required field validation
    # ---------------------------------

    if not organization:
        return JsonResponse({
            "success": False,
            "message": "Organization name is required."
        }, status=400)

    if not department:
        return JsonResponse({
            "success": False,
            "message": "Department is required."
        }, status=400)

    if not supervisor_name:
        return JsonResponse({
            "success": False,
            "message": "Supervisor name is required."
        }, status=400)

    if not start_date:
        return JsonResponse({
            "success": False,
            "message": "Start date is required."
        }, status=400)

    if not end_date:
        return JsonResponse({
            "success": False,
            "message": "End date is required."
        }, status=400)

    # ---------------------------------
    # Validate date format
    # ---------------------------------

    try:
        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)

    except ValueError:
        return JsonResponse({
            "success": False,
            "message": "Please enter valid start and end dates."
        }, status=400)

    # ---------------------------------
    # End date cannot be before start
    # ---------------------------------

    if end_date < start_date:
        return JsonResponse({
            "success": False,
            "message": "End date cannot be before the start date."
        }, status=400)

    # ---------------------------------
    # Start date cannot be in the past
    # ---------------------------------

    if start_date < date.today():
        return JsonResponse({
            "success": False,
            "message": "Start date cannot be in the past."
        }, status=400)

    # ---------------------------------
    # Validate organization length
    # ---------------------------------

    if len(organization) < 2:
        return JsonResponse({
            "success": False,
            "message": "Organization name is too short."
        }, status=400)

    if len(organization) > 255:
        return JsonResponse({
            "success": False,
            "message": "Organization name is too long."
        }, status=400)

    # ---------------------------------
    # Validate supervisor name
    # ---------------------------------

    if len(supervisor_name) < 2:
        return JsonResponse({
            "success": False,
            "message": "Supervisor name is too short."
        }, status=400)

    # ---------------------------------
    # Validate phone
    # ---------------------------------

    if supervisor_phone:

        allowed_chars = "0123456789+-() "

        if any(
            char not in allowed_chars
            for char in supervisor_phone
        ):
            return JsonResponse({
                "success": False,
                "message": "Please enter a valid supervisor phone number."
            }, status=400)

        digits = "".join(
            char for char in supervisor_phone
            if char.isdigit()
        )

        if len(digits) < 9 or len(digits) > 15:
            return JsonResponse({
                "success": False,
                "message": "Supervisor phone number is invalid."
            }, status=400)

    # ---------------------------------
    # Check overlapping placements
    # ---------------------------------

    student = request.user

    overlapping = FieldPlacement.objects.filter(
        student=student,
        start_date__lte=end_date,
        end_date__gte=start_date
    ).exists()

    if overlapping:
        return JsonResponse({
            "success": False,
            "message": (
                "You already have a field placement within "
                "the selected date range."
            )
        }, status=400)

    # ---------------------------------
    # Save placement
    # ---------------------------------

    FieldPlacement.objects.create(
        student=student,
        organization=organization,
        department=department,
        supervisor_name=supervisor_name,
        supervisor_phone=supervisor_phone,
        start_date=start_date,
        end_date=end_date,
    )

    # ---------------------------------
    # Success response
    # ---------------------------------

    return JsonResponse({
        "success": True,
        "message": "Field placement saved successfully."
    })



# Edit placement
@login_required(login_url="home")
def edit_placement(request, id):

    placement = get_object_or_404(
        FieldPlacement,
        id=id
    )

    # Check ownership
    if placement.student != request.user:
        messages.error(
            request,
            "You are not authorized to edit this placement."
        )
        return redirect("daily_reports")


    # GET
    if request.method == "GET":

        return render(
            request,
            "edit_placement.html",
            {
                "placement": placement
            }
        )


    # POST
    if request.method == "POST":

        organization = request.POST.get(
            "organization",
            placement.organization
        ).strip()

        department = request.POST.get(
            "department",
            placement.department
        ).strip()

        supervisor_name = request.POST.get(
            "supervisor_name",
            placement.supervisor_name
        ).strip()

        supervisor_phone = request.POST.get(
            "supervisor_phone",
            placement.supervisor_phone or ""
        ).strip()

        start_date_value = request.POST.get(
            "start_date",
            placement.start_date.isoformat()
        ).strip()

        end_date_value = request.POST.get(
            "end_date",
            placement.end_date.isoformat()
        ).strip()


        # Organization
        if not organization:

            messages.error(
                request,
                "Organization name is required."
            )

            return redirect(
                "edit_placement",
                id=placement.id
            )


        if len(organization) < 2:

            messages.error(
                request,
                "Organization name is too short."
            )

            return redirect(
                "edit_placement",
                id=placement.id
            )


        if len(organization) > 255:

            messages.error(
                request,
                "Organization name is too long."
            )

            return redirect(
                "edit_placement",
                id=placement.id
            )


        # Department
        if not department:

            messages.error(
                request,
                "Department is required."
            )

            return redirect(
                "edit_placement",
                id=placement.id
            )


        if len(department) > 255:

            messages.error(
                request,
                "Department name is too long."
            )

            return redirect(
                "edit_placement",
                id=placement.id
            )


        # Supervisor
        if not supervisor_name:

            messages.error(
                request,
                "Supervisor name is required."
            )

            return redirect(
                "edit_placement",
                id=placement.id
            )


        if len(supervisor_name) < 2:

            messages.error(
                request,
                "Supervisor name is too short."
            )

            return redirect(
                "edit_placement",
                id=placement.id
            )


        # Dates
        try:

            start_date = date.fromisoformat(
                start_date_value
            )

            end_date = date.fromisoformat(
                end_date_value
            )

        except ValueError:

            messages.error(
                request,
                "Please enter valid start and end dates."
            )

            return redirect(
                "edit_placement",
                id=placement.id
            )


        if end_date < start_date:

            messages.error(
                request,
                "End date cannot be before the start date."
            )

            return redirect(
                "edit_placement",
                id=placement.id
            )


        # Prevent changing to a new past start date
        if (
            start_date != placement.start_date
            and start_date < date.today()
        ):

            messages.error(
                request,
                "Start date cannot be in the past."
            )

            return redirect(
                "edit_placement",
                id=placement.id
            )


        # Phone
        if supervisor_phone:

            allowed_chars = "0123456789+-() "

            if any(
                char not in allowed_chars
                for char in supervisor_phone
            ):

                messages.error(
                    request,
                    "Please enter a valid supervisor phone number."
                )

                return redirect(
                    "edit_placement",
                    id=placement.id
                )


            digits = "".join(
                char
                for char in supervisor_phone
                if char.isdigit()
            )

            if len(digits) < 9 or len(digits) > 15:

                messages.error(
                    request,
                    "Supervisor phone number is invalid."
                )

                return redirect(
                    "edit_placement",
                    id=placement.id
                )


        # Check overlapping placement
        overlapping = FieldPlacement.objects.filter(
            student=request.user,
            start_date__lte=end_date,
            end_date__gte=start_date
        ).exclude(
            id=placement.id
        ).exists()


        if overlapping:

            messages.error(
                request,
                "You already have a field placement "
                "within the selected date range."
            )

            return redirect(
                "edit_placement",
                id=placement.id
            )


        # Update
        placement.organization = organization
        placement.department = department
        placement.supervisor_name = supervisor_name
        placement.supervisor_phone = supervisor_phone
        placement.start_date = start_date
        placement.end_date = end_date

        placement.save()


        messages.success(
            request,
            "Field placement updated successfully."
        )


        # Return to the same edit-placement page
        return redirect(
            "edit_placement",
            id=placement.id
        )


    # Invalid method
    messages.error(
        request,
        "Invalid request method."
    )

    return redirect(
        "edit_placement",
        id=placement.id
    )







# Placements
@login_required(login_url="home")
def placements(request): 
    placement = FieldPlacement.objects.filter( 
        student=request.user
    ).order_by("-start_date")
    
    return render( 
        request, "placements_re.html", 
        { 
            "placement": placement, 
        } 
    )




# Reports
@login_required(login_url="home")
def reports(request, id):

    placement = get_object_or_404(
        FieldPlacement,
        id=id,
        student=request.user
    )

    report = DailyFieldReport.objects.filter( 
        placement=placement
    ).order_by("-updated_at")

    return render( 
        request, "report_list_re.html", 
        { 
            "report_list": report,
            "placement": placement.id,
            'organization': placement.organization
        } 
    )





# Add new daily report
@login_required(login_url="home")
def add_report(request, id):

    # Get placement
    placement = get_object_or_404(
        FieldPlacement,
        id=id,
        student=request.user
    )

    # --------------------------------------------------
    # Available dates for the placement
    # --------------------------------------------------
    available_dates = []

    current_date = placement.start_date

    while current_date <= placement.end_date:
        available_dates.append(current_date)
        current_date += timedelta(days=1)

    # --------------------------------------------------
    # Handle form submission
    # --------------------------------------------------
    if request.method == "POST":

        report_date = request.POST.get("date", "").strip()
        title = request.POST.get("title", "").strip()
        activities = request.POST.get("activities", "").strip()
        skills_learned = request.POST.get("skills_learned", "").strip()
        challenges = request.POST.get("challenges", "").strip()
        solutions = request.POST.get("solutions", "").strip()
        remarks = request.POST.get("remarks", "").strip()

        errors = []

        # --------------------------------------------------
        # Required field validation
        # --------------------------------------------------

        if not report_date:
            errors.append("Please select a report date.")

        if not title:
            errors.append("Please enter a report title.")

        if not activities:
            errors.append("Please describe the activities completed.")

        if not skills_learned:
            errors.append("Please describe the skills you learned.")

        if not challenges:
            errors.append("Please describe the challenges encountered.")

        if not solutions:
            errors.append("Please describe the solutions used.")

        # --------------------------------------------------
        # Validate date
        # --------------------------------------------------

        selected_date = None

        if report_date:

            try:
                from datetime import datetime

                selected_date = datetime.strptime(
                    report_date,
                    "%Y-%m-%d"
                ).date()

            except ValueError:
                errors.append("Please enter a valid date.")

        # --------------------------------------------------
        # Make sure date is within placement period
        # --------------------------------------------------

        if selected_date:

            if (
                selected_date < placement.start_date
                or selected_date > placement.end_date
            ):
                errors.append(
                    "The report date must be within your field placement period."
                )

        # --------------------------------------------------
        # Prevent duplicate report for same date
        # --------------------------------------------------

        if selected_date:

            duplicate = DailyFieldReport.objects.filter(
                placement=placement,
                date=selected_date
            ).exists()

            if duplicate:
                errors.append(
                    "A report for this date has already been submitted."
                )

        # --------------------------------------------------
        # If validation fails
        # --------------------------------------------------

        if errors:

            for error in errors:
                messages.error(request, error)

            return render(
                request,
                "add_report_re.html",
                {
                    "placement": placement,
                    "available_dates": available_dates,
                    "form_data": request.POST,
                }
            )

        # --------------------------------------------------
        # Create report
        # --------------------------------------------------

        DailyFieldReport.objects.create(
            placement=placement,
            date=selected_date,
            title=title,
            activities=activities,
            skills_learned=skills_learned,
            challenges=challenges,
            solutions=solutions,
            remarks=remarks,
        )

        messages.success(
            request,
            "Daily field report submitted successfully."
        )

        return redirect("reports_list", id)

    # --------------------------------------------------
    # Display form
    # --------------------------------------------------

    return render(
        request,
        "add_report_re.html",
        {
            "placement": placement,
            "available_dates": available_dates,
        }
    )




# Edit report
@login_required(login_url="home")
def edit_report(request, id):

    # --------------------------------------------------
    # Get the existing report
    # --------------------------------------------------
    report = get_object_or_404(
        DailyFieldReport,
        id=id,
        placement__student=request.user
    )

    placement = report.placement

    # --------------------------------------------------
    # Prevent editing approved reports
    # --------------------------------------------------
    if report.supervisor_approved:
        messages.error(
            request,
            "This report has already been approved and cannot be edited."
        )
        return redirect("report_detail", report.id)

    # --------------------------------------------------
    # Available dates for the placement
    # --------------------------------------------------
    available_dates = []

    current_date = placement.start_date

    while current_date <= placement.end_date:
        available_dates.append(current_date)
        current_date += timedelta(days=1)

    # --------------------------------------------------
    # Handle form submission
    # --------------------------------------------------
    if request.method == "POST":

        report_date = request.POST.get("date", "").strip()
        title = request.POST.get("title", "").strip()
        activities = request.POST.get("activities", "").strip()
        skills_learned = request.POST.get("skills_learned", "").strip()
        challenges = request.POST.get("challenges", "").strip()
        solutions = request.POST.get("solutions", "").strip()
        remarks = request.POST.get("remarks", "").strip()

        errors = []

        # --------------------------------------------------
        # Required field validation
        # --------------------------------------------------

        if not report_date:
            errors.append("Please select a report date.")

        if not title:
            errors.append("Please enter a report title.")

        if not activities:
            errors.append(
                "Please describe the activities completed."
            )

        # These are optional in your model,
        # so don't make them required.
        #
        # skills_learned = optional
        # challenges = optional
        # solutions = optional
        # remarks = optional

        # --------------------------------------------------
        # Validate title length
        # --------------------------------------------------

        if title and len(title) > 255:
            errors.append(
                "Report title cannot exceed 255 characters."
            )

        # --------------------------------------------------
        # Validate date
        # --------------------------------------------------

        selected_date = None

        if report_date:

            try:
                selected_date = datetime.strptime(
                    report_date,
                    "%Y-%m-%d"
                ).date()

            except ValueError:
                errors.append(
                    "Please enter a valid date."
                )

        # --------------------------------------------------
        # Make sure date is within placement period
        # --------------------------------------------------

        if selected_date:

            if (
                selected_date < placement.start_date
                or selected_date > placement.end_date
            ):
                errors.append(
                    "The report date must be within your "
                    "field placement period."
                )

        # --------------------------------------------------
        # Prevent duplicate report for same date
        # --------------------------------------------------
        # IMPORTANT:
        # Exclude the current report from the check.
        # Otherwise the current date would always
        # appear as a duplicate.
        # --------------------------------------------------

        if selected_date:

            duplicate = DailyFieldReport.objects.filter(
                placement=placement,
                date=selected_date
            ).exclude(
                id=report.id
            ).exists()

            if duplicate:
                errors.append(
                    "Another report for this date has "
                    "already been submitted."
                )

        # --------------------------------------------------
        # If validation fails
        # --------------------------------------------------

        if errors:

            for error in errors:
                messages.error(request, error)

            return render(
                request,
                "edit_report_re.html",
                {
                    "report": report,
                    "placement": placement,
                    "available_dates": available_dates,
                    "form_data": request.POST,
                }
            )

        # --------------------------------------------------
        # Update report
        # --------------------------------------------------

        report.date = selected_date
        report.title = title
        report.activities = activities
        report.skills_learned = skills_learned
        report.challenges = challenges
        report.solutions = solutions
        report.remarks = remarks

        report.save()

        messages.success(
            request,
            "Daily field report updated successfully."
        )

    # --------------------------------------------------
    # Display edit form
    # --------------------------------------------------

    return render(
        request,
        "edit_report_re.html",
        {
            "report": report,
            "placement": placement,
            "available_dates": available_dates,
        }
    )



# Weekly report
@login_required(login_url="home")
def report_detail_weekly(request, id):

    # ---------------------------------
    # Get field placement
    # ---------------------------------

    placement = get_object_or_404(
        FieldPlacement,
        id=id
    )

    # ---------------------------------
    # Make sure logged-in student owns
    # this placement
    # ---------------------------------

    if placement.student != request.user:
        messages.error(
            request,
            "You are not authorized to view this report."
        )

        return redirect("daily_reports", placement)

    # ---------------------------------
    # Get all daily reports
    # ---------------------------------

    reports = DailyFieldReport.objects.filter(
        placement=placement
    ).order_by("-date")

    # ---------------------------------
    # Group reports by week
    # ---------------------------------

    weekly_reports = OrderedDict()

    for report in reports:

        # Monday = start of week
        week_start = report.date - timedelta(
            days=report.date.weekday()
        )

        # Sunday = end of week
        week_end = week_start + timedelta(days=6)

        week_key = week_start

        if week_key not in weekly_reports:
            weekly_reports[week_key] = {
                "week_start": week_start,
                "week_end": week_end,
                "reports": []
            }

        weekly_reports[week_key]["reports"].append(report)

    # ---------------------------------
    # Convert to list for template
    # ---------------------------------

    weekly_reports = list(weekly_reports.values())

    return render(
        request,
        "preview_weekly_report_re.html",
        {
            "placement": placement,
            "weekly_reports": weekly_reports,
        }
    )



# Report summary

@login_required(login_url="home")
def report_summary(request, id):

    # ---------------------------------
    # Get field placement
    # ---------------------------------

    placement = get_object_or_404(
        FieldPlacement,
        id=id
    )

    # ---------------------------------
    # Make sure logged-in student owns
    # this placement
    # ---------------------------------

    if placement.student != request.user:
        messages.error(
            request,
            "You are not authorized to view this report."
        )

        return redirect("daily_reports", placement)

    # ---------------------------------
    # Get all daily reports
    # ---------------------------------

    reports = DailyFieldReport.objects.filter(
        placement=placement
    ).order_by("-date")

    # ---------------------------------
    # Group reports by week
    # ---------------------------------

    weekly_reports = OrderedDict()

    for report in reports:

        # Monday = start of week
        week_start = report.date - timedelta(
            days=report.date.weekday()
        )

        # Sunday = end of week
        week_end = week_start + timedelta(days=6)

        week_key = week_start

        if week_key not in weekly_reports:
            weekly_reports[week_key] = {
                "week_start": week_start,
                "week_end": week_end,
                "reports": []
            }

        weekly_reports[week_key]["reports"].append(report)

    # ---------------------------------
    # Convert to list for template
    # ---------------------------------

    weekly_reports = list(weekly_reports.values())

    return render(
        request,
        "report_summary_re.html",
        {
            "placement": placement,
            "weekly_reports": weekly_reports,
        }
    )





# Report preview
@login_required(login_url="home")
def report_detail(request, id):

    # Get the specific daily report
    report = get_object_or_404(
        DailyFieldReport,
        id=id
    )

    # Make sure the logged-in student owns this report
    if report.placement.student != request.user:

        messages.error(
            request,
            "You are not authorized to view this report."
        )

        return redirect("daily_reports")

    return render(
        request,
        "preview_report_re.html",
        {
            "report": report,
        }
    )




# Delete daily report
@login_required(login_url="home")
def delete_report(request, id):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request method."
        }, status=405)

    report = get_object_or_404(
        DailyFieldReport,
        id=id
    )

    # Make sure the report belongs to the logged-in student
    if report.placement.student != request.user:
        return JsonResponse({
            "success": False,
            "message": "You are not authorized to delete this report."
        }, status=403)

    report.delete()

    return JsonResponse({
        "success": True,
        "message": "Report deleted successfully."
    })




# Delete placement
@login_required(login_url="home")
def delete_placement(request, id):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request method."
        }, status=405)

    placement = get_object_or_404(
        FieldPlacement,
        id=id
    )

    # Make sure the placement belongs to the logged-in student
    if placement.student != request.user:
        return JsonResponse({
            "success": False,
            "message": "You are not authorized to delete this placement."
        }, status=403)

    placement.delete()

    return JsonResponse({
        "success": True,
        "message": "Field placement deleted successfully."
    })






# Generate field report for one placement
@login_required(login_url="home")
def generate_field_report(request, id):

    placement = get_object_or_404(
        FieldPlacement,
        id=id
    )

    # Only the owner of the placement can access the report
    if placement.student != request.user:
        messages.error(
            request,
            "You are not authorized to access this field report."
        )
        return redirect("daily_reports")

    reports = placement.daily_reports.all().order_by("date")

    # Check if this placement already has a saved report
    saved_report = getattr(
        placement,
        "generated_report",
        None
    )

    return render(
        request,
        "generate_field_re.html",
        {
            "placement": placement,
            "reports": reports,
            "saved_report": saved_report,
        }
    )




# Save report
@login_required(login_url="home")
@require_POST
def save_field_report(request, id):

    placement = get_object_or_404(
        FieldPlacement,
        id=id
    )

    # Security check
    if placement.student != request.user:
        return JsonResponse(
            {
                "success": False,
                "message": "You are not authorized to save this report."
            },
            status=403
        )

    report_html = request.POST.get(
        "report_html",
        ""
    )

    if not report_html.strip():
        return JsonResponse(
            {
                "success": False,
                "message": "Report content cannot be empty."
            },
            status=400
        )

    # Create if it doesn't exist,
    # otherwise update the existing report.
    saved_report, created = GeneratedFieldReport.objects.update_or_create(
        placement=placement,
        defaults={
            "report_html": report_html
        }
    )

    return JsonResponse(
        {
            "success": True,
            "message": "Report saved successfully.",
            "created": created,
            "updated_at": saved_report.updated_at.strftime(
                "%d %b %Y, %H:%M"
            ),
        }
    )





# Refresh
@login_required(login_url="home")
def refresh_field_report_data(request, id):

    placement = get_object_or_404(
        FieldPlacement,
        id=id
    )

    # Security check
    if placement.student != request.user:
        return JsonResponse(
            {
                "success": False,
                "message": "You are not authorized to refresh this report."
            },
            status=403
        )

    # Get all daily reports belonging to this placement
    reports = placement.daily_reports.all().order_by("date")

    report_data = []

    for report in reports:

        report_data.append(
            {
                "id": report.id,
                "date": report.date.strftime("%d %B %Y"),
                "title": report.title,
                "activities": report.activities,
                "skills_learned": report.skills_learned,
                "challenges": report.challenges,
                "solutions": report.solutions,
                "remarks": report.remarks,
            }
        )

    return JsonResponse(
        {
            "success": True,
            "message": "Daily reports refreshed successfully.",
            "reports": report_data,
            "total_reports": len(report_data),
        }
    )




# Download docx
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from docx import Document
from docx.shared import Mm, Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def set_cell_text(cell, text, bold=False):
    """
    Safely write text into a DOCX table cell.
    """

    cell.text = ""

    paragraph = cell.paragraphs[0]

    run = paragraph.add_run(
        str(text) if text is not None else ""
    )

    run.bold = bold
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)

    paragraph.paragraph_format.space_after = Pt(0)
    paragraph.paragraph_format.line_spacing = 1.15

    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def set_cell_shading(cell, fill="E7E6E6"):
    """
    Add background color to a table cell.
    """

    tc_pr = cell._tc.get_or_add_tcPr()

    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)

    tc_pr.append(shd)


def set_cell_width(cell, width_mm):
    """
    Set table cell width.
    """

    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()

    tc_w = tc_pr.first_child_found_in("w:tcW")

    if tc_w is None:
        tc_w = OxmlElement("w:tcW")
        tc_pr.append(tc_w)

    tc_w.set(qn("w:w"), str(int(width_mm * 56.7)))
    tc_w.set(qn("w:type"), "dxa")


def set_repeat_table_header(row):
    """
    Make table header repeat on next pages.
    """

    tr_pr = row._tr.get_or_add_trPr()

    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")

    tr_pr.append(tbl_header)


def set_paragraph_format(paragraph):
    """
    Standard report paragraph formatting.
    """

    paragraph.paragraph_format.line_spacing = 1.6
    paragraph.paragraph_format.space_after = Pt(6)
    paragraph.paragraph_format.first_line_indent = Mm(10)

    for run in paragraph.runs:
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)


def add_body_paragraph(document, text):
    """
    Add normal report paragraph.
    """

    text = str(text or "").strip()

    if not text:
        return

    paragraph = document.add_paragraph()

    run = paragraph.add_run(text)

    run.font.name = "Times New Roman"
    run.font.size = Pt(12)

    set_paragraph_format(paragraph)

    return paragraph


def add_heading(document, text, level=1):
    """
    Add report heading.
    """

    paragraph = document.add_paragraph()

    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT

    run = paragraph.add_run(str(text))

    run.bold = True
    run.font.name = "Times New Roman"

    if level == 1:
        run.font.size = Pt(14)
    else:
        run.font.size = Pt(12)

    paragraph.paragraph_format.space_before = Pt(10)
    paragraph.paragraph_format.space_after = Pt(8)
    paragraph.paragraph_format.line_spacing = 1.15

    return paragraph


def add_center_heading(document, text, size=14):
    """
    Centered heading.
    """

    paragraph = document.add_paragraph()

    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = paragraph.add_run(str(text))

    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)

    paragraph.paragraph_format.space_after = Pt(12)

    return paragraph


def add_page_break(document):
    document.add_page_break()


def add_page_number(paragraph):
    """
    Insert dynamic Word page number.
    """

    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = paragraph.add_run()

    fld_char1 = OxmlElement("w:fldChar")
    fld_char1.set(qn("w:fldCharType"), "begin")

    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = "PAGE"

    fld_char2 = OxmlElement("w:fldChar")
    fld_char2.set(qn("w:fldCharType"), "end")

    run._r.append(fld_char1)
    run._r.append(instr_text)
    run._r.append(fld_char2)

    run.font.name = "Times New Roman"
    run.font.size = Pt(10)


def configure_document(document):
    """
    Configure the complete Word document.
    """

    section = document.sections[0]

    # A4
    section.page_width = Mm(210)
    section.page_height = Mm(297)

    # Same approximate margins as browser template
    section.top_margin = Mm(25)
    section.bottom_margin = Mm(25)
    section.left_margin = Mm(22)
    section.right_margin = Mm(22)

    # Default font
    normal = document.styles["Normal"]

    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)

    normal._element.rPr.rFonts.set(
        qn("w:eastAsia"),
        "Times New Roman"
    )

    # Footer
    footer = section.footer

    paragraph = footer.paragraphs[0]

    add_page_number(paragraph)


def build_field_report_docx(placement, reports):

    document = Document()

    configure_document(document)

    # =========================================================
    # DATA
    # =========================================================

    student = placement.student

    student_name = (
        student.get_full_name()
        or student.username
    )

    organization = getattr(
        placement,
        "organization",
        ""
    )

    department = getattr(
        placement,
        "department",
        ""
    )

    supervisor = getattr(
        placement,
        "supervisor_name",
        ""
    )

    start_date = getattr(
        placement,
        "start_date",
        None
    )

    end_date = getattr(
        placement,
        "end_date",
        None
    )

    # =========================================================
    # COVER PAGE
    # =========================================================

    for _ in range(4):
        document.add_paragraph()

    add_center_heading(
        document,
        "FIELD PRACTICAL TRAINING REPORT",
        18
    )

    document.add_paragraph()

    add_center_heading(
        document,
        student_name,
        14
    )

    document.add_paragraph()

    if organization:
        add_center_heading(
            document,
            organization,
            13
        )

    if department:
        add_center_heading(
            document,
            department,
            12
        )

    document.add_paragraph()

    if supervisor:
        add_center_heading(
            document,
            f"Supervisor: {supervisor}",
            12
        )

    if start_date and end_date:

        period = (
            f"{start_date.strftime('%d %B %Y')} - "
            f"{end_date.strftime('%d %B %Y')}"
        )

        add_center_heading(
            document,
            period,
            12
        )

    add_page_break(document)

    # =========================================================
    # DECLARATION
    # =========================================================

    add_center_heading(
        document,
        "DECLARATION",
        14
    )

    declaration = (
        "I, "
        f"{student_name}, "
        "declare that this Field Practical Training Report "
        "is my own work and has been prepared based on the "
        "activities and experiences obtained during my field "
        "practical training."
    )

    add_body_paragraph(
        document,
        declaration
    )

    document.add_paragraph()
    add_body_paragraph(
        document,
        f"Student Name: {student_name}"
    )

    add_body_paragraph(
        document,
        "Signature: ______________________________"
    )

    add_body_paragraph(
        document,
        "Date: ___________________________________"
    )

    add_page_break(document)

    # =========================================================
    # TABLE OF CONTENTS
    # =========================================================

    add_center_heading(
        document,
        "TABLE OF CONTENTS",
        14
    )

    toc_items = [
        ("Declaration", "2"),
        ("Table of Contents", "3"),
        ("List of Tables", "4"),
        ("List of Figures", "5"),
        ("Abbreviations", "6"),
        ("CHAPTER ONE: INTRODUCTION", "7"),
        ("1.1 Background of Industry/Organization", "7"),
        ("1.2 Organization Structure", "8"),
        ("1.3 Vision, Mission and Objectives", "9"),
        ("CHAPTER TWO: ACTIVITIES PERFORMED", "10"),
        ("2.1 Overview", "10"),
        ("2.2 Daily Activities", "10"),
        ("2.3 General Observations", "11"),
        ("2.4 Challenges Encountered", "12"),
        ("2.5 How Challenges Were Solved", "12"),
        ("CHAPTER THREE", "13"),
        ("References", "14"),
        ("Appendices", "15"),
    ]

    for title, page in toc_items:

        paragraph = document.add_paragraph()

        paragraph.paragraph_format.line_spacing = 1.3
        paragraph.paragraph_format.space_after = Pt(4)

        run = paragraph.add_run(
            f"{title} ........................................ {page}"
        )

        run.font.name = "Times New Roman"
        run.font.size = Pt(12)

    add_page_break(document)

    # =========================================================
    # LIST OF TABLES
    # =========================================================

    add_center_heading(
        document,
        "LIST OF TABLES",
        14
    )

    tables = [
        "Table 1: Organization Information",
        "Table 2: Daily Activities",
        "Table 3: Skills Acquired",
    ]

    for item in tables:
        add_body_paragraph(
            document,
            item
        )

    add_page_break(document)

    # =========================================================
    # LIST OF FIGURES
    # =========================================================

    add_center_heading(
        document,
        "LIST OF FIGURES",
        14
    )

    figures = [
        "Figure 1: Historical Background",
        "Figure 2: Organization Structure",
        "Figure 3: Field Activities",
    ]

    for item in figures:
        add_body_paragraph(
            document,
            item
        )

    add_page_break(document)

    # =========================================================
    # ABBREVIATIONS
    # =========================================================

    add_center_heading(
        document,
        "ABBREVIATIONS",
        14
    )

    abbreviation_table = document.add_table(
        rows=1,
        cols=2
    )

    abbreviation_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    abbreviation_table.style = "Table Grid"

    header = abbreviation_table.rows[0]

    set_cell_text(
        header.cells[0],
        "Abbreviation",
        True
    )

    set_cell_text(
        header.cells[1],
        "Meaning",
        True
    )

    set_cell_shading(header.cells[0])
    set_cell_shading(header.cells[1])

    set_repeat_table_header(header)

    abbreviations = [
        ("FPT", "Field Practical Training"),
        ("ICT", "Information and Communication Technology"),
    ]

    for abbreviation, meaning in abbreviations:

        row = abbreviation_table.add_row()

        set_cell_text(
            row.cells[0],
            abbreviation
        )

        set_cell_text(
            row.cells[1],
            meaning
        )

    add_page_break(document)

    # =========================================================
    # CHAPTER ONE
    # =========================================================

    add_center_heading(
        document,
        "CHAPTER ONE",
        15
    )

    add_center_heading(
        document,
        "INTRODUCTION",
        14
    )

    # ---------------------------------------------------------
    # 1.1
    # ---------------------------------------------------------

    add_heading(
        document,
        "1.1 Background of Industry/Organization",
        2
    )

    background = getattr(
        placement,
        "organization_description",
        ""
    )

    if not background:

        background = (
            f"{organization} provided an environment where "
            "the student was able to acquire practical "
            "knowledge and experience related to the field "
            "of study."
        )

    add_body_paragraph(
        document,
        background
    )

    # ---------------------------------------------------------
    # 1.2
    # ---------------------------------------------------------

    add_heading(
        document,
        "1.2 Organization Structure",
        2
    )

    structure = getattr(
        placement,
        "organization_structure",
        ""
    )

    if structure:

        add_body_paragraph(
            document,
            structure
        )

    else:

        add_body_paragraph(
            document,
            "The organization structure consists of different "
            "departments and personnel who work together to "
            "achieve the organization's objectives."
        )

    # ---------------------------------------------------------
    # 1.3
    # ---------------------------------------------------------

    add_heading(
        document,
        "1.3 Vision, Mission and Objectives",
        2
    )

    vision = getattr(
        placement,
        "vision",
        ""
    )

    mission = getattr(
        placement,
        "mission",
        ""
    )

    if vision:

        add_heading(
            document,
            "Vision",
            2
        )

        add_body_paragraph(
            document,
            vision
        )

    if mission:

        add_heading(
            document,
            "Mission",
            2
        )

        add_body_paragraph(
            document,
            mission
        )

    objectives = getattr(
        placement,
        "objectives",
        ""
    )

    if objectives:

        add_heading(
            document,
            "Objectives",
            2
        )

        for objective in str(objectives).splitlines():

            objective = objective.strip()

            if objective:

                paragraph = document.add_paragraph(
                    style="List Number"
                )

                run = paragraph.add_run(
                    objective
                )

                run.font.name = "Times New Roman"
                run.font.size = Pt(12)

    add_page_break(document)

    # =========================================================
    # CHAPTER TWO
    # =========================================================

    add_center_heading(
        document,
        "CHAPTER TWO",
        15
    )

    add_center_heading(
        document,
        "ACTIVITIES PERFORMED",
        14
    )

    # ---------------------------------------------------------
    # 2.1
    # ---------------------------------------------------------

    add_heading(
        document,
        "2.1 Overview",
        2
    )

    add_body_paragraph(
        document,
        "During the field practical training period, "
        "various activities were performed in order to "
        "develop practical skills, professional experience "
        "and a better understanding of the working environment."
    )

    # ---------------------------------------------------------
    # 2.2
    # ---------------------------------------------------------

    add_heading(
        document,
        "2.2 Daily Activities",
        2
    )

    # Daily activities table

    table = document.add_table(
        rows=1,
        cols=5
    )

    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    headers = [
        "Date",
        "Activity",
        "Skills Learned",
        "Challenges",
        "Solutions",
    ]

    header_row = table.rows[0]

    for index, header_text in enumerate(headers):

        set_cell_text(
            header_row.cells[index],
            header_text,
            True
        )

        set_cell_shading(
            header_row.cells[index]
        )

    set_repeat_table_header(header_row)

    for report in reports:

        row = table.add_row()

        date_value = getattr(
            report,
            "date",
            None
        )

        date_text = (
            date_value.strftime("%d %B %Y")
            if date_value
            else ""
        )

        set_cell_text(
            row.cells[0],
            date_text
        )

        set_cell_text(
            row.cells[1],
            getattr(report, "activities", "")
        )

        set_cell_text(
            row.cells[2],
            getattr(report, "skills_learned", "")
        )

        set_cell_text(
            row.cells[3],
            getattr(report, "challenges", "")
        )

        set_cell_text(
            row.cells[4],
            getattr(report, "solutions", "")
        )

    # ---------------------------------------------------------
    # 2.3
    # ---------------------------------------------------------

    add_page_break(document)

    add_heading(
        document,
        "2.3 General Observations",
        2
    )

    observations = getattr(
        placement,
        "general_observations",
        ""
    )

    if observations:

        add_body_paragraph(
            document,
            observations
        )

    else:

        add_body_paragraph(
            document,
            "The field practical training provided an "
            "opportunity to observe professional practices, "
            "workplace procedures and the application of "
            "theoretical knowledge in practical situations."
        )

    # ---------------------------------------------------------
    # 2.4
    # ---------------------------------------------------------

    add_heading(
        document,
        "2.4 Challenges Encountered",
        2
    )

    challenges = getattr(
        placement,
        "challenges",
        ""
    )

    if challenges:

        add_body_paragraph(
            document,
            challenges
        )

    else:

        add_body_paragraph(
            document,
            "Some challenges were encountered during the "
            "training period. These challenges provided "
            "opportunities for learning and problem solving."
        )

    # ---------------------------------------------------------
    # 2.5
    # ---------------------------------------------------------

    add_heading(
        document,
        "2.5 How Challenges Were Solved",
        2
    )

    solutions = getattr(
        placement,
        "solutions",
        ""
    )

    if solutions:

        add_body_paragraph(
            document,
            solutions
        )

    else:

        add_body_paragraph(
            document,
            "The challenges were addressed through guidance "
            "from supervisors, consultation with colleagues, "
            "research and practical problem-solving."
        )

    add_page_break(document)

    # =========================================================
    # CHAPTER THREE
    # =========================================================

    add_center_heading(
        document,
        "CHAPTER THREE",
        15
    )

    add_heading(
        document,
        "3.1 Conclusion",
        2
    )

    conclusion = getattr(
        placement,
        "conclusion",
        ""
    )

    if conclusion:

        add_body_paragraph(
            document,
            conclusion
        )

    else:

        add_body_paragraph(
            document,
            "The field practical training was an important "
            "part of the student's academic development. "
            "It provided practical exposure and enabled the "
            "student to connect classroom knowledge with "
            "real workplace activities."
        )

    add_heading(
        document,
        "3.2 Recommendations",
        2
    )

    recommendations = getattr(
        placement,
        "recommendations",
        ""
    )

    if recommendations:

        add_body_paragraph(
            document,
            recommendations
        )

    else:

        add_body_paragraph(
            document,
            "Students should be given sufficient practical "
            "exposure and continuous guidance throughout "
            "their field practical training."
        )

    add_heading(
        document,
        "3.3 Skills and Knowledge Acquired",
        2
    )

    skills = set()

    for report in reports:

        value = getattr(
            report,
            "skills_learned",
            ""
        )

        if value:

            for line in str(value).splitlines():

                line = line.strip()

                if line:
                    skills.add(line)

    if skills:

        for skill in sorted(skills):

            paragraph = document.add_paragraph(
                style="List Bullet"
            )

            run = paragraph.add_run(skill)

            run.font.name = "Times New Roman"
            run.font.size = Pt(12)

    else:

        add_body_paragraph(
            document,
            "Various technical, communication, teamwork and "
            "problem-solving skills were acquired during the "
            "field practical training."
        )

    # =========================================================
    # REFERENCES
    # =========================================================

    add_page_break(document)

    add_center_heading(
        document,
        "REFERENCES",
        14
    )

    references = getattr(
        placement,
        "references",
        ""
    )

    if references:

        for reference in str(references).splitlines():

            reference = reference.strip()

            if reference:

                add_body_paragraph(
                    document,
                    reference
                )

    else:

        add_body_paragraph(
            document,
            "References used during the preparation of this report."
        )

    # =========================================================
    # APPENDICES
    # =========================================================

    add_page_break(document)

    add_center_heading(
        document,
        "APPENDICES",
        14
    )

    additional_info = getattr(
        placement,
        "additional_information",
        ""
    )

    if additional_info:

        add_body_paragraph(
            document,
            additional_info
        )

    else:

        add_body_paragraph(
            document,
            "Supporting materials and additional information "
            "related to the field practical training are "
            "included in this section."
        )

    return document



@login_required(login_url="home")
@require_POST
def download_field_report_docx(request, id):

    placement = get_object_or_404(
        FieldPlacement,
        id=id
    )

    # =========================================================
    # SECURITY
    # =========================================================

    if placement.student != request.user:

        return JsonResponse(
            {
                "success": False,
                "message": "You are not authorized to download this report."
            },
            status=403
        )

    # =========================================================
    # DAILY REPORTS
    # =========================================================

    reports = (
        placement.daily_reports
        .all()
        .order_by("date", "id")
    )

    try:

        document = build_field_report_docx(
            placement,
            reports
        )

        # Save DOCX into memory
        buffer = BytesIO()

        document.save(buffer)

        buffer.seek(0)

        response = HttpResponse(
            buffer.getvalue(),
            content_type=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            )
        )

        response["Content-Disposition"] = (
            'attachment; '
            'filename="Field_Practical_Training_Report.docx"'
        )

        return response

    except Exception as e:

        return JsonResponse(
            {
                "success": False,
                "message": (
                    "Failed to generate DOCX report."
                ),
                "error": str(e),
            },
            status=500
        )





# Construction message
@login_required(login_url="home")
def construction_message(request):
    return render(request, 'wait_message.html')