# Disaster Response Information System (DRIS)

A web-based platform for disaster response management, developed for the National Disaster Management Agency (NADMA).

## Overview

The Disaster Response Information System (DRIS) is a comprehensive platform that facilitates effective disaster response by connecting citizens, volunteers, and authorities. Through DRIS, citizens can report disaster events and request aid, volunteers can register their availability and skills, and authorities can monitor and manage aid requests, coordinate shelters, and assign volunteers.

## User Groups

1. **Citizens** - General public who can report disasters and request assistance
2. **Volunteers** - Individuals who offer their skills and time to help during emergencies
3. **Authorities** - NADMA staff and officials who coordinate disaster response efforts

## Features

- **User Management**: Role-based registration and authentication for citizens, volunteers and authorities
- **Disaster Reporting**: Citizens can report disaster events with location, type, severity, and other details
- **Aid Request Management**: Citizens can request various types of aid during emergencies
- **Volunteer Coordination**: Volunteers can register their skills and availability, while authorities can assign them to tasks
- **Shelter Directory**: Information on available emergency shelters including location and capacity
- **Administrative Dashboard**: Authorities can manage users, reports, shelters, and assignments

## Technical Details

- **Framework**: Django (Python web framework)
- **Database**: SQLite
- **Authentication**: Django's built-in authentication system with custom user model
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript

## Project Structure

- `accounts/`: User authentication and profile management
- `disasters/`: Disaster reporting and aid request functionality
- `volunteers/`: Volunteer registration and assignment management
- `shelters/`: Emergency shelter tracking and management
- `dashboard/`: Administrative dashboard for authorities
- `home/`: Main landing pages
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS, images)

## Setup Instructions

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Apply migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Run the development server: `python manage.py runserver`
6. Access the site at http://127.0.0.1:8000/

## License

© 2025 NADMA - National Disaster Management Agency
