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
    # Past dates are allowed
    # ---------------------------------
    #
    # Start dates in the past are intentionally
    # allowed because the field training website
    # was launched after some students had already
    # started or completed their training.
    #
    # No date.today() restriction is applied here.

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

    # =========================================================
    # GET PLACEMENT
    # =========================================================

    placement = get_object_or_404(
        FieldPlacement,
        id=id
    )


    # =========================================================
    # AUTHORIZATION
    # =========================================================

    if placement.student != request.user:

        messages.error(
            request,
            "You are not authorized to view this report."
        )

        return redirect(
            "daily_reports",
            placement.id
        )


    # =========================================================
    # DAILY REPORTS
    # =========================================================

    reports = (
        DailyFieldReport.objects
        .filter(
            placement=placement
        )
        .order_by("-date")
    )


    # =========================================================
    # GROUP DAILY REPORTS BY WEEK
    # =========================================================

    weekly_reports = OrderedDict()

    for report in reports:

        week_start = (
            report.date
            - timedelta(
                days=report.date.weekday()
            )
        )

        week_end = (
            week_start
            + timedelta(
                days=6
            )
        )

        if week_start not in weekly_reports:

            weekly_reports[week_start] = {

                "week_start":
                    week_start,

                "week_end":
                    week_end,

                "reports":
                    []

            }

        weekly_reports[
            week_start
        ]["reports"].append(
            report
        )


    weekly_reports = list(
        weekly_reports.values()
    )


    # =========================================================
    # GET SAVED GENERATED REPORT
    # =========================================================
    #
    # GeneratedFieldReport is OneToOne with FieldPlacement.
    #
    # This contains:
    #
    # 2.1 -> section_21_brief_overview
    # 2.2 -> section_22_activities_performed
    # 2.3 -> section_23_general_observation
    # 2.4 -> section_24_challenges
    # 2.5 -> section_25_solutions
    #
    # Complete Chapter Two -> report_html
    #
    # =========================================================

    generated_report = (
        GeneratedFieldReport.objects
        .filter(
            placement=placement
        )
        .first()
    )


    # =========================================================
    # COMPLETE CHAPTER TWO
    # =========================================================

    saved_summary = ""

    if generated_report:

        saved_summary = (
            generated_report.report_html or ""
        )


    # =========================================================
    # SECTION 2.1
    # =========================================================

    saved_section_21 = ""

    if generated_report:

        saved_section_21 = (
            generated_report
            .section_21_brief_overview
            or ""
        )


    # =========================================================
    # SECTION 2.2
    # =========================================================

    saved_section_22 = ""

    if generated_report:

        saved_section_22 = (
            generated_report
            .section_22_activities_performed
            or ""
        )


    # =========================================================
    # SECTION 2.3
    # =========================================================

    saved_section_23 = ""

    if generated_report:

        saved_section_23 = (
            generated_report
            .section_23_general_observation
            or ""
        )


    # =========================================================
    # SECTION 2.4
    # =========================================================

    saved_section_24 = ""

    if generated_report:

        saved_section_24 = (
            generated_report
            .section_24_challenges
            or ""
        )


    # =========================================================
    # SECTION 2.5
    # =========================================================

    saved_section_25 = ""

    if generated_report:

        saved_section_25 = (
            generated_report
            .section_25_solutions
            or ""
        )


    # =========================================================
    # DATA SENT TO JAVASCRIPT / CHATGPT
    # =========================================================

    gpt_reports = []

    for report in reports:

        gpt_reports.append({

            "date":
                str(
                    report.date
                ),

            "title":
                report.title or "",

            "activities":
                report.activities or "",

            "skills_learned":
                report.skills_learned or "",

            "challenges":
                report.challenges or "",

            "solutions":
                report.solutions or "",

            "remarks":
                report.remarks or "",

            "supervisor_comment":
                report.supervisor_comment or "",
        })


    # =========================================================
    # RENDER TEMPLATE
    # =========================================================

    return render(
        request,
        "report_summary_re.html",
        {

            # -------------------------------------------------
            # PLACEMENT
            # -------------------------------------------------

            "placement":
                placement,


            # -------------------------------------------------
            # DAILY REPORTS
            # -------------------------------------------------

            "reports":
                reports,


            # -------------------------------------------------
            # WEEKLY REPORTS
            # -------------------------------------------------

            "weekly_reports":
                weekly_reports,


            # -------------------------------------------------
            # GENERATED REPORT
            # -------------------------------------------------

            "generated_report":
                generated_report,


            # -------------------------------------------------
            # COMPLETE CHAPTER TWO
            # -------------------------------------------------

            "saved_summary":
                saved_summary,


            # -------------------------------------------------
            # CHAPTER TWO SECTIONS
            # -------------------------------------------------

            "saved_section_21":
                saved_section_21,

            "saved_section_22":
                saved_section_22,

            "saved_section_23":
                saved_section_23,

            "saved_section_24":
                saved_section_24,

            "saved_section_25":
                saved_section_25,


            # -------------------------------------------------
            # DATA FOR CHATGPT / JAVASCRIPT
            # -------------------------------------------------

            "gpt_reports":
                gpt_reports,
        }
    )







