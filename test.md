# JobBoard - Your Professional Job Posting Platform

## 🚀 Overview

JobBoard is a modern web application that connects employers and job seekers. Built with Flask and modern web technologies, it provides a seamless platform for job posting, company reviews, and professional networking.

## ✨ Features

- **User Authentication**

  - Secure registration and login system
  - Role-based access (Job Seekers & Employers)
  - Profile management

- **Job Management**

  - Post new job opportunities
  - Advanced job search with filters
  - Detailed job listings with company information

- **Company Profiles**
  - Comprehensive company information
  - Company ratings and reviews
  - Job history and current openings

## 🛠 Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Flask-Login
- **Security**: Werkzeug Security

## 📦 Prerequisites

- Python 3.8+
- pip (Python package manager)
- SQLite3

## 🚀 Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/job-board-flask.git
cd job-board-flask
```

2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Initialize the database

```bash
flask initdb
```

5. Start the development server

```bash
flask run
```

## 🔧 Configuration

Copy `.env.example` to `.env` and update the following variables:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///job_board.db
```

## 📝 API Documentation

### Authentication

```
POST /api/register
POST /api/login
GET /api/logout
```

### Jobs

```
GET /api/jobs
POST /api/jobs
GET /api/jobs/<id>
PUT /api/jobs/<id>
DELETE /api/jobs/<id>
```

### Companies

```
GET /api/companies
POST /api/companies
GET /api/companies/<id>
POST /api/companies/<id>/ratings
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - _Initial work_ - [YourGithub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc

---

<p align="center">Made with ❤️ by Your Name</p>
