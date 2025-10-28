# Airbnb Clone - Django Project

A full-featured Airbnb clone built with Django, featuring property listings, booking management, user authentication, reviews, and a REST API.

## Features

- **User Management**
  - Custom user model with guest/host roles
  - User registration and authentication
  - Profile management with image uploads
  - User verification system

- **Property Listings**
  - Create, update, and delete listings
  - Multiple property types (apartment, house, villa, etc.)
  - Image uploads for listings
  - Search and filter functionality
  - Location-based search

- **Booking System**
  - Book properties with date selection
  - Booking validation (no overlapping dates)
  - Automatic price calculation
  - Booking status management (pending, confirmed, cancelled, completed)
  - Host and guest dashboards

- **Reviews & Ratings**
  - Multi-criteria rating system
  - Guest reviews after completed bookings
  - Host responses to reviews
  - Average rating calculation

- **REST API**
  - Full CRUD operations for all models
  - Token-based authentication
  - Filtering and search capabilities
  - Pagination support

## Tech Stack

- **Backend**: Django 4.2.7
- **Database**: PostgreSQL (configurable to SQLite)
- **API**: Django REST Framework
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **Image Processing**: Pillow
- **Forms**: Django Crispy Forms with Bootstrap 5

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL (optional, can use SQLite)
- pip

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/EbenezerBaafi/airbnbClonedApp.git
cd airbnb_clone
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the root directory:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# For PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=airbnb_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# For SQLite (comment out PostgreSQL settings above)
# DB_ENGINE=django.db.backends.sqlite3
# DB_NAME=db.sqlite3
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Collect static files**
```bash
python manage.py collectstatic
```

8. **Run development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Project Structure

```
airbnb_clone/
├── airbnb_clone/          # Project configuration
├── users/                 # User authentication & profiles
├── listings/              # Property listings
├── bookings/              # Booking management
├── reviews/               # Reviews & ratings
├── api/                   # REST API
├── templates/             # Global templates
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploaded files
└── manage.py
```

## Usage

### For Guests

1. Register an account as a "Guest" or "Both"
2. Browse available listings
3. Search by location, dates, and number of guests
4. Book a property
5. Leave reviews after your stay

### For Hosts

1. Register an account as a "Host" or "Both"
2. Create property listings
3. Upload images for your properties
4. Manage bookings from your host dashboard
5. Respond to guest reviews

## API Endpoints

The REST API is available at `/api/`:

- `GET /api/listings/` - List all listings
- `POST /api/listings/` - Create a listing (authenticated)
- `GET /api/listings/{id}/` - Retrieve a listing
- `PUT /api/listings/{id}/` - Update a listing (owner only)
- `DELETE /api/listings/{id}/` - Delete a listing (owner only)
- `GET /api/bookings/` - List user's bookings
- `POST /api/bookings/` - Create a booking
- `GET /api/reviews/` - List all reviews
- `POST /api/reviews/` - Create a review

## Admin Panel

Access the admin panel at `/admin/` with superuser credentials to:
- Manage users, listings, bookings, and reviews
- View statistics and analytics
- Moderate content

## Testing

Run tests with:
```bash
python manage.py test
```

## Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Configure `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Set up a web server (Gunicorn + Nginx)
5. Configure SSL certificates
6. Set up media file storage (AWS S3, etc.)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is for educational purposes.

## Support

For issues and questions, please open an issue on the repository.