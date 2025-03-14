from flask import Flask, render_template, request, redirect, url_for, flash, g, jsonify, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "supports_credentials": True
    }
})
app.config['SECRET_KEY'] = os.urandom(24)
app.config['DATABASE'] = 'job_board.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initialize the database."""
    init_db()
    print('Initialized the database.')

# Routes
@app.route('/')
def index():
    db = get_db()
    jobs = db.execute('SELECT jobs.*, companies.name as company_name, '
                     '(SELECT AVG(rating) FROM company_ratings WHERE company_id = jobs.company_id) as avg_rating '
                     'FROM jobs JOIN companies ON jobs.company_id = companies.id '
                     'ORDER BY posted_date DESC').fetchall()
    return render_template('index.html', jobs=jobs)

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    db = get_db()
    job = db.execute('SELECT jobs.*, companies.name as company_name, companies.description as company_description, '
                    '(SELECT AVG(rating) FROM company_ratings WHERE company_id = jobs.company_id) as avg_rating '
                    'FROM jobs JOIN companies ON jobs.company_id = companies.id '
                    'WHERE jobs.id = ?', (job_id,)).fetchone()
    
    if job is None:
        flash('Job not found')
        return redirect(url_for('index'))
    
    return render_template('job_detail.html', job=job)

@app.route('/company/<int:company_id>')
def company_detail(company_id):
    db = get_db()
    company = db.execute('SELECT *, (SELECT AVG(rating) FROM company_ratings WHERE company_id = ?) as avg_rating '
                        'FROM companies WHERE id = ?', (company_id, company_id)).fetchone()
    
    if company is None:
        flash('Company not found')
        return redirect(url_for('index'))
    
    jobs = db.execute('SELECT * FROM jobs WHERE company_id = ? ORDER BY posted_date DESC', (company_id,)).fetchall()
    ratings = db.execute('SELECT * FROM company_ratings WHERE company_id = ? ORDER BY created_at DESC', (company_id,)).fetchall()
    
    return render_template('company_detail.html', company=company, jobs=jobs, ratings=ratings)

