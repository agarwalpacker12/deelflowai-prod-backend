import time
import random
import os
import django
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deelflowAI.deelflowAI.settings')
django.setup()

from deelflow.models import PropertyAIAnalysis

# Create model if not exists (migration required)
# class PropertyAIAnalysis(models.Model):
#     address = models.CharField(max_length=255)
#     ai_confidence = models.FloatField()
#     distress_level = models.FloatField()
#     motivation = models.CharField(max_length=255)
#     timeline = models.CharField(max_length=255)
#     roi_percent = models.FloatField()
#     cap_rate = models.FloatField()
#     cash_flow = models.FloatField()
#     market_stability_score = models.FloatField()
#     comparables_confidence = models.FloatField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# Prediction logic (mocked for demo)
def predict_ai_details():
    return {
        'address': '1247 Oak Street, Dallas, TX 75201',
        'ai_confidence': round(random.uniform(55, 65), 2),
        'distress_level': round(random.uniform(7, 10), 2),
        'motivation': 'High – Divorce Settlement',
        'timeline': '30–45 days',
        'roi_percent': round(random.uniform(10, 15), 2),
        'cap_rate': round(random.uniform(5, 7), 2),
        'cash_flow': round(random.uniform(500, 600), 2),
        'market_stability_score': round(random.uniform(7, 8), 2),
        'comparables_confidence': round(random.uniform(85, 95), 2),
    }


def insert_prediction():
    data = predict_ai_details()
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
    print(f"Inserted/Updated AI prediction for {obj.address} at {obj.updated_at}")


def main():
    while True:
        insert_prediction()
        time.sleep(60)  # Run every 60 seconds

if __name__ == "__main__":
    main()
