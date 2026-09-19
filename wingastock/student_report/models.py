from django.db import models
from django.contrib.auth.models import User


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

    report_html = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report - {self.placement}"