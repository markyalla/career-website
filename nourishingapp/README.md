# Nest & Nourish - Maternal Wellness Management System

A comprehensive web application designed specifically for mothers to track their fitness, recovery, and mental wellness journey.

## Features

- **User Authentication**: Secure registration and login system
- **Dashboard**: Personalized welcome page with wellness overview
- **Exercise Tracking**: Log and track various exercises with duration and notes
- **Recovery Tips**: Expert guidance on self-care and recovery practices
- **Mental Wellness Support**: Daily mood and stress tracking with resources
- **Responsive Design**: Beautiful, mobile-friendly interface using Bootstrap

## Installation & Setup

### 1. Create Project Directory
```bash
mkdir nest-nourish
cd nest-nourish
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Project Structure
Create the following directory structure:
```
nest-nourish/
├── app.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── exercise.html
│   ├── recovery.html
│   ├── mental_wellness.html
│   └── profile.html
└── static/
    ├── css/
    └── js/
```

### 5. Create Templates Directory
```bash
mkdir templates
```

### 6. Add All Template Files
Copy each HTML template file into the `templates/` directory with the exact filenames shown above.

### 7. Run the Application
```bash
python app.py
```

The application will be available at: `http://127.0.0.1:5000`

## Database

The application uses SQLite database which will be created automatically when you first run the app. The database file `nest_nourish.db` will be created in your project directory.

### Database Models

- **User**: Stores user account information
- **Exercise**: Tracks exercise sessions with type, duration, and notes
- **WellnessEntry**: Records daily mood, stress levels, sleep, and reflections

## Security Notes

- Change the `SECRET_KEY` in `app.py` before deploying to production
- Use environment variables for sensitive configuration in production
- Consider using PostgreSQL or MySQL for production deployments

## Usage

1. **Registration**: Create a new account with username, email, and password
2. **Login**: Access your personal dashboard
3. **Exercise Logging**: Track your workouts with predefined exercise types
4. **Wellness Check-ins**: Record daily mood, stress levels, and sleep
5. **Recovery Resources**: Access tips and guidance for self-care
6. **Profile Management**: View your progress and account information

## Features Included

### Exercise Module
- Pre-defined exercise types suitable for mothers
- Duration tracking
- Personal notes for each session
- Exercise tips and video recommendations

### Recovery Module
- Rest and sleep guidance
- Nutrition tips
- Physical and emotional recovery strategies
- Daily routine suggestions
- Important medical reminders

### Mental Wellness Module
- Mood tracking (1-10 scale)
- Stress level monitoring
- Sleep hours logging
- Daily reflections
- Mental health resources
- Crisis support information
- Interactive breathing exercises
- Daily affirmations
- Quick wellness tools

### User Management
- Secure password hashing
- Session management
- Personal dashboard
- Progress tracking
- Account statistics

## Customization

You can easily customize this application by:

- Adding more exercise types in the dropdown
- Modifying the wellness tracking parameters
- Adding new recovery tips and resources
- Customizing the color scheme in the CSS variables
- Adding more interactive wellness tools
- Implementing email notifications
- Adding social features for community support

## Future Enhancements

Consider adding these features for enhanced functionality:

- Email verification for registration
- Password reset functionality
- Data export features
- Exercise and wellness charts/graphs
- Reminder notifications
- Social sharing capabilities
- Healthcare provider integration
- Mobile app companion

## Support

This application is designed with mothers' unique needs in mind, providing a safe and supportive digital space for wellness tracking and self-care guidance.