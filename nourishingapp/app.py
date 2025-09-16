from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nest_nourish.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    postpartum_months = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Maternal wellness tracking
    exercises = db.relationship('Exercise', backref='user', lazy=True)
    wellness_entries = db.relationship('WellnessEntry', backref='user', lazy=True)
    progress_entries = db.relationship('ProgressEntry', backref='user', lazy=True)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_type = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    date_completed = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

class WellnessEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood_rating = db.Column(db.Integer, nullable=False)  # 1-10 scale
    stress_level = db.Column(db.Integer, nullable=False)  # 1-10 scale
    sleep_hours = db.Column(db.Float, nullable=True)
    notes = db.Column(db.Text)
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)

class Tip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Tip('{self.title}', '{self.category}')"

class MentalTip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month_relation = db.Column(db.Integer, nullable=False)  # Months postpartum
    tip_content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class RecoveryTip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    recovery_stage = db.Column(db.String(50), nullable=False)  # e.g., "Early", "Mid", "Late"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class MentalWellnessResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)  # e.g., "Article", "Exercise", "Meditation"
    mood_category = db.Column(db.String(50))  # e.g., "Anxiety", "Depression", "Stress"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class ExerciseVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_type = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    video_url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    difficulty_level = db.Column(db.String(20), default='Beginner')  # Beginner, Intermediate, Advanced
    duration = db.Column(db.Integer)  # in minutes
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ProgressEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    performance_rating = db.Column(db.Integer, nullable=False)  # 1-5 scale (1=Poor, 5=Excellent)
    energy_level = db.Column(db.Integer, nullable=False)  # 1-10 scale
    difficulty_felt = db.Column(db.Integer, nullable=False)  # 1-10 scale
    notes = db.Column(db.Text)
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)
    
    exercise = db.relationship('Exercise', backref='progress_entries')

# Secure admin interface
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

# Initialize Flask-Admin
admin = Admin(app, name='NourishAdmin', template_mode='bootstrap3')
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Exercise, db.session))
admin.add_view(AdminModelView(WellnessEntry, db.session))
admin.add_view(AdminModelView(Tip, db.session))
admin.add_view(AdminModelView(MentalTip, db.session))
admin.add_view(AdminModelView(RecoveryTip, db.session))
admin.add_view(AdminModelView(MentalWellnessResource, db.session))
admin.add_view(AdminModelView(ExerciseVideo, db.session))
admin.add_view(AdminModelView(ProgressEntry, db.session))

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('register.html')
        
        # Create new user
        password_hash = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['full_name'] = user.full_name
            login_user(user)  # Flask-Login
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()  # Flask-Login
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found. Please log in again.', 'danger')
        session.clear()
        return redirect(url_for('login'))
    
    recent_exercises = Exercise.query.filter_by(user_id=user.id).order_by(Exercise.date_completed.desc()).limit(5).all()
    recent_wellness = WellnessEntry.query.filter_by(user_id=user.id).order_by(WellnessEntry.date_recorded.desc()).limit(3).all()
    
    # Get personalized tips based on postpartum months
    wellness_tips = MentalTip.query.filter_by(month_relation=user.postpartum_months).all()
    
    return render_template('dashboard.html',
                         user=user,
                         exercises=recent_exercises,
                         wellness_entries=recent_wellness,
                         wellness_tips=wellness_tips)

@app.route('/exercise')
def exercise():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    
    # Get exercise videos for display
    exercise_videos = ExerciseVideo.query.filter_by(is_active=True).all()
    
    return render_template('exercise.html', exercise_videos=exercise_videos)

