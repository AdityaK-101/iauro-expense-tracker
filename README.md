# Expense Tracker (Full Stack Application)

## Overview
This is a full-stack Expense Tracker application developed using Flask and SQLite. It allows users to manage their daily expenses with authentication, CRUD operations, and data visualization.

## Features

### Authentication
- User Signup
- User Login (session-based authentication)
- Logout functionality

### Expense Management
- Add Expense (Category, Amount, Comments)
- View Expenses in table format (sorted by latest)
- Edit existing expenses
- Delete expenses

### Data Visualization
- Pie chart showing category-wise expense distribution
- Percentage representation in chart

### Additional Features
- Auto-suggestions for categories using datalist
- Created At and Updated At timestamps
- Clean and responsive UI using Bootstrap

## Tech Stack
- Backend: Flask (Python)
- Database: SQLite
- Frontend: HTML, Bootstrap
- Visualization: Chart.js

## Project Structure
expense-tracker/
├── app.py
├── database.db
├── templates/
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── edit.html
├── requirements.txt
└── README.md

## Setup & Installation

1. Clone the repository
git clone https://github.com/AdityaK-101/iauro-expense-tracker.git
cd expense-tracker

2. Install dependencies
pip install -r requirements.txt

3. Run the application
python app.py

4. Open in browser
http://127.0.0.1:5000

## How It Works
Users register and log in to access the dashboard. Expenses are stored in an SQLite database. The dashboard displays expenses in a table sorted by latest entries. Chart.js is used to visualize category-wise expense distribution. Categories are reused using datalist for better user experience.

## Security Considerations
- Passwords are hashed using Werkzeug
- Session-based authentication is used
- No sensitive data is hardcoded