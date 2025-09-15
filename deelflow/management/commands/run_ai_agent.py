from django.core.management.base import BaseCommand
import time
from datetime import datetime
from deelflow.models import PropertyAIAnalysis

class Command(BaseCommand):
    help = 'AI Agent: Fetches properties from resources and inserts into PropertyAIAnalysis.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('AI Agent started.'))
        while True:
            properties = self.fetch_properties_from_resources()
            self.insert_properties(properties)
            time.sleep(300)  # Run every 5 minutes

    def fetch_properties_from_resources(self):
        # TODO: Replace with actual logic to fetch property data from APIs, web scraping, etc.
        return [
            {
                'address': '1247 Oak Street, Dallas, TX 75201',
                'ai_confidence': 58.0,
                'distress_level': 8.5,
                'motivation': 'High – Divorce Settlement',
                'timeline': '30–45 days',
                'roi_percent': 12.7,
                'cap_rate': 6.2,
                'cash_flow': 540,
                'market_stability_score': 7.2,
                'comparables_confidence': 90.0,
            },
            # Add more properties here
        ]

    def insert_properties(self, properties):
        for data in properties:
            obj, created = PropertyAIAnalysis.objects.update_or_create(
                address=data['address'],
                defaults={
                    'ai_confidence': data['ai_confidence'],
                    'distress_level': data['distress_level'],
                    'motivation': data['motivation'],
                    'timeline': data['timeline'],
                    'roi_percent': data['roi_percent'],
                    'cap_rate': data['cap_rate'],
                    'cash_flow': data['cash_flow'],
                    'market_stability_score': data['market_stability_score'],
                    'comparables_confidence': data['comparables_confidence'],
                    'updated_at': datetime.now()
                }
            )
            print(f"{'Inserted' if created else 'Updated'}: {obj.address}")