@app.route('/log_exercise', methods=['POST'])
def log_exercise():
    if 'user_id' not in session:
        if request.is_json or request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
            return {'success': False, 'error': 'Please log in'}, 401
        flash('Please log in to log exercises.', 'warning')
        return redirect(url_for('login'))
    
    exercise_type = request.form['exercise_type']
    duration = int(request.form['duration'])
    notes = request.form.get('notes', '')
    
    new_exercise = Exercise(
        user_id=session['user_id'],
        exercise_type=exercise_type,
        duration=duration,
        notes=notes
    )
    
    db.session.add(new_exercise)
    db.session.commit()
    
    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
        return {'success': True, 'exercise_id': new_exercise.id, 'message': 'Exercise logged successfully!'}
    
    flash('Exercise logged successfully!', 'success')
    return redirect(url_for('exercise'))

@app.route('/log_progress', methods=['POST'])
def log_progress():
    if 'user_id' not in session:
        flash('Please log in to log progress.', 'warning')
        return redirect(url_for('login'))
    
    exercise_id = int(request.form['exercise_id'])
    performance_rating = int(request.form['performance_rating'])
    energy_level = int(request.form['energy_level'])
    difficulty_felt = int(request.form['difficulty_felt'])
    notes = request.form.get('notes', '')
    
    new_progress = ProgressEntry(
        user_id=session['user_id'],
        exercise_id=exercise_id,
        performance_rating=performance_rating,
        energy_level=energy_level,
        difficulty_felt=difficulty_felt,
        notes=notes
    )
    
    db.session.add(new_progress)
    db.session.commit()
    
    flash('Progress logged successfully!', 'success')
    return redirect(url_for('exercise'))

@app.route('/get_exercise_videos/<exercise_type>')
def get_exercise_videos(exercise_type):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    videos = ExerciseVideo.query.filter_by(exercise_type=exercise_type, is_active=True).all()
    return render_template('exercise_videos.html', videos=videos, exercise_type=exercise_type)

@app.route('/recovery')
def recovery():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    # Get recovery tips based on user's postpartum stage
    if user.postpartum_months <= 3:
        stage = "Early"
    elif user.postpartum_months <= 12:
        stage = "Mid"
    else:
        stage = "Late"
    
    recovery_tips = RecoveryTip.query.filter_by(recovery_stage=stage, is_active=True).all()
    all_recovery_tips = RecoveryTip.query.filter_by(is_active=True).all()
    
    return render_template('recovery.html', 
                         recovery_tips=recovery_tips, 
                         all_recovery_tips=all_recovery_tips,
                         user=user)

@app.route('/mental_wellness')
def mental_wellness():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    wellness_resources = MentalWellnessResource.query.filter_by(is_active=True).all()
    
    # Get personalized mental tips based on postpartum months
    mental_tips = MentalTip.query.filter_by(month_relation=user.postpartum_months).all()
    
    return render_template('mental_wellness.html', 
                         wellness_resources=wellness_resources,
                         mental_tips=mental_tips,
                         user=user)

