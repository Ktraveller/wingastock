from django.db import models
from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField




# Field placement report
class FieldPlacement(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="field_placements"
    )
    organization = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True)
    supervisor_name = models.CharField(max_length=255)
    supervisor_phone = models.CharField(max_length=30, blank=True)

    start_date = models.DateField()
    end_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.organization}"




# Daily report
class DailyFieldReport(models.Model):
    placement = models.ForeignKey(
        "FieldPlacement",
        on_delete=models.CASCADE,
        related_name="daily_reports"
    )
    date = models.DateField()

    title = models.CharField(max_length=255)
    activities = models.TextField(
        help_text="Describe the activities performed today."
    )
    skills_learned = models.TextField(
        blank=True,
        help_text="Skills or knowledge gained today."
    )
    challenges = models.TextField(
        blank=True,
        help_text="Challenges encountered during the day."
    )
    solutions = models.TextField(
        blank=True,
        help_text="How the challenges were solved."
    )
    remarks = models.TextField(blank=True)

    supervisor_comment = models.TextField(blank=True)
    supervisor_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=["placement", "date"],
                name="unique_daily_report_per_day"
            )
        ]

    def __str__(self):
        return f"{self.placement.student} - {self.date}"



# Generated report
class GeneratedFieldReport(models.Model):

    placement = models.OneToOneField(
        FieldPlacement,
        on_delete=models.CASCADE,
        related_name="generated_report"
    )

    # =========================================================
    # COMPLETE GENERATED REPORT
    # =========================================================

    report_html = models.TextField(
        blank=True
    )

    # =========================================================
    # PRELIMINARY PAGES
    # =========================================================

    declaration = models.TextField(
        blank=True
    )

    abbreviations = models.TextField(
        blank=True
    )

    # =========================================================
    # CHAPTER ONE / ORGANIZATION INFORMATION
    # =========================================================

    historical_background = models.TextField(
        blank=True
    )

    organization_structure = models.TextField(
        blank=True
    )

    vision = models.TextField(
        blank=True
    )

    mission = models.TextField(
        blank=True
    )

    objectives = models.TextField(
        blank=True
    )

    # =========================================================
    # CHAPTER TWO
    # =========================================================

    # 2.1 Brief Overview of Undertaken
    section_21_brief_overview = models.TextField(
        blank=True
    )

    # 2.2 Activities Performed
    section_22_activities_performed = models.TextField(
        blank=True
    )

    # 2.3 General Observation
    section_23_general_observation = models.TextField(
        blank=True
    )

    # 2.4 Challenges / Problems Faced
    section_24_challenges = models.TextField(
        blank=True
    )

    # 2.5 How Student Solved the Challenges
    section_25_solutions = models.TextField(
        blank=True
    )

    # =========================================================
    # OTHER REPORT SECTIONS
    # =========================================================

    conclusion = models.TextField(
        blank=True
    )

    recommendations = models.TextField(
        blank=True
    )

    references_bibliography = models.TextField(
        blank=True
    )

    # =========================================================
    # REPORT IMAGES
    # =========================================================

    historical_background_image = CloudinaryField(
        "historical background image",
        folder="field_reports",
        blank=True,
        null=True
    )

    organization_structure_image = CloudinaryField(
        "organization structure image",
        folder="field_reports",
        blank=True,
        null=True
    )

    organization_image = CloudinaryField(
        "organization image",
        folder="field_reports",
        blank=True,
        null=True
    )

    activity_image = CloudinaryField(
        "activity image",
        folder="field_reports",
        blank=True,
        null=True
    )

    appendix_image = CloudinaryField(
        "appendix image",
        folder="field_reports",
        blank=True,
        null=True
    )

    # =========================================================
    # TIMESTAMPS
    # =========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"Report - "
            f"{self.placement.student} - "
            f"{self.placement.organization}"
        )