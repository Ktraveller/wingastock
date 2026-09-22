from django.urls import path
from student_report.views_r.index import report_index
from student_report.views_r.reports import add_placement, placements, add_report, edit_report, reports, report_detail, report_detail_weekly, report_summary, delete_report, delete_placement, edit_placement, generate_field_report, save_field_report, download_field_report_docx, construction_message, refresh_field_report_data
from student_report.views_r.account import account_report


# Student report
urlpatterns = [
    path('', report_index, name='report_home'),

    # Placement
    path('add-placement/', add_placement, name='add_placement'),
    path('placements/', placements, name='placements_list'),


    # Reports
    path('reports/<int:id>/', reports, name='reports_list'),
    path('add-report/<int:id>/', add_report, name='add_new_report'),
    path('edit-report/<int:id>/', edit_report, name='edit_report'),
    path('report-preview/<int:id>/', report_detail, name='report_preview'),

    path('weekly-report-preview/<int:id>/', report_detail_weekly, name='report_preview_weekly'),
    path('report-summary<int:id>/', report_summary, name='report_summary'),

    path(
        "delete-report/<int:id>/",
        delete_report,
        name="delete_report"
    ),

    path(
        "delete-placement/<int:id>/",
        delete_placement,
        name="delete_placement"
    ),

    path(
        "edit-placement/<int:id>/",
        edit_placement,
        name="edit_placement"
    ),


    # Field report
    path(
        "generate-field-report/<int:id>/",
        generate_field_report,
        name="generate_field_report"
    ),

    path(
        "field-report/<int:id>/save/",
        save_field_report,
        name="save_field_report",
    ),

    path(
        "field-report/<int:id>/download-docx/",
        download_field_report_docx,
        name="download_field_report_docx",
    ),

    path(
        "field-report/<int:id>/refresh-data/",
        refresh_field_report_data,
        name="refresh_field_report_data",
    ),


    # User Account
    path('account/', account_report, name='user_account'),

    # Message
    path('construction-message/', construction_message, name="construction_message")

]