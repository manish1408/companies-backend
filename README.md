# User Management System

A general-purpose user management system built with FastAPI, MongoDB, and JWT authentication. This project provides a clean, reusable foundation for user authentication and profile management across different applications.

## Features

- **User Authentication**: Sign up, sign in
- **User Management**: Admin can create, view, update, and delete users
- **Profile Management**: Users can view and update their profiles
- **JWT Authentication**: Secure token-based authentication
- **Role-based Access**: Admin and user roles with appropriate permissions
- **File Upload**: Azure Blob Storage integration for profile pictures and file uploads

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database with Motor async driver
- **JWT**: JSON Web Tokens for authentication
- **Azure Blob Storage**: Cloud storage for file uploads
- **Pydantic**: Data validation and serialization

## Project Structure

```
app/
├── controllers/          # API route handlers
│   ├── Auth.py          # Authentication endpoints
│   └── Profile.py       # Profile management endpoints
├── services/            # Business logic layer
│   ├── Auth.py          # Authentication service
│   ├── Profile.py       # Profile service
│   └── Common.py        # Common utilities service
├── models/              # Database models
│   └── User.py          # User model
├── schemas/             # Pydantic schemas
│   ├── User.py          # User schemas
│   ├── ServerResponse.py # API response schema
│   ├── Common.py        # Common schemas
│   └── PyObjectId.py    # MongoDB ObjectId schema
├── middleware/          # Custom middleware
│   ├── Auth.py          # Authentication middleware
│   ├── Cors.py          # CORS middleware
│   ├── GlobalErrorHandling.py # Error handling
│   └── JWTVerification.py # JWT verification
├── helpers/             # Utility functions
│   ├── Database.py      # Database connection
│   ├── AsyncDatabase.py # Async database helper
│   ├── AzureStorage.py  # Azure Blob Storage helper
│   └── Utilities.py     # General utilities
├── dependencies.py      # Dependency injection
├── config.py           # Configuration
└── main.py             # Application entry point
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/signin` - User login

### User Management (Admin)
- `GET /api/v1/auth/admin/users` - Get all users (admin only)
- `POST /api/v1/auth/admin/create-user` - Create user (admin only)
- `GET /api/v1/auth/admin/users/{user_id}` - Get user by ID (admin only)

### User Operations
- `GET /api/v1/auth/users/get-all-users` - Get all users
- `PUT /api/v1/auth/users/{user_id}` - Update user profile
- `DELETE /api/v1/auth/users/delete-user/{user_id}` - Delete user

### Profile Management
- `GET /api/v1/profile/me` - Get current user profile

## Environment Variables

Create a `.env` file with the following variables:

```env
# Database
MONGODB_CONNECTION_STRING=mongodb://localhost:27017
DB_NAME=user_management

# JWT
JWT_SECRET=your-secret-key
JWT_EXPIRY=3600


# Azure Storage
AZURE_STORAGE_CONNECTION_STRING=your-azure-connection-string
AZURE_STORAGE_CONTAINER=your-container-name
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables
4. Run the application:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

## Usage

1. Start the server
2. Access the API documentation at `http://localhost:3003/api-docs`
3. Use the endpoints to manage users and authentication

## Features for New Projects

This template provides:
- Complete user authentication system
- Admin and user role management
- File upload capabilities
- Clean, modular code structure
- Comprehensive error handling
- JWT-based security

## Customization

To adapt this for your specific project:
1. Modify user schemas in `app/schemas/User.py`
2. Add new endpoints in controllers
3. Extend services for additional business logic
4. Update database models as needed
5. Customize middleware for specific requirements

## License

This project is designed as a template for general use across different applications.