@app.route('/log_wellness', methods=['POST'])
def log_wellness():
    if 'user_id' not in session:
        flash('Please log in to log wellness entries.', 'warning')
        return redirect(url_for('login'))
    
    mood_rating = int(request.form['mood_rating'])
    stress_level = int(request.form['stress_level'])
    sleep_hours = float(request.form['sleep_hours']) if request.form['sleep_hours'] else None
    notes = request.form.get('notes', '')
    
    new_entry = WellnessEntry(
        user_id=session['user_id'],
        mood_rating=mood_rating,
        stress_level=stress_level,
        sleep_hours=sleep_hours,
        notes=notes
    )
    
    db.session.add(new_entry)
    db.session.commit()
    
    flash('Wellness entry logged successfully!', 'success')
    return redirect(url_for('mental_wellness'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please log in to access your profile.', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found. Please log in again.', 'danger')
        session.clear()
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        user.postpartum_months = int(request.form.get('postpartum_months', user.postpartum_months))
        user.full_name = request.form.get('full_name', user.full_name)
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
        
    return render_template('profile.html', user=user)

def create_sample_data():
    """Create sample data for testing"""
    # Mental tips for different postpartum months
    mental_tips_data = [
        (0, "Welcome to motherhood! It's normal to feel overwhelmed. Take it one day at a time."),
        (1, "Your body is recovering. Focus on rest, nutrition, and gentle movement when you feel ready."),
        (2, "Sleep deprivation is tough. Rest when baby rests and ask for help with household tasks."),
        (3, "You're adjusting to new routines. Be patient with yourself as you find your rhythm."),
        (6, "You may be returning to work or establishing new routines. Self-care remains important."),
        (12, "Your baby is becoming more active. Make time for activities that bring you joy."),
    ]
    
    for month, tip in mental_tips_data:
        if not MentalTip.query.filter_by(month_relation=month).first():
            mental_tip = MentalTip(month_relation=month, tip_content=tip)
            db.session.add(mental_tip)
    
    # Recovery tips for different stages
    recovery_tips_data = [
        ("Early", "Gentle Recovery", "Focus on healing and rest. Listen to your body's needs."),
        ("Early", "Nutrition Focus", "Eat nutrient-dense foods to support healing and energy."),
        ("Mid", "Building Strength", "Gradually increase activity levels as your body allows."),
        ("Mid", "Sleep Strategies", "Develop healthy sleep habits for you and your family."),
        ("Late", "Maintaining Wellness", "Focus on long-term health and wellness practices."),
        ("Late", "Active Lifestyle", "Incorporate regular exercise that you enjoy."),
    ]
    
    for stage, title, content in recovery_tips_data:
        if not RecoveryTip.query.filter_by(title=title).first():
            recovery_tip = RecoveryTip(title=title, content=content, recovery_stage=stage)
            db.session.add(recovery_tip)
    
    # Exercise videos
    exercise_videos_data = [
        ("Prenatal Yoga", "Gentle Prenatal Flow", "https://example.com/prenatal-yoga", "Gentle yoga for expecting mothers", "Beginner", 20),
        ("Postnatal Yoga", "Postpartum Recovery Yoga", "https://example.com/postpartum-yoga", "Restorative yoga for new mothers", "Beginner", 15),
        ("Walking", "Walking for New Mothers", "https://example.com/walking-guide", "Tips for walking with your baby", "Beginner", 10),
        ("Pilates", "Core Recovery Pilates", "https://example.com/core-pilates", "Gentle core strengthening", "Intermediate", 25),
        ("Pelvic Floor Exercises", "Pelvic Floor Basics", "https://example.com/pelvic-floor", "Essential pelvic floor exercises", "Beginner", 10),
    ]
    
    for ex_type, title, url, desc, level, duration in exercise_videos_data:
        if not ExerciseVideo.query.filter_by(title=title).first():
            video = ExerciseVideo(
                exercise_type=ex_type,
                title=title,
                video_url=url,
                description=desc,
                difficulty_level=level,
                duration=duration
            )
            db.session.add(video)
    
    # Mental wellness resources
    wellness_resources_data = [
        ("Breathing Exercise", "5-Minute Calm", "Take 5 minutes to focus on deep breathing...", "Exercise", "Anxiety"),
        ("Self-Care Article", "Daily Self-Care", "Simple ways to care for yourself each day...", "Article", "General"),
        ("Meditation Guide", "Mindful Moments", "Brief meditation practices for busy mothers...", "Meditation", "Stress"),
    ]
    
    for title, subtitle, content, res_type, mood_cat in wellness_resources_data:
        if not MentalWellnessResource.query.filter_by(title=title).first():
            resource = MentalWellnessResource(
                title=title,
                content=content,
                resource_type=res_type,
                mood_category=mood_cat
            )
            db.session.add(resource)
    
    db.session.commit()

# Create database tables
with app.app_context():
    db.create_all()
    
    # Create a default admin user if it doesn't exist
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            full_name='Administrator',
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Default admin user created: username='admin', password='admin123'")
    
    # Create sample data
    create_sample_data()
    print("Sample data created successfully!")

if __name__ == '__main__':
    app.run(debug=True)