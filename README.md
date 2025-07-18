# Coderr - IT Freelancer Platform


A comprehensive platform connecting businesses with IT freelancers, built with Django REST API backend and Vanilla JavaScript frontend.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Database Models](#database-models)
- [Authentication](#authentication)
- [Development Guidelines](#development-guidelines)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

Coderr is a full-stack web application that serves as a marketplace for IT freelancers and businesses. The platform allows freelancers to create service offers with different pricing tiers, while businesses can browse, filter, and order services. The system includes user authentication, profile management, order processing, and review systems.

## ✨ Features

### Core Functionality

- **User Authentication & Authorization**: Custom user model with different user types
- **Profile Management**: Separate profiles for businesses and customers
- **Offer Management**: Create, edit, and manage service offers with multiple pricing tiers
- **Order System**: Complete order lifecycle from creation to completion
- **Review System**: Rate and review completed services
- **Search & Filtering**: Advanced filtering capabilities for offers
- **File Upload**: Support for images and documents

### User Types

- **Business Users**: Can create offers and manage their services
- **Customer Users**: Can browse offers, place orders, and leave reviews

## 🛠 Tech Stack

### Backend

- **Framework**: Django 5.2.3
- **API**: Django REST Framework 3.16.0
- **Database**: SQLite3 (development)
- **Authentication**: Token-based authentication
- **Filtering**: Django Filter 25.1
- **File Handling**: Django's built-in file upload system

### Frontend

- **Language**: Vanilla JavaScript (ES6+)
- **Styling**: CSS3 with custom design system
- **Icons**: Custom SVG icons
- **Fonts**: DM Sans, Figtree
- **Documentation**: JSDoc

## 📁 Project Structure

```
├── BackEnd/                    # Django REST API
│   ├── coderr/                # Main Django project
│   │   ├── settings.py        # Django configuration
│   │   ├── urls.py           # Main URL routing
│   │   └── views.py          # Base views
│   ├── user_auth/            # User authentication app
│   ├── profiles/             # User profiles app
│   ├── offers/               # Service offers app
│   ├── orders/               # Order management app
│   ├── reviews/              # Review system app
│   ├── manage.py             # Django management script
│   └── requirements.txt      # Python dependencies
│
├── FrontEnd/                  # Vanilla JavaScript frontend
│   ├── assets/               # Static assets
│   │   ├── fonts/           # Custom fonts
│   │   ├── icons/           # SVG icons
│   │   ├── img/             # Images
│   │   └── logo/            # Brand assets
│   ├── scripts/             # JavaScript files
│   │   ├── shared/          # Common utilities
│   │   └── template/        # HTML templates
│   ├── shared/              # Shared resources
│   │   ├── scripts/         # Common JavaScript
│   │   └── styles/          # CSS files
│   ├── styles/              # Page-specific styles
│   └── *.html               # HTML pages
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Node.js** (for development tools)
- **Git**
- **Visual Studio Code** (recommended)
- **Live Server extension** (for VS Code)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Coderr
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd BackEnd

# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd FrontEnd

# Open with Live Server
# In VS Code: Right-click on index.html → "Open with Live Server"
# Or use any local server of your choice
```

The frontend will be available at `http://localhost:5500` (or similar port)

## 🏃‍♂️ Running the Application

### Development Mode

1. **Start Backend Server**:

   ```bash
   cd BackEnd
   source env/bin/activate  # or env\Scripts\activate on Windows
   python manage.py runserver
   ```

2. **Start Frontend**:
   - Open `FrontEnd/index.html` with Live Server
   - Or serve the FrontEnd directory with any HTTP server

### Production Considerations

- Change `DEBUG = False` in `BackEnd/coderr/settings.py`
- Set a proper `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Use a production database (PostgreSQL recommended)
- Set up proper static file serving
- Configure CORS settings if needed

## 📚 API Documentation

### Base URL

```
http://localhost:8000/api/
```

### Main Endpoints

#### Authentication

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

#### User Management

- `GET /api/users/` - List users
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user

#### Profiles

- `GET /api/profiles/` - List profiles
- `GET /api/profiles/{id}/` - Get profile details
- `POST /api/profiles/` - Create profile
- `PUT /api/profiles/{id}/` - Update profile

#### Offers

- `GET /api/offers/` - List offers (with filtering)
- `GET /api/offers/{id}/` - Get offer details
- `POST /api/offers/` - Create offer
- `PUT /api/offers/{id}/` - Update offer
- `DELETE /api/offers/{id}/` - Delete offer

#### Orders

- `GET /api/orders/` - List orders
- `GET /api/orders/{id}/` - Get order details
- `POST /api/orders/` - Create order
- `PUT /api/orders/{id}/` - Update order status

#### Reviews

- `GET /api/reviews/` - List reviews
- `GET /api/reviews/{id}/` - Get review details
- `POST /api/reviews/` - Create review
- `PUT /api/reviews/{id}/` - Update review

#### Base Info

- `GET /api/base-info/` - Get platform statistics

### Authentication

The API uses Token Authentication. Include the token in request headers:

```
Authorization: Token <your-token-here>
```

## 🗄 Database Models

### User Model

- Custom user model extending Django's AbstractUser
- Fields: username, email, type (business/customer)

### Offer Model

- Service offers with multiple pricing tiers
- Fields: title, description, image, min_price, min_delivery_time
- Related to OfferDetail for pricing packages

### OfferDetail Model

- Individual pricing packages for offers
- Fields: title, revisions, delivery_time_in_days, price, features (JSON)
- Features stored as JSON string

### Profile Model

- Extended user information
- Fields: user, file (profile image), bio, etc.

### Order Model

- Order management system
- Fields: offer, customer, status, created_at, updated_at

### Review Model

- Rating and review system
- Fields: order, rating, comment, created_at

## 🔐 Authentication

The application uses Django REST Framework's Token Authentication:

1. **Registration**: Users can register with username, email, and password
2. **Login**: Returns authentication token
3. **Token Usage**: Include token in Authorization header for protected endpoints
4. **User Types**: Business and Customer types with different permissions

## 💻 Development Guidelines

### Backend Development

1. **Virtual Environment**: Always work within the virtual environment
2. **Migrations**: Run migrations after model changes
3. **Code Style**: Follow PEP 8 guidelines
4. **Testing**: Write tests for new features

### Frontend Development

1. **Vanilla JavaScript**: No frameworks - keep it simple
2. **Modular Structure**: Use shared scripts for common functionality
3. **CSS Organization**: Follow the established CSS structure
4. **JSDoc**: Document functions and classes

### File Organization

- **Shared Resources**: Place common code in `FrontEnd/shared/`
- **Page-Specific**: Keep page-specific code in respective directories
- **Assets**: Organize images, icons, and fonts in `assets/`

## 🐛 Troubleshooting

### Common Issues

1. **Database Migration Errors**:

   ```bash
   python manage.py makemigrations --empty <app_name>
   python manage.py migrate
   ```

2. **Static Files Not Loading**:

   - Ensure Live Server is running
   - Check file paths in HTML files

3. **CORS Issues**:

   - Backend and frontend should run on different ports
   - Configure CORS settings if needed

4. **Token Authentication Issues**:
   - Ensure token is included in Authorization header
   - Check token format: `Token <token-value>`

### Debug Mode

- Backend debug is enabled by default
- Check Django debug toolbar for detailed information
- Use browser developer tools for frontend debugging

## 📝 Additional Notes

- **JSDoc Documentation**: Available in `FrontEnd/docs/`
- **Custom Fonts**: DM Sans and Figtree fonts included
- **Responsive Design**: Mobile-first approach
- **File Upload**: Supports image uploads for offers and profiles
- **Search Functionality**: Advanced filtering and search capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is developed for educational purposes at the Developer Akademie.

---

**Note**: This project is designed for educational purposes and demonstrates full-stack development with Django and Vanilla JavaScript. For production use, consider implementing additional security measures, proper error handling, and performance optimizations.
