DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS company_ratings;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    user_type TEXT NOT NULL,  -- 'job_seeker' or 'employer'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    website TEXT,
    location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company_id INTEGER NOT NULL,
    location TEXT NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT,
    salary_range TEXT,
    posted_date DATE NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies (id)
);

CREATE TABLE company_ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Insert sample data
INSERT INTO companies (name, description, website, location) VALUES
('TechCorp', 'A leading technology company', 'https://techcorp.example.com', 'San Francisco, CA'),
('DesignHub', 'Creative design agency', 'https://designhub.example.com', 'New York, NY'),
('DataSystems', 'Big data and analytics', 'https://datasystems.example.com', 'Austin, TX');

INSERT INTO jobs (title, company_id, location, description, requirements, salary_range, posted_date) VALUES
('Senior Software Engineer', 1, 'San Francisco, CA', 'Join our team to build cutting-edge software solutions.', 'Python, JavaScript, 5+ years experience', '$120,000 - $150,000', '2023-05-15'),
('UX Designer', 2, 'New York, NY', 'Design beautiful and intuitive user interfaces for our clients.', 'Figma, Adobe XD, 3+ years experience', '$90,000 - $110,000', '2023-05-14'),
('Data Scientist', 3, 'Austin, TX', 'Analyze complex data sets to drive business decisions.', 'Python, SQL, Machine Learning, 2+ years experience', '$100,000 - $130,000', '2023-05-13'),
('Frontend Developer', 1, 'Remote', 'Build responsive web applications using modern frameworks.', 'React, TypeScript, 2+ years experience', '$80,000 - $110,000', '2023-05-12'),
('Product Manager', 2, 'New York, NY', 'Lead product development from conception to launch.', 'Agile, 4+ years experience in tech', '$110,000 - $140,000', '2023-05-11');

