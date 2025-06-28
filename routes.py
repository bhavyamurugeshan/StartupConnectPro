from flask import render_template, redirect, url_for, flash, request, session
from app import app
from forms import LoginForm, RegistrationForm, StartupForm, ConnectionForm, MessageForm, SearchForm
from data_store import data_store
from functools import wraps

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current logged-in user"""
    if 'user_id' in session:
        return data_store.get_user_by_id(session['user_id'])
    return None

@app.route('/')
def index():
    """Home page"""
    # Get recent startups for homepage
    recent_startups = list(data_store.startups.values())[-6:]  # Last 6 startups
    return render_template('index.html', startups=recent_startups)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        if data_store.get_user_by_username(form.username.data):
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)
        
        if data_store.get_user_by_email(form.email.data):
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('register.html', form=form)
        
        # Create new user
        user = data_store.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            user_type=form.user_type.data,
            full_name=form.full_name.data,
            bio=form.bio.data,
            location=form.location.data,
            industry=form.industry.data,
            experience=form.experience.data
        )
        
        session['user_id'] = user.id
        flash('Registration successful! Welcome to the platform.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = data_store.get_user_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """User logout"""
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user = get_current_user()
    user_startups = data_store.get_startups_by_founder(user.id)
    connections = data_store.get_connections_for_user(user.id)
    conversations = data_store.get_conversations_for_user(user.id)
    
    return render_template('dashboard.html', user=user, startups=user_startups, 
                         connections=connections, conversations=conversations)

@app.route('/profile')
@login_required
def profile():
    """User profile"""
    user = get_current_user()
    return render_template('profile.html', user=user)

@app.route('/startup/new', methods=['GET', 'POST'])
@login_required
def create_startup():
    """Create new startup"""
    user = get_current_user()
    if user.user_type != 'founder':
        flash('Only startup founders can create startup profiles.', 'warning')
        return redirect(url_for('dashboard'))
    
    form = StartupForm()
    if form.validate_on_submit():
        startup = data_store.create_startup(
            founder_id=user.id,
            name=form.name.data,
            description=form.description.data,
            industry=form.industry.data,
            stage=form.stage.data,
            funding_needed=form.funding_needed.data,
            location=form.location.data,
            website=form.website.data,
            pitch_deck=form.pitch_deck.data,
            team_size=form.team_size.data,
            revenue=form.revenue.data,
            looking_for=form.looking_for.data
        )
        
        flash('Startup profile created successfully!', 'success')
        return redirect(url_for('startup_detail', startup_id=startup.id))
    
    return render_template('startup_form.html', form=form, title='Create Startup')

@app.route('/startup/<int:startup_id>')
def startup_detail(startup_id):
    """Startup detail page"""
    startup = data_store.get_startup_by_id(startup_id)
    if not startup:
        flash('Startup not found.', 'danger')
        return redirect(url_for('search'))
    
    founder = data_store.get_user_by_id(startup.founder_id)
    current_user = get_current_user()
    
    # Check if current user can connect with this startup
    can_connect = (current_user and 
                  current_user.id != startup.founder_id and 
                  current_user.user_type in ['investor', 'partner', 'service_provider'])
    
    return render_template('startup_detail.html', startup=startup, founder=founder, 
                         can_connect=can_connect)

@app.route('/startup/<int:startup_id>/connect', methods=['GET', 'POST'])
@login_required
def connect_startup(startup_id):
    """Send connection request to startup"""
    startup = data_store.get_startup_by_id(startup_id)
    if not startup:
        flash('Startup not found.', 'danger')
        return redirect(url_for('search'))
    
    current_user = get_current_user()
    if current_user.id == startup.founder_id:
        flash('You cannot connect with your own startup.', 'warning')
        return redirect(url_for('startup_detail', startup_id=startup_id))
    
    form = ConnectionForm()
    if form.validate_on_submit():
        connection = data_store.create_connection(
            sender_id=current_user.id,
            receiver_id=startup.founder_id,
            startup_id=startup_id,
            message=form.message.data
        )
        
        flash('Connection request sent successfully!', 'success')
        return redirect(url_for('startup_detail', startup_id=startup_id))
    
    return render_template('startup_detail.html', startup=startup, 
                         founder=data_store.get_user_by_id(startup.founder_id),
                         form=form, show_form=True, can_connect=True)

@app.route('/search')
def search():
    """Search startups"""
    form = SearchForm()
    startups = []
    
    if request.method == 'GET' and request.args:
        # Handle search from URL parameters
        query = request.args.get('query', '')
        industry = request.args.get('industry', '')
        stage = request.args.get('stage', '')
        looking_for = request.args.get('looking_for', '')
        
        form.query.data = query
        form.industry.data = industry
        form.stage.data = stage
        form.looking_for.data = looking_for
        
        startups = data_store.search_startups(query, industry, stage, looking_for)
    elif form.validate_on_submit():
        # Handle search from form submission
        startups = data_store.search_startups(
            form.query.data or '',
            form.industry.data or '',
            form.stage.data or '',
            form.looking_for.data or ''
        )
    else:
        # Show all startups by default
        startups = list(data_store.startups.values())
    
    return render_template('search.html', form=form, startups=startups)

@app.route('/connections')
@login_required
def connections():
    """View connections"""
    user = get_current_user()
    connections = data_store.get_connections_for_user(user.id)
    
    # Separate sent and received connections
    sent_connections = [c for c in connections if c.sender_id == user.id]
    received_connections = [c for c in connections if c.receiver_id == user.id]
    
    return render_template('messages.html', sent_connections=sent_connections, 
                         received_connections=received_connections)

@app.route('/connection/<int:connection_id>/respond/<action>')
@login_required
def respond_connection(connection_id, action):
    """Respond to connection request"""
    current_user = get_current_user()
    
    # Find the connection
    connection = None
    for conn in data_store.connections:
        if conn.id == connection_id and conn.receiver_id == current_user.id:
            connection = conn
            break
    
    if not connection:
        flash('Connection request not found.', 'danger')
        return redirect(url_for('connections'))
    
    if action == 'accept':
        data_store.update_connection_status(connection_id, 'accepted')
        flash('Connection request accepted!', 'success')
    elif action == 'decline':
        data_store.update_connection_status(connection_id, 'declined')
        flash('Connection request declined.', 'info')
    
    return redirect(url_for('connections'))

@app.route('/messages')
@login_required
def messages():
    """View messages/conversations"""
    user = get_current_user()
    conversations = data_store.get_conversations_for_user(user.id)
    
    # Get user details for each conversation
    conversation_users = []
    for user_id in conversations:
        other_user = data_store.get_user_by_id(user_id)
        if other_user:
            # Get latest message
            msgs = data_store.get_messages_between_users(user.id, user_id)
            latest_message = msgs[-1] if msgs else None
            conversation_users.append({
                'user': other_user,
                'latest_message': latest_message
            })
    
    return render_template('messages.html', conversations=conversation_users)

@app.route('/messages/<int:user_id>', methods=['GET', 'POST'])
@login_required
def conversation(user_id):
    """View conversation with specific user"""
    current_user = get_current_user()
    other_user = data_store.get_user_by_id(user_id)
    
    if not other_user:
        flash('User not found.', 'danger')
        return redirect(url_for('messages'))
    
    messages = data_store.get_messages_between_users(current_user.id, user_id)
    
    form = MessageForm()
    if form.validate_on_submit():
        data_store.create_message(
            sender_id=current_user.id,
            receiver_id=user_id,
            content=form.content.data
        )
        flash('Message sent!', 'success')
        return redirect(url_for('conversation', user_id=user_id))
    
    return render_template('messages.html', other_user=other_user, 
                         messages=messages, form=form, show_conversation=True)

@app.context_processor
def utility_processor():
    """Make utility functions available in templates"""
    return dict(
        get_user_by_id=data_store.get_user_by_id,
        get_startup_by_id=data_store.get_startup_by_id,
        get_current_user=get_current_user
    )
