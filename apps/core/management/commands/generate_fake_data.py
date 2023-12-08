import os
import django
import random
from faker import Faker
from django.core.management.base import BaseCommand
from apps.core.models import Snack, RequestSnack, User

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))

        self.create_fake_requests()
        self.create_fake_users()

        self.stdout.write(self.style.SUCCESS('Data population completed.'))

    def create_fake_requests(self, num_requests=100):
        snack_types = [choice[0] for choice in Snack.type_choices]
        snack_status = [choice[0] for choice in RequestSnack.snack_status]

        for _ in range(num_requests):
            RequestSnack.objects.create(
                student_name=fake.name(),
                student_registration=fake.random_int(min=1000, max=9999),
                student_email="luccasraffael6@gmail.com",
                data=fake.date_between(start_date='-30d', end_date='today'),
                justification=fake.text(100),
                status="pendente",
                type=random.choice(snack_types),
                checked=False
            )

    def create_fake_users(self, num_users=20):
        for _ in range(num_users):
            User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'generate_fake_data.settings')
    django.setup()
    command = Command()
    command.handle()