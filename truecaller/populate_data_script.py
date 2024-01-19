import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'truecaller.settings')
django.setup()

import random
from faker import Faker
from django.utils import timezone
from app.models import User, Contact


fake = Faker()

def create_fake_user():
    return User.objects.create(
        username=fake.user_name(),
        phone_number=fake.phone_number()[:14],
        email=fake.email(),
        password=fake.password(),
    )

def create_fake_contact(user):
    return Contact.objects.create(
        name=fake.name(),
        user=user,
        phone_number=fake.phone_number()[:14],
        is_spam=random.choice([True, False])
    )

def populate_data(num_users=100, contacts_per_user=8):
    for _ in range(num_users):
        try:
            user = create_fake_user()
            for _ in range(contacts_per_user):
                create_fake_contact(user)
        except:
            continue

if __name__ == "__main__":
    populate_data()
