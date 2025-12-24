import os
import requests
from django.core.management import BaseCommand
from django.db import transaction
from products.models import Product

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:

            FASTAPI_URL = os.getenv('FASTAPI_URL', 'http://fastapi:8000')
            response = requests.get(f'{FASTAPI_URL}/api/v1/products/all')

            if response.status_code != 200:
                self.stderr.write(f"Error: {response.status_code}")
                return
            products = response.json()
            self.stdout.write(f"recived {len(products)} products")

            created_count = 0
            updated_count = 0

            for product in products:
                defaults = {
                    'name': product['name'],
                    'description': product['description'],
                    'price': float(product['price']),
                    'is_available': product['is_available'],
                }

                obj, created = Product.objects.get_or_create(
                    id=product['id'],
                    defaults=defaults
                )

                if created:
                    created_count += 1
                    self.stdout.write(f"created {obj.name} product")
                else:
                    updated_count += 1
                    self.stdout.write(f"updated {obj.name} product")

            self.stdout.write(f"{created_count} created product\n"
                              f" {updated_count} updated product\n"
                              f" {Product.objects.count()} all products")

        except requests.ConnectionError:
            self.stderr.write("Connection error")
        except Exception as e:
            self.stderr.write(f"Error: {e}")



