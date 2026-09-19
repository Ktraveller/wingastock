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




# Download report
@login_required(login_url="home")
@require_POST
def download_field_report_docx(request, id):

    try:

        # =========================================================
        # GET PLACEMENT
        # =========================================================

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
                    "message": (
                        "You are not authorized to "
                        "download this report."
                    )
                },
                status=403
            )

        # =========================================================
        # GET SAVED REPORT
        # =========================================================

        saved_report = GeneratedFieldReport.objects.filter(
            placement=placement
        ).first()

        if (
            not saved_report
            or not saved_report.report_html.strip()
        ):

            return JsonResponse(
                {
                    "success": False,
                    "message": (
                        "Please save the report "
                        "before downloading it."
                    )
                },
                status=400
            )

        # =========================================================
        # CREATE DOCUMENT
        # =========================================================

        document = Document()

        # =========================================================
        # A4 PAGE
        # =========================================================

        section = document.sections[0]

        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)

        # These match the web template approximately:
        #
        # Web:
        # padding: 25mm 22mm
        #
        # Word:
        # 25mm top/bottom
        # 22mm left/right

        section.top_margin = Inches(25 / 25.4)
        section.bottom_margin = Inches(25 / 25.4)

        section.left_margin = Inches(22 / 25.4)
        section.right_margin = Inches(22 / 25.4)

        # =========================================================
        # DEFAULT DOCUMENT FONT
        # =========================================================

        normal_style = document.styles["Normal"]

        normal_style.font.name = "Times New Roman"
        normal_style.font.size = Pt(12)

        # Make East Asian font Times New Roman too
        normal_style._element.rPr.rFonts.set(
            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ascii",
            "Times New Roman"
        )

        normal_style._element.rPr.rFonts.set(
            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hAnsi",
            "Times New Roman"
        )

        # =========================================================
        # PARSE HTML
        # =========================================================

        soup = BeautifulSoup(
            saved_report.report_html,
            "html.parser"
        )

        # Remove web-only elements
        for element in soup.find_all(
            [
                "script",
                "style",
                "button",
                "input",
                "textarea",
                "select"
            ]
        ):

            element.decompose()

        # =========================================================
        # CSS HELPER
        # =========================================================

        def parse_style(element):

            style = element.get(
                "style",
                ""
            )

            result = {}

            for item in style.split(";"):

                if ":" not in item:
                    continue

                key, value = item.split(
                    ":",
                    1
                )

                result[
                    key.strip().lower()
                ] = value.strip().lower()

            return result

        # =========================================================
        # LENGTH CONVERTER
        # =========================================================

        def css_to_pt(value, default=12):

            if not value:
                return default

            value = str(value).strip().lower()

            try:

                if value.endswith("pt"):
                    return float(
                        value.replace("pt", "")
                    )

                if value.endswith("px"):
                    return float(
                        value.replace("px", "")
                    ) * 0.75

                if value.endswith("em"):
                    return float(
                        value.replace("em", "")
                    ) * 12

                if value.endswith("rem"):
                    return float(
                        value.replace("rem", "")
                    ) * 12

                if value.endswith("mm"):
                    return float(
                        value.replace("mm", "")
                    ) * 2.83465

                if value.endswith("cm"):
                    return float(
                        value.replace("cm", "")
                    ) * 28.3465

                return float(value)

            except:

                return default

        # =========================================================
        # COLOR CONVERTER
        # =========================================================

        def css_color(value):

            if not value:
                return None

            value = value.strip().lower()

            # Common colors
            colors = {
                "black": "000000",
                "white": "FFFFFF",
                "red": "FF0000",
                "blue": "0000FF",
                "green": "008000",
                "gray": "808080",
                "grey": "808080",
                "transparent": None,
            }

            if value in colors:
                return colors[value]

            # HEX
            if value.startswith("#"):

                value = value[1:]

                if len(value) == 3:

                    value = "".join(
                        char * 2
                        for char in value
                    )

                if len(value) == 6:
                    return value.upper()

            # rgb(...)
            if value.startswith("rgb("):

                try:

                    numbers = (
                        value
                        .replace("rgb(", "")
                        .replace(")", "")
                        .split(",")
                    )

                    r = int(numbers[0].strip())
                    g = int(numbers[1].strip())
                    b = int(numbers[2].strip())

                    return (
                        f"{r:02X}"
                        f"{g:02X}"
                        f"{b:02X}"
                    )

                except:
                    pass

            return None

        # =========================================================
        # SET RUN FONT
        # =========================================================

        def configure_run(
            run,
            bold=False,
            italic=False,
            underline=False,
            font_size=12,
            font_name="Times New Roman",
            color=None
        ):

            run.font.name = font_name
            run.font.size = Pt(font_size)

            run.bold = bold
            run.italic = italic
            run.underline = underline

            if color:

                try:
                    run.font.color.rgb = (
                        __import__(
                            "docx"
                        ).shared.RGBColor.from_string(
                            color
                        )
                    )

                except:
                    pass

            # Ensure Word uses the same font
            run._element.rPr.rFonts.set(
                "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ascii",
                font_name
            )

            run._element.rPr.rFonts.set(
                "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hAnsi",
                font_name
            )

        # =========================================================
        # INLINE CONTENT
        # =========================================================

        def add_inline_content(
            paragraph,
            element,
            inherited_bold=False,
            inherited_italic=False,
            inherited_underline=False,
            inherited_size=12,
            inherited_color=None
        ):

            # -----------------------------------------------------
            # Plain text
            # -----------------------------------------------------

            if isinstance(
                element,
                NavigableString
            ):

                text = str(element)

                if not text:
                    return

                run = paragraph.add_run(
                    text
                )

                configure_run(
                    run,
                    bold=inherited_bold,
                    italic=inherited_italic,
                    underline=inherited_underline,
                    font_size=inherited_size,
                    color=inherited_color
                )

                return

            # -----------------------------------------------------
            # Invalid element
            # -----------------------------------------------------

            if not isinstance(
                element,
                Tag
            ):
                return

            tag = element.name.lower()

            # -----------------------------------------------------
            # Ignore web elements
            # -----------------------------------------------------

            if tag in [
                "script",
                "style",
                "button",
                "input",
                "textarea",
                "select"
            ]:
                return

            # -----------------------------------------------------
            # Line break
            # -----------------------------------------------------

            if tag == "br":

                paragraph.add_run().add_break()

                return

            # -----------------------------------------------------
            # Image
            # -----------------------------------------------------

            if tag == "img":

                # Images can be added here if the HTML contains
                # local file URLs or accessible image files.
                #
                # We intentionally don't download remote images
                # here because report images are not required
                # for the document structure.

                return

            # -----------------------------------------------------
            # Tag formatting
            # -----------------------------------------------------

            bold = inherited_bold
            italic = inherited_italic
            underline = inherited_underline

            if tag in [
                "strong",
                "b"
            ]:

                bold = True

            if tag in [
                "em",
                "i"
            ]:

                italic = True

            if tag == "u":

                underline = True

            # -----------------------------------------------------
            # Inline CSS
            # -----------------------------------------------------

            styles = parse_style(
                element
            )

            if (
                styles.get("font-weight")
                in [
                    "bold",
                    "700",
                    "800",
                    "900"
                ]
            ):

                bold = True

            if (
                styles.get("font-style")
                == "italic"
            ):

                italic = True

            if (
                "underline"
                in styles.get(
                    "text-decoration",
                    ""
                )
            ):

                underline = True

            size = inherited_size

            if styles.get(
                "font-size"
            ):

                size = css_to_pt(
                    styles.get(
                        "font-size"
                    ),
                    inherited_size
                )

            color = inherited_color

            if styles.get(
                "color"
            ):

                color = css_color(
                    styles.get(
                        "color"
                    )
                )

            # -----------------------------------------------------
            # Children
            # -----------------------------------------------------

            for child in element.children:

                add_inline_content(
                    paragraph,
                    child,
                    inherited_bold=bold,
                    inherited_italic=italic,
                    inherited_underline=underline,
                    inherited_size=size,
                    inherited_color=color
                )

        # =========================================================
        # APPLY PARAGRAPH STYLE
        # =========================================================

        def apply_paragraph_style(
            paragraph,
            element
        ):

            styles = parse_style(
                element
            )

            # -----------------------------------------------------
            # Alignment
            # -----------------------------------------------------

            alignment = styles.get(
                "text-align"
            )

            if not alignment:

                classes = " ".join(
                    element.get(
                        "class",
                        []
                    )
                ).lower()

                if "center" in classes:
                    alignment = "center"

                elif "right" in classes:
                    alignment = "right"

                elif "justify" in classes:
                    alignment = "justify"

            if alignment == "center":

                paragraph.alignment = (
                    WD_ALIGN_PARAGRAPH.CENTER
                )

            elif alignment == "right":

                paragraph.alignment = (
                    WD_ALIGN_PARAGRAPH.RIGHT
                )

            elif alignment == "justify":

                paragraph.alignment = (
                    WD_ALIGN_PARAGRAPH.JUSTIFY
                )

            else:

                paragraph.alignment = (
                    WD_ALIGN_PARAGRAPH.LEFT
                )

            # -----------------------------------------------------
            # Line height
            # -----------------------------------------------------

            line_height = styles.get(
                "line-height"
            )

            if line_height:

                if line_height == "normal":

                    paragraph.paragraph_format.line_spacing = 1.0

                elif line_height.endswith("px"):

                    px = css_to_pt(
                        line_height
                    )

                    paragraph.paragraph_format.line_spacing = (
                        px / 12
                    )

                elif line_height.endswith("pt"):

                    pt_value = css_to_pt(
                        line_height
                    )

                    paragraph.paragraph_format.line_spacing = (
                        pt_value / 12
                    )

                else:

                    try:

                        paragraph.paragraph_format.line_spacing = (
                            float(
                                line_height
                            )
                        )

                    except:
                        pass

            else:

                # Matches:
                # line-height: 1.6

                paragraph.paragraph_format.line_spacing = 1.6

            # -----------------------------------------------------
            # Margin top
            # -----------------------------------------------------

            if styles.get(
                "margin-top"
            ):

                paragraph.paragraph_format.space_before = Pt(
                    css_to_pt(
                        styles.get(
                            "margin-top"
                        ),
                        0
                    )
                )

            # -----------------------------------------------------
            # Margin bottom
            # -----------------------------------------------------

            if styles.get(
                "margin-bottom"
            ):

                paragraph.paragraph_format.space_after = Pt(
                    css_to_pt(
                        styles.get(
                            "margin-bottom"
                        ),
                        0
                    )
                )

            # -----------------------------------------------------
            # Text indentation
            # -----------------------------------------------------

            if styles.get(
                "text-indent"
            ):

                paragraph.paragraph_format.first_line_indent = (
                    Inches(
                        css_to_pt(
                            styles.get(
                                "text-indent"
                            ),
                            0
                        ) / 72
                    )
                )

        # =========================================================
        # CREATE PARAGRAPH
        # =========================================================

        def create_paragraph(
            element,
            default_size=12
        ):

            paragraph = document.add_paragraph()

            apply_paragraph_style(
                paragraph,
                element
            )

            add_inline_content(
                paragraph,
                element,
                inherited_size=default_size
            )

            return paragraph

        # =========================================================
        # CREATE HEADING
        # =========================================================

        def create_heading(
            element
        ):

            tag = element.name.lower()

            sizes = {
                "h1": 20,
                "h2": 18,
                "h3": 16,
                "h4": 14,
                "h5": 12,
                "h6": 12
            }

            size = sizes.get(
                tag,
                12
            )

            paragraph = document.add_paragraph()

            apply_paragraph_style(
                paragraph,
                element
            )

            # If HTML doesn't specify alignment,
            # preserve common heading behavior.

            styles = parse_style(
                element
            )

            if "text-align" not in styles:

                paragraph.alignment = (
                    WD_ALIGN_PARAGRAPH.LEFT
                )

            add_inline_content(
                paragraph,
                element,
                inherited_bold=True,
                inherited_size=size
            )

            return paragraph

        # =========================================================
        # CREATE TABLE
        # =========================================================

        def create_table(
            element
        ):

            rows = element.find_all(
                "tr"
            )

            if not rows:
                return

            max_columns = 0

            for row in rows:

                cells = row.find_all(
                    [
                        "td",
                        "th"
                    ],
                    recursive=False
                )

                max_columns = max(
                    max_columns,
                    len(cells)
                )

            if max_columns == 0:
                return

            table = document.add_table(
                rows=len(rows),
                cols=max_columns
            )

            table.style = "Table Grid"

            # -----------------------------------------------------
            # Process cells
            # -----------------------------------------------------

            for row_index, row in enumerate(rows):

                cells = row.find_all(
                    [
                        "td",
                        "th"
                    ],
                    recursive=False
                )

                for col_index, cell in enumerate(cells):

                    if col_index >= max_columns:
                        continue

                    word_cell = table.cell(
                        row_index,
                        col_index
                    )

                    # Clear default text
                    word_cell.text = ""

                    paragraph = (
                        word_cell.paragraphs[0]
                    )

                    apply_paragraph_style(
                        paragraph,
                        cell
                    )

                    # Header cells
                    is_header = (
                        cell.name.lower()
                        == "th"
                    )

                    add_inline_content(
                        paragraph,
                        cell,
                        inherited_bold=is_header,
                        inherited_size=11
                    )

            # -----------------------------------------------------
            # Keep table together when possible
            # -----------------------------------------------------

            for row in table.rows:

                for cell in row.cells:

                    for paragraph in cell.paragraphs:

                        paragraph.paragraph_format.space_after = Pt(2)
                        paragraph.paragraph_format.line_spacing = 1.0

            return table

        # =========================================================
        # CREATE LIST
        # =========================================================

        def create_list(
            element,
            ordered=False
        ):

            items = element.find_all(
                "li",
                recursive=False
            )

            for item in items:

                paragraph = document.add_paragraph()

                paragraph.style = (
                    "List Number"
                    if ordered
                    else "List Bullet"
                )

                paragraph.paragraph_format.line_spacing = 1.6

                add_inline_content(
                    paragraph,
                    item
                )

        # =========================================================
        # CREATE BLOCKQUOTE
        # =========================================================

        def create_blockquote(
            element
        ):

            paragraph = document.add_paragraph()

            paragraph.paragraph_format.left_indent = (
                Inches(0.5)
            )

            paragraph.paragraph_format.line_spacing = 1.6

            add_inline_content(
                paragraph,
                element
            )

            return paragraph

        # =========================================================
        # PROCESS ELEMENT
        # =========================================================

        def process_element(
            element
        ):

            if not isinstance(
                element,
                Tag
            ):
                return

            tag = element.name.lower()

            # -----------------------------------------------------
            # Ignore
            # -----------------------------------------------------

            if tag in [
                "script",
                "style",
                "button",
                "input",
                "textarea",
                "select"
            ]:
                return

            # -----------------------------------------------------
            # Table
            # -----------------------------------------------------

            if tag == "table":

                create_table(
                    element
                )

                return

            # -----------------------------------------------------
            # Headings
            # -----------------------------------------------------

            if tag in [
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6"
            ]:

                create_heading(
                    element
                )

                return

            # -----------------------------------------------------
            # Paragraph
            # -----------------------------------------------------

            if tag == "p":

                create_paragraph(
                    element
                )

                return

            # -----------------------------------------------------
            # Lists
            # -----------------------------------------------------

            if tag == "ul":

                create_list(
                    element,
                    ordered=False
                )

                return

            if tag == "ol":

                create_list(
                    element,
                    ordered=True
                )

                return

            # -----------------------------------------------------
            # Blockquote
            # -----------------------------------------------------

            if tag == "blockquote":

                create_blockquote(
                    element
                )

                return

            # -----------------------------------------------------
            # DIV / SECTION / ARTICLE
            # -----------------------------------------------------

            if tag in [
                "div",
                "section",
                "article",
                "main"
            ]:

                children = list(
                    element.children
                )

                has_block_children = False

                for child in children:

                    if not isinstance(
                        child,
                        Tag
                    ):
                        continue

                    child_tag = (
                        child.name.lower()
                    )

                    if child_tag in [
                        "p",
                        "h1",
                        "h2",
                        "h3",
                        "h4",
                        "h5",
                        "h6",
                        "table",
                        "ul",
                        "ol",
                        "blockquote",
                        "div",
                        "section",
                        "article"
                    ]:

                        has_block_children = True

                        process_element(
                            child
                        )

                # If it contains only text
                if not has_block_children:

                    text = element.get_text(
                        strip=False
                    )

                    if text.strip():

                        create_paragraph(
                            element
                        )

                return

            # -----------------------------------------------------
            # Other block elements
            # -----------------------------------------------------

            if tag in [
                "header",
                "footer",
                "address"
            ]:

                create_paragraph(
                    element
                )

                return

            # -----------------------------------------------------
            # Fallback
            # -----------------------------------------------------

            text = element.get_text(
                strip=False
            )

            if text.strip():

                create_paragraph(
                    element
                )

        # =========================================================
        # PROCESS REPORT PAGES
        # =========================================================

        report_pages = soup.select(
            ".report-page"
        )

        if report_pages:

            for page_index, page in enumerate(
                report_pages
            ):

                # -------------------------------------------------
                # Every .report-page in the web template becomes
                # one Word page.
                # -------------------------------------------------

                if page_index > 0:

                    document.add_page_break()

                # -------------------------------------------------
                # Process only direct children
                # -------------------------------------------------

                for element in page.children:

                    if not isinstance(
                        element,
                        Tag
                    ):
                        continue

                    process_element(
                        element
                    )

        else:

            # =====================================================
            # FALLBACK
            # =====================================================

            body = soup.body

            if body:

                for element in body.children:

                    if not isinstance(
                        element,
                        Tag
                    ):
                        continue

                    process_element(
                        element
                    )

            else:

                for element in soup.children:

                    if not isinstance(
                        element,
                        Tag
                    ):
                        continue

                    process_element(
                        element
                    )

        # =========================================================
        # REMOVE EMPTY FINAL PARAGRAPH IF POSSIBLE
        # =========================================================

        # Word always keeps a final paragraph internally,
        # so we don't aggressively remove it.

        # =========================================================
        # SAVE
        # =========================================================

        output = BytesIO()

        document.save(
            output
        )

        output.seek(0)

        # =========================================================
        # RESPONSE
        # =========================================================

        response = HttpResponse(
            output.getvalue(),
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

        print(
            "DOCX GENERATION ERROR:",
            repr(e)
        )

        return JsonResponse(
            {
                "success": False,
                "message": (
                    "Unable to create the Word document."
                ),
                "error": str(e)
            },
            status=500
        )