# Save report summary
@login_required(login_url="home")
@require_POST
def save_report_summary(request, id):

    try:

        # =========================================================
        # GET PLACEMENT
        # =========================================================

        placement = get_object_or_404(
            FieldPlacement,
            id=id
        )


        # =========================================================
        # SECURITY CHECK
        # =========================================================

        if placement.student != request.user:

            return JsonResponse(
                {
                    "success": False,
                    "message": (
                        "You are not authorized "
                        "to save this report."
                    ),
                },
                status=403
            )


        # =========================================================
        # READ JSON
        # =========================================================

        try:

            data = json.loads(
                request.body
            )

        except json.JSONDecodeError:

            return JsonResponse(
                {
                    "success": False,
                    "message": "Invalid JSON data.",
                },
                status=400
            )


        # =========================================================
        # SAVE COMPLETE CHAPTER TWO
        #
        # Existing JavaScript:
        #
        # {
        #     "summary": "complete chapter two..."
        # }
        #
        # Saved into:
        #
        # GeneratedFieldReport.report_html
        # =========================================================

        if "summary" in data:

            summary = str(
                data.get(
                    "summary",
                    ""
                )
            ).strip()


            if not summary:

                return JsonResponse(
                    {
                        "success": False,
                        "message": (
                            "Please enter the complete "
                            "Chapter Two before saving."
                        ),
                    },
                    status=400
                )


            # -----------------------------------------------------
            # GET OR CREATE REPORT
            # -----------------------------------------------------

            generated_report, created = (
                GeneratedFieldReport.objects
                .get_or_create(
                    placement=placement
                )
            )


            # -----------------------------------------------------
            # SAVE COMPLETE CHAPTER TWO
            # -----------------------------------------------------

            generated_report.report_html = summary


            generated_report.save(
                update_fields=[
                    "report_html",
                    "updated_at"
                ]
            )


            return JsonResponse(
                {
                    "success": True,

                    "message": (
                        "Complete Chapter Two "
                        "saved successfully."
                    ),

                    "section":
                        "chapter_two",

                    "field":
                        "report_html",

                    "content":
                        summary,

                    "created":
                        created,
                }
            )


        # =========================================================
        # GET SECTION
        # =========================================================

        section = str(
            data.get(
                "section",
                ""
            )
        ).strip()


        if not section:

            return JsonResponse(
                {
                    "success": False,
                    "message": (
                        "Report section is required."
                    ),
                },
                status=400
            )


        # =========================================================
        # SECTION 2.5 SUPPORT
        #
        # Your NEW MODEL has:
        #
        # section_25_solutions
        #
        # Therefore Section 2.5 should save only the
        # solutions field.
        #
        # =========================================================

        if section == "2.5":

            # -----------------------------------------------------
            # Support the new normal "content" format
            #
            # {
            #     "section": "2.5",
            #     "content": "..."
            # }
            # -----------------------------------------------------

            content = str(
                data.get(
                    "content",
                    ""
                )
            ).strip()


            # -----------------------------------------------------
            # Backward compatibility
            #
            # If old JavaScript still sends:
            #
            # {
            #     "challenges": "...",
            #     "challenge_solutions": "..."
            # }
            #
            # use challenge_solutions as Section 2.5.
            # -----------------------------------------------------

            if not content:

                content = str(
                    data.get(
                        "challenge_solutions",
                        ""
                    )
                ).strip()


            if not content:

                return JsonResponse(
                    {
                        "success": False,
                        "message": (
                            "Please enter the solutions "
                            "before saving."
                        ),
                    },
                    status=400
                )


            # -----------------------------------------------------
            # GET OR CREATE REPORT
            # -----------------------------------------------------

            generated_report, created = (
                GeneratedFieldReport.objects
                .get_or_create(
                    placement=placement
                )
            )


            # -----------------------------------------------------
            # SAVE SECTION 2.5
            # -----------------------------------------------------

            generated_report.section_25_solutions = (
                content
            )


            generated_report.save(
                update_fields=[
                    "section_25_solutions",
                    "updated_at"
                ]
            )


            return JsonResponse(
                {
                    "success": True,

                    "message": (
                        "Section 2.5 solutions "
                        "saved successfully."
                    ),

                    "section":
                        section,

                    "field":
                        "section_25_solutions",

                    "content":
                        content,

                    "created":
                        created,
                }
            )


        # =========================================================
        # NORMAL SECTION MAPPING
        #
        # This matches your NEW GeneratedFieldReport model.
        # =========================================================

        allowed_sections = {

            "2.1":
                "section_21_brief_overview",

            "2.2":
                "section_22_activities_performed",

            "2.3":
                "section_23_general_observation",

            "2.4":
                "section_24_challenges",

        }


        # =========================================================
        # VALIDATE SECTION
        # =========================================================

        if section not in allowed_sections:

            return JsonResponse(
                {
                    "success": False,
                    "message": (
                        "Invalid report section."
                    ),
                },
                status=400
            )


        # =========================================================
        # GET CONTENT
        # =========================================================

        content = str(
            data.get(
                "content",
                ""
            )
        ).strip()


        # =========================================================
        # VALIDATE CONTENT
        # =========================================================

        if not content:

            return JsonResponse(
                {
                    "success": False,
                    "message": (
                        "Please enter the report "
                        "content first."
                    ),
                },
                status=400
            )


        # =========================================================
        # GET OR CREATE GENERATED REPORT
        # =========================================================

        generated_report, created = (
            GeneratedFieldReport.objects
            .get_or_create(
                placement=placement
            )
        )


        # =========================================================
        # GET DATABASE FIELD
        # =========================================================

        field_name = (
            allowed_sections[
                section
            ]
        )


        # =========================================================
        # SAVE SECTION
        #
        # 2.1 -> section_21_brief_overview
        #
        # 2.2 -> section_22_activities_performed
        #
        # 2.3 -> section_23_general_observation
        #
        # 2.4 -> section_24_challenges
        # =========================================================

        setattr(
            generated_report,
            field_name,
            content
        )


        # =========================================================
        # SAVE ONLY THE CHANGED FIELD
        # =========================================================

        generated_report.save(
            update_fields=[
                field_name,
                "updated_at"
            ]
        )


        # =========================================================
        # SUCCESS RESPONSE
        # =========================================================

        return JsonResponse(
            {
                "success": True,

                "message": (
                    f"Section {section} "
                    "saved successfully."
                ),

                "section":
                    section,

                "field":
                    field_name,

                "content":
                    content,

                "created":
                    created,
            }
        )


    # =============================================================
    # UNEXPECTED ERROR
    # =============================================================

    except Exception as e:

        return JsonResponse(
            {
                "success": False,

                "message":
                    str(e),
            },
            status=500
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






# Construction message
@login_required(login_url="home")
def construction_message(request):
    return render(request, 'wait_message.html')