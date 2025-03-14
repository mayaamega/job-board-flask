# Job Board Application

A modern job board platform built with Flask, Next.js, and SQLite, featuring a responsive UI powered by Shadcn components. This application enables employers to post jobs, job seekers to search and apply for positions, and provides a seamless user experience for managing job listings and company profiles.

## Features

- **Job Listings**: Browse and search through available job positions
- **Company Profiles**: Detailed company information and available positions
- **User Authentication**: Secure login and registration system
- **Job Posting**: Easy-to-use interface for employers to post new positions
- **Search Functionality**: Advanced search capabilities for jobs and companies
- **Responsive Design**: Modern UI that works across all devices

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Next.js, React
- **UI Components**: Shadcn UI
- **Database**: SQLite
- **Styling**: Tailwind CSS

## Prerequisites

- Python 3.x
- Node.js (Latest LTS version)
- pnpm (Package manager)

## Installation

1. Clone the repository

```bash
git clone <repository-url>
cd job-board-flask
```

2. Set up the Python virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

3. Install frontend dependencies

```bash
pnpm install
```

4. Initialize the database

```bash
sqlite3 database.db < schema.sql
```

## Development

1. Start the Flask backend server

```bash
flask run --debug
```

2. In a separate terminal, start the frontend development server

```bash
pnpm dev
```

The application will be available at:

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Project Structure

```
├── app/                 # Next.js frontend application
├── components/          # Reusable UI components
├── lib/                 # Utility functions and helpers
├── static/             # Static assets (CSS, JS)
├── templates/          # Flask HTML templates
├── schema.sql          # Database schema
└── app.py              # Flask application entry point
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Shadcn UI](https://ui.shadcn.com/) for the beautiful component library
- [Flask](https://flask.palletsprojects.com/) for the backend framework
- [Next.js](https://nextjs.org/) for the frontend framework
