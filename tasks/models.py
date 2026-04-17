"""
Unmanaged model — reads/writes the same 'tasks' table created by Laravel migrations.
Django will NOT create or alter this table (managed = False).
"""

from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'Todo'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
        ('OVERDUE', 'Overdue'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    due_date = models.DateField()
    project_id = models.BigIntegerField()
    assigned_to = models.BigIntegerField()
    created_by = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tasks'
        managed = False  # Django does NOT manage this table

    def __str__(self):
        return f"{self.title} ({self.status})"


class User(models.Model):
    """Read-only reference to Laravel's users table for admin verification."""
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    role = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'
        managed = False

    def __str__(self):
        return f"{self.name} ({self.role})"


class PersonalAccessToken(models.Model):
    """Read-only reference to Sanctum tokens for auth verification."""
    id = models.BigAutoField(primary_key=True)
    tokenable_type = models.CharField(max_length=255)
    tokenable_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=64)
    abilities = models.TextField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'personal_access_tokens'
        managed = False
