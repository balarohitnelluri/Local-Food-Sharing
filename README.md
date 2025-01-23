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

        <img width="432" alt="image" src="https://github.com/user-attachments/assets/206f0495-7324-4fa3-98b8-091295579dee" />

	•	Existing users can log in securely using their registered credentials.

        <img width="434" alt="image" src="https://github.com/user-attachments/assets/19fb0540-464a-49cb-865c-987b4723003d" />

    •	If the customer forgot the password will able to reset the password.

        <img width="432" alt="image" src="https://github.com/user-attachments/assets/404bdbe3-18a2-45e3-a6af-7abda8bb5895" />

       - You'll get a One Time Password to your email

        <img width="432" alt="image" src="https://github.com/user-attachments/assets/ee846b17-6c9c-4253-9e10-3f5ceb9dcbf5" />

       - Once after you login you'll go to main window

        <img width="432" alt="image" src="https://github.com/user-attachments/assets/ccabbda0-9d58-4879-bb1c-43dc22697562" />

3. Adding Food Listings
	•	Navigate to the Add Listings screen.
	•	Provide details such as food type, quantity, expiration date, and location.
    
    <img width="432" alt="image" src="https://github.com/user-attachments/assets/a2108f44-88c2-461b-9012-9481900792fa" />


5. Scheduling Pickups
	•	Browse available food listings and request a pickup.
	•	Schedule a convenient date and time, with notifications for confirmation.

    <img width="432" alt="image" src="https://github.com/user-attachments/assets/aace646c-f1ea-40d7-978c-41d7596d1f52" />

    <img width="432" alt="image" src="https://github.com/user-attachments/assets/cd687314-cd96-4586-bd4c-4d00987f7934" />



7. Managing Notifications
	•	View requests received for your listings and approve or decline them.
	•	Stay updated with alerts for listing updates and scheduled pickups.

    <img width="432" alt="image" src="https://github.com/user-attachments/assets/c0b2a346-f8b2-4ccf-9086-9143dbcc25cc" />


9. Generating Reports
	•	Access the reporting section to export data on user activity and system performance in Excel format.

    <img width="432" alt="image" src="https://github.com/user-attachments/assets/d184ed7a-46b5-41c0-bdcd-d2678a2682c3" />


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