@app.route('/rate_company/<int:company_id>', methods=['POST'])
def rate_company(company_id):
    if 'user_id' not in session:
        flash('You must be logged in to rate a company')
        return redirect(url_for('login'))
    
    rating = int(request.form.get('rating', 0))
    comment = request.form.get('comment', '')
    
    if rating < 1 or rating > 5:
        flash('Rating must be between 1 and 5')
        return redirect(url_for('company_detail', company_id=company_id))
    
    db = get_db()
    db.execute('INSERT INTO company_ratings (company_id, user_id, rating, comment, created_at) VALUES (?, ?, ?, ?, ?)',
              (company_id, session['user_id'], rating, comment, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    db.commit()
    
    flash('Thank you for your rating!')
    return redirect(url_for('company_detail', company_id=company_id))

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if 'user_id' not in session:
        flash('You must be logged in to post a job')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        company_id = request.form.get('company_id')
        location = request.form.get('location')
        description = request.form.get('description')
        requirements = request.form.get('requirements')
        salary_range = request.form.get('salary_range')
        
        db = get_db()
        db.execute('INSERT INTO jobs (title, company_id, location, description, requirements, salary_range, posted_date) '
                  'VALUES (?, ?, ?, ?, ?, ?, ?)',
                  (title, company_id, location, description, requirements, salary_range, datetime.now().strftime('%Y-%m-%d')))
        db.commit()
        
        flash('Job posted successfully!')
        return redirect(url_for('index'))
    
    db = get_db()
    companies = db.execute('SELECT id, name FROM companies').fetchall()
    return render_template('post_job.html', companies=companies)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        user_type = request.form.get('user_type')
        
        db = get_db()
        if db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone() is not None:
            flash('Username already exists')
            return redirect(url_for('register'))
        
        db.execute('INSERT INTO users (username, password, email, user_type) VALUES (?, ?, ?, ?)',
                  (username, generate_password_hash(password), email, user_type))
        db.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user is None or not check_password_hash(user['password'], password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['user_type'] = user['user_type']
        
        flash('Logged in successfully!')
        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!')
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    location = request.args.get('location', '')
    
    db = get_db()
    sql = '''
        SELECT jobs.*, companies.name as company_name,
        (SELECT AVG(rating) FROM company_ratings WHERE company_id = jobs.company_id) as avg_rating
        FROM jobs JOIN companies ON jobs.company_id = companies.id
        WHERE 1=1
    '''
    params = []
    
    if query:
        sql += ' AND (jobs.title LIKE ? OR jobs.description LIKE ? OR companies.name LIKE ?)'
        query_param = f'%{query}%'
        params.extend([query_param, query_param, query_param])
    
    if location:
        sql += ' AND jobs.location LIKE ?'
        params.append(f'%{location}%')
    
    sql += ' ORDER BY jobs.posted_date DESC'
    
    jobs = db.execute(sql, params).fetchall()
    return render_template('search_results.html', jobs=jobs, query=query, location=location)

# API Endpoints
# API Routes
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    db = get_db()
    jobs = db.execute('SELECT jobs.*, companies.name as company_name, '
                     '(SELECT AVG(rating) FROM company_ratings WHERE company_id = jobs.company_id) as avg_rating '
                     'FROM jobs JOIN companies ON jobs.company_id = companies.id '
                     'ORDER BY posted_date DESC').fetchall()
    
    job_list = []
    for job in jobs:
        job_dict = dict(job)
        job_dict['avg_rating'] = float(job_dict['avg_rating']) if job_dict['avg_rating'] else 0
        job_list.append(job_dict)
    
    return jsonify(job_list)

@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    db = get_db()
    job = db.execute('SELECT jobs.*, companies.name as company_name, companies.description as company_description, '
                    '(SELECT AVG(rating) FROM company_ratings WHERE company_id = jobs.company_id) as avg_rating '
                    'FROM jobs JOIN companies ON jobs.company_id = companies.id '
                    'WHERE jobs.id = ?', (job_id,)).fetchone()
    
    if job is None:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(dict(job))

@app.route('/api/companies', methods=['GET'])
def get_companies():
    db = get_db()
    companies = db.execute('SELECT *, (SELECT AVG(rating) FROM company_ratings WHERE company_id = companies.id) as avg_rating '
                          'FROM companies ORDER BY name').fetchall()
    return jsonify([dict(company) for company in companies])

@app.route('/api/companies/<int:company_id>', methods=['GET'])
def get_company(company_id):
    db = get_db()
    company = db.execute('SELECT *, (SELECT AVG(rating) FROM company_ratings WHERE company_id = ?) as avg_rating '
                        'FROM companies WHERE id = ?', (company_id, company_id)).fetchone()
    
    if company is None:
        return jsonify({'error': 'Company not found'}), 404
    
    jobs = db.execute('SELECT * FROM jobs WHERE company_id = ? ORDER BY posted_date DESC', (company_id,)).fetchall()
    ratings = db.execute('SELECT * FROM company_ratings WHERE company_id = ? ORDER BY created_at DESC', (company_id,)).fetchall()
    
    return jsonify({
        'company': dict(company),
        'jobs': [dict(job) for job in jobs],
        'ratings': [dict(rating) for rating in ratings]
    })

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    
    if user is None or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    return jsonify({
        'id': user['id'],
        'username': user['username'],
        'user_type': user['user_type']
    })

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    user_type = data.get('user_type')
    
    if not all([username, password, email, user_type]):
        return jsonify({'error': 'All fields are required'}), 400
    
    db = get_db()
    if db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone() is not None:
        return jsonify({'error': 'Username already exists'}), 400
    
    db.execute('INSERT INTO users (username, password, email, user_type) VALUES (?, ?, ?, ?)',
              (username, generate_password_hash(password), email, user_type))
    db.commit()
    
    return jsonify({'message': 'Registration successful'}), 201

if __name__ == '__main__':
    app.run(debug=True)

