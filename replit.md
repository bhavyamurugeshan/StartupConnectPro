# Replit.md - StartupConnect Platform

## Overview

StartupConnect is a web-based platform designed to connect innovative startups with investors, business partners, and service providers. Built with Flask, the application facilitates meaningful connections through a comprehensive matching and messaging system.

## System Architecture

### Technology Stack
- **Backend Framework**: Flask (Python 3.11+)
- **Web Server**: Gunicorn with autoscale deployment
- **Frontend**: Bootstrap 5 with dark theme, Feather Icons
- **Data Storage**: In-memory data store (transitional architecture)
- **Form Handling**: Flask-WTF with WTForms validation
- **Session Management**: Flask sessions with secret key authentication
- **Package Management**: UV with pyproject.toml configuration

### Architectural Patterns
- **MVC Architecture**: Clear separation with models, views (templates), and controllers (routes)
- **Form-based Interactions**: WTForms for data validation and rendering
- **Session-based Authentication**: Simple login/logout with session storage
- **Responsive Design**: Bootstrap-based responsive UI with dark theme

## Key Components

### Data Models
- **User Model**: Supports multiple user types (founder, investor, partner, service_provider) with authentication
- **Startup Model**: Complete startup profiles with industry, stage, funding details
- **Connection Model**: Manages relationships between users and startups
- **Message Model**: Handles private messaging between users

### Data Storage Strategy
Currently implements an in-memory data store (`DataStore` class) for rapid development and testing. This design choice allows for:
- Quick prototyping without database setup complexity
- Easy testing and development iterations
- Clear data access patterns that can be migrated to persistent storage later

**Migration Path**: The current in-memory store is designed to be replaced with a persistent database (PostgreSQL) using Drizzle ORM, maintaining the same interface contracts.

### Authentication & Authorization
- **Session-based Authentication**: Uses Flask sessions for user state management
- **Role-based Access**: Different user types (founders, investors, partners, service providers)
- **Login Required Decorator**: Protects sensitive routes with `@login_required`
- **Password Security**: Werkzeug password hashing for secure credential storage

### User Interface Architecture
- **Template Inheritance**: Base template with consistent navigation and styling
- **Responsive Design**: Bootstrap 5 grid system with mobile-first approach
- **Dark Theme**: Replit-compatible dark theme implementation
- **Icon System**: Feather Icons for consistent visual language

## Data Flow

### User Registration & Authentication
1. User submits registration form with validation
2. Password is hashed using Werkzeug security
3. User profile is stored in data store
4. Session is created for authenticated state

### Startup Management
1. Founders create startup profiles through form interface
2. Startup data is validated and stored
3. Startups appear in search results and discovery feeds
4. Rich filtering and search capabilities

### Connection & Messaging
1. Users discover startups through search/browse interface
2. Connection requests are initiated through startup detail pages
3. Direct messaging system facilitates communication
4. Conversation history is maintained per user pair

## External Dependencies

### Python Packages
- **Flask**: Core web framework
- **Flask-WTF**: Form handling and CSRF protection
- **Werkzeug**: WSGI utilities and security functions
- **Gunicorn**: Production WSGI server
- **Email-Validator**: Email validation for forms
- **Psycopg2-binary**: PostgreSQL driver (prepared for future migration)

### Frontend Dependencies
- **Bootstrap 5**: CSS framework with dark theme
- **Feather Icons**: SVG icon system
- **Custom CSS**: Minimal overrides for platform-specific styling

### Infrastructure
- **Replit Nix Environment**: Stable-24_05 channel with OpenSSL and PostgreSQL
- **Gunicorn Configuration**: Autoscale deployment with port binding

## Deployment Strategy

### Development Environment
- **Replit Workflows**: Configured for local development with hot reload
- **Debug Mode**: Flask debug mode enabled for development
- **Port Configuration**: Standardized on port 5000

### Production Deployment
- **Gunicorn Server**: Multi-worker WSGI server
- **Autoscale Target**: Replit autoscale deployment
- **Proxy Headers**: ProxyFix middleware for proper header handling
- **Environment Variables**: Secure session key configuration

### Database Migration Path
The current in-memory storage is designed for easy migration to PostgreSQL:
1. Replace `DataStore` class with Drizzle ORM models
2. Implement database connection and migration scripts
3. Update data access methods to use persistent storage
4. Maintain existing API contracts for seamless transition

## Changelog
- June 27, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.