import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Automatically creates or updates a superuser using environment variables."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "").strip()

        if not password:
            self.stdout.write(
                self.style.WARNING(
                    "[create_admin] DJANGO_SUPERUSER_PASSWORD environment variable is not set. Skipping superuser creation."
                )
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )

        user.set_password(password)
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"[create_admin] Superuser '{username}' successfully created."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"[create_admin] Existing superuser '{username}' updated with latest password and permissions."
                )
            )
