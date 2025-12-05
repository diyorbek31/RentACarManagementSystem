from django.db import models

# Add account-related models here if needed (e.g., Profile)


class ExampleProfile(models.Model):
    user_identifier = models.CharField(max_length=150)

    def __str__(self):
        return self.user_identifier
