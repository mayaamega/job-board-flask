# Job Board Application

A modern job board platform built with Flask and Next.js, featuring job listings, company profiles, and user ratings.

## Features

- **Job Listings**: Browse and search through job postings with detailed information
- **Company Profiles**: View company details and employee ratings
- **User Authentication**: Secure registration and login system
- **Job Posting**: Employers can post new job opportunities
- **Company Ratings**: Users can rate and review companies
- **Modern UI**: Responsive design with Radix UI components and Tailwind CSS

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Next.js, React
- **Database**: SQLite
- **UI Components**: Radix UI
- **Styling**: Tailwind CSS
- **Icons**: Font Awesome

## Prerequisites

- Python 3.x
- Node.js and npm/pnpm
- SQLite

## Setup

1. Clone the repository

```bash
git clone <repository-url>
cd job-board-flask
```

2. Set up Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Initialize the database

```bash
flask initdb
```

4. Install frontend dependencies

```bash
pnpm install
```

5. Start the development server

```bash
# Start Flask backend
flask run

# In a separate terminal, start the frontend
pnpm run dev
```
