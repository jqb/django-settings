"""
Initialize default values into DB.
"""
from django.core.management.base import BaseCommand
from django_settings.dataapi import initialize_data


class Command(BaseCommand):
    help = 'Initialize default values into DB'
    args = ""

    def handle(self, **options):
        initialize_data()
