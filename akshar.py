from flask import Flask, render_template, request, redirect, session, url_for
from models import *
import os
import subprocess
from datetime import datetime
from recommendation import detect_emotion
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from user_analysis import generate_user_analysis

app = Flask(__name__, template_folder='templates')
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize database
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        trusted_contact = request.form['trusted_contact']
        
        # Automatically assign user role
        role = Role.query.filter_by(name='user').first()
        if not role:
            role = Role(name='user')
            db.session.add(role)
            db.session.commit()

        if User.query.filter_by(username=username).first():
            return "Username already exists."

        new_user = User(
            username=username,
            password=password,
            trusted_contact=trusted_contact,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            login_user(user)
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role.name

            if user.role.name == 'user':
                anjum_path = os.path.join('templates', 'anjum.py')
                subprocess.Popen(['python', anjum_path], shell=True)
                return redirect(url_for('anjum_wrapper'))

            elif user.role.name == 'admin':
                return redirect(url_for('admin_dashboard'))

        return "Invalid credentials"

    return render_template('login.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    
    # Generate user analysis
    plots, stats = generate_user_analysis()
    
    # Get recent posts
    recent_posts = Post.query.order_by(Post.timestamp.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html',
                         username=current_user.username,
                         stats=stats,
                         recent_posts=recent_posts)

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Create roles if they don't exist
        admin_role = Role.query.filter_by(name='admin').first()
        user_role = Role.query.filter_by(name='user').first()
        
        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)
        if not user_role:
            user_role = Role(name='user')
            db.session.add(user_role)
        
        db.session.commit()

        # Create default admin user if not present
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            default_admin = User(
                username='admin',
                password='admin',
                trusted_contact='0000000000',
                role=admin_role
            )
            db.session.add(default_admin)
            db.session.commit()

@app.route('/anjum_wrapper', methods=['GET', 'POST'])
def anjum_wrapper():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        content = request.form['content']
        if content.strip():
            # Step 1: Analyze content
            emotion, confidence = detect_emotion(content)

            # Step 2: Save post along with emotion and confidence
            new_post = Post(content=content, user_id=user.id, emotion=emotion, confidence=confidence)
            db.session.add(new_post)
            db.session.commit()

            # Optional: Trigger alerts if emotion = 'depressed' and confidence > threshold
            if emotion == 'depressed' and confidence > 0.7:
                # Example: send_alert_to_trusted_contact(user)
                pass

            return redirect(url_for('anjum_wrapper'))

    user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).all()
    return render_template('anjum_wrapper.html', username=user.username, posts=user_posts)


@app.route('/community')
def community():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('community.html', posts=posts)

app.run(debug=True)
