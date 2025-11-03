from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, ListingImage
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates sample listings for testing'

    def handle(self, *args, **kwargs):
        # Create a sample host user if doesn't exist
        host, created = User.objects.get_or_create(
            username='samplehost',
            defaults={
                'email': 'host@example.com',
                'user_type': 'host',
                'is_verified': True
            }
        )
        
        if created:
            host.set_password('password123')
            host.save()
            self.stdout.write(self.style.SUCCESS('Created sample host user'))

        # Sample listing data
        sample_listings = [
            {
                'title': 'Luxury Beachfront Villa with Private Pool',
                'description': 'Wake up to stunning ocean views in this modern beachfront villa. Features include a private infinity pool, spacious living areas, and direct beach access. Perfect for families or groups looking for a luxurious getaway.',
                'property_type': 'villa',
                'city': 'Miami',
                'state': 'Florida',
                'country': 'United States',
                'bedrooms': 4,
                'bathrooms': Decimal('3.5'),
                'guests': 8,
                'price_per_night': Decimal('450.00'),
                'wifi': True,
                'pool': True,
                'parking': True,
                'air_conditioning': True,
                'kitchen': True,
            },
            {
                'title': 'Modern Downtown Loft with City Views',
                'description': 'Stylish loft apartment in the heart of downtown. Floor-to-ceiling windows offer panoramic city views. Walking distance to restaurants, bars, and entertainment. Ideal for business travelers or couples.',
                'property_type': 'apartment',
                'city': 'New York',
                'state': 'New York',
                'country': 'United States',
                'bedrooms': 2,
                'bathrooms': Decimal('2.0'),
                'guests': 4,
                'price_per_night': Decimal('280.00'),
                'wifi': True,
                'gym': True,
                'parking': True,
                'air_conditioning': True,
                'heating': True,
                'tv': True,
            },
            {
                'title': 'Cozy Mountain Cabin with Fireplace',
                'description': 'Escape to the mountains in this charming cabin. Features a wood-burning fireplace, mountain views, and a hot tub on the deck. Perfect for romantic getaways or family retreats.',
                'property_type': 'cabin',
                'city': 'Aspen',
                'state': 'Colorado',
                'country': 'United States',
                'bedrooms': 3,
                'bathrooms': Decimal('2.0'),
                'guests': 6,
                'price_per_night': Decimal('320.00'),
                'wifi': True,
                'heating': True,
                'parking': True,
                'kitchen': True,
                'tv': True,
            },
            {
                'title': 'Spacious Family Home with Backyard',
                'description': 'Beautiful family home with a large backyard, perfect for kids and pets. Modern kitchen, comfortable living spaces, and close to schools and parks. Great for extended stays.',
                'property_type': 'house',
                'city': 'Austin',
                'state': 'Texas',
                'country': 'United States',
                'bedrooms': 4,
                'bathrooms': Decimal('3.0'),
                'guests': 8,
                'price_per_night': Decimal('220.00'),
                'wifi': True,
                'parking': True,
                'air_conditioning': True,
                'kitchen': True,
                'tv': True,
            },
            {
                'title': 'Ocean View Studio Apartment',
                'description': 'Compact yet comfortable studio with breathtaking ocean views. Perfect for solo travelers or couples. Includes a small kitchenette and balcony overlooking the beach.',
                'property_type': 'studio',
                'city': 'Malibu',
                'state': 'California',
                'country': 'United States',
                'bedrooms': 1,
                'bathrooms': Decimal('1.0'),
                'guests': 2,
                'price_per_night': Decimal('180.00'),
                'wifi': True,
                'parking': True,
                'air_conditioning': True,
                'kitchen': True,
            },
            {
                'title': 'Historic Cottage in Wine Country',
                'description': 'Charming historic cottage surrounded by vineyards. Restored with modern amenities while maintaining its rustic charm. Walking distance to wineries and tasting rooms.',
                'property_type': 'cottage',
                'city': 'Napa',
                'state': 'California',
                'country': 'United States',
                'bedrooms': 2,
                'bathrooms': Decimal('1.5'),
                'guests': 4,
                'price_per_night': Decimal('260.00'),
                'wifi': True,
                'parking': True,
                'kitchen': True,
                'heating': True,
                'tv': True,
            },
            {
                'title': 'Luxury Penthouse with Rooftop Terrace',
                'description': 'Exclusive penthouse with private rooftop terrace and 360-degree city views. Features high-end appliances, designer furniture, and concierge service. Ultimate luxury living.',
                'property_type': 'apartment',
                'city': 'Los Angeles',
                'state': 'California',
                'country': 'United States',
                'bedrooms': 3,
                'bathrooms': Decimal('3.0'),
                'guests': 6,
                'price_per_night': Decimal('550.00'),
                'wifi': True,
                'gym': True,
                'pool': True,
                'parking': True,
                'air_conditioning': True,
                'kitchen': True,
                'tv': True,
            },
            {
                'title': 'Lakefront Villa with Private Dock',
                'description': 'Stunning lakefront property with private dock and boat included. Spacious deck for entertaining, modern interior, and water sports equipment available. Paradise for water lovers.',
                'property_type': 'villa',
                'city': 'Lake Tahoe',
                'state': 'California',
                'country': 'United States',
                'bedrooms': 5,
                'bathrooms': Decimal('4.0'),
                'guests': 10,
                'price_per_night': Decimal('480.00'),
                'wifi': True,
                'pool': False,
                'parking': True,
                'heating': True,
                'kitchen': True,
                'tv': True,
            },
            {
                'title': 'Minimalist City Apartment',
                'description': 'Clean, modern apartment with minimalist design. Located in trendy neighborhood with easy access to public transportation. Perfect for young professionals or couples.',
                'property_type': 'apartment',
                'city': 'San Francisco',
                'state': 'California',
                'country': 'United States',
                'bedrooms': 1,
                'bathrooms': Decimal('1.0'),
                'guests': 2,
                'price_per_night': Decimal('150.00'),
                'wifi': True,
                'parking': False,
                'air_conditioning': True,
                'heating': True,
                'kitchen': True,
            },
            {
                'title': 'Tropical Paradise Villa with Pool',
                'description': 'Experience paradise in this tropical villa. Lush gardens, private pool, outdoor shower, and tropical décor throughout. Close to beaches and local attractions.',
                'property_type': 'villa',
                'city': 'Honolulu',
                'state': 'Hawaii',
                'country': 'United States',
                'bedrooms': 3,
                'bathrooms': Decimal('2.5'),
                'guests': 6,
                'price_per_night': Decimal('380.00'),
                'wifi': True,
                'pool': True,
                'parking': True,
                'air_conditioning': True,
                'kitchen': True,
                'tv': True,
            },
        ]

        created_count = 0
        for listing_data in sample_listings:
            # Add common fields
            listing_data.update({
                'host': host,
                'street_address': f'{random.randint(100, 9999)} Main Street',
                'zip_code': f'{random.randint(10000, 99999)}',
                'is_active': True,
            })
            
            # Check if listing already exists
            if not Listing.objects.filter(title=listing_data['title']).exists():
                Listing.objects.create(**listing_data)
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample listings')
        )
        self.stdout.write(
            self.style.WARNING('Note: Images need to be added manually or via admin panel')
        )
        self.stdout.write(
            self.style.SUCCESS('Sample host credentials: username="samplehost", password="password123"')
        )