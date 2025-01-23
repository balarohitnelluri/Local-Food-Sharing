# Local-Food-Sharing

Local Food Sharing Application

## Overview

The Local Food Sharing Application is a Python-based platform designed to promote sustainability and reduce food waste. It connects users who have surplus food to share with those in need, providing an intuitive interface for food listings, scheduling pickups, and managing activities. The application ensures secure user authentication, seamless data handling, and a visually engaging user experience.

## Features
	•	User Registration & Login: Secure authentication with encrypted passwords.
	•	Food Listings: Add, view, and manage surplus food items with filters for type, location, and expiration date.
	•	Pickup Scheduling: Seamless scheduling of pickups with real-time updates.
	•	Notifications: Alerts for listing updates, approvals, and upcoming pickups.
	•	Reporting: Export detailed user activity and system data in Excel format.
	•	User-Friendly Interface: Built with Tkinter and CustomTkinter for an engaging and intuitive experience.

 <img width="753" alt="image" src="https://github.com/user-attachments/assets/9fac4da7-d928-4b18-9fb4-2323554f85dc" />


## Technologies Used
	•	Programming Language: Python
	•	Frontend: Tkinter, CustomTkinter
	•	Database: MySQL
	•	UI Prototyping: Figma
	•	Version Control: GitHub
	•	Real-Time Data Generation: Talend
	•	Reporting: Pandas for generating Excel reports

## Installation Instructions
	1.	Clone the Repository:

git clone [repository-url]
cd local-food-sharing-app


	2.	Install Dependencies:

pip install -r requirements.txt


	3.	Set Up MySQL Database:
	•	Install and configure MySQL.
	•	Run the SQL scripts in the sql/ folder to set up the database schema.
	4.	Run the Application:

python main.py

## Project Structure

local-food-sharing-app/
│
├── gui/                   # UI components
├── assets/                # Images, icons, and fonts for styling
├── sql/                   # Database scripts
├── main.py                # Entry point for the application
├── config.py              # Database configuration
├── controller.py          # Backend logic and workflows
├── utils.py               # Helper functions
└── requirements.txt       # Python dependencies

## How to Use

1. User Registration & Login
	•	New users can sign up by providing their name, email, and password.
	•	Existing users can log in securely using their registered credentials.

2. Adding Food Listings
	•	Navigate to the Add Listings screen.
	•	Provide details such as food type, quantity, expiration date, and location.

3. Scheduling Pickups
	•	Browse available food listings and request a pickup.
	•	Schedule a convenient date and time, with notifications for confirmation.

4. Managing Notifications
	•	View requests received for your listings and approve or decline them.
	•	Stay updated with alerts for listing updates and scheduled pickups.

5. Generating Reports
	•	Access the reporting section to export data on user activity and system performance in Excel format.

## Future Enhancements
	•	Multilingual support for a wider user base.
	•	Mobile app integration for on-the-go access.
	•	AI-powered recommendations for food-sharing opportunities.

## Contributors
	•	Raja Mouli Vodapally
	•	Bala Rohit Nelluri
	•	Ushodaya Hari Podhili
	•	Gurucharan Bhayankara
	•	Gayathri Karnati

## License

This project is licensed under the MIT License.

Feel free to use this as your GitHub README or modify it further to suit your needs!
