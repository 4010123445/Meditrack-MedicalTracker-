🩺 MediTrack – Desktop Medical Management System
📌 Overview

MediTrack is a desktop application designed to help users manage patient records, medications, medical appointments, and automated reminders. The system provides popup notifications and text-to-speech alerts to ensure timely medication intake and appointment attendance. It offers a user-friendly interface integrated with a local database for reliable data storage.

🎯 Features

Patient management with full CRUD operations

Medication tracking and history per patient

Appointment scheduling with calendar and time picker

Automated reminders with popup and voice alerts

Search and filter functions for easy data retrieval

Centralized main menu for navigation

🛠 Technologies Used

Python

Tkinter (GUI)

SQLite (local database)

Text-to-Speech (pyttsx3)

▶ How to Run the Application
Requirements

Python 3.10 or higher

Setup

Download or extract the MediTrack project folder

Install required libraries:

py -m pip install pyttsx3 tkcalendar


Run the application:

py main.py

🗄 Database

MediTrack uses a local SQLite database file (meditrack.db) that is automatically created when the app runs for the first time. No additional database setup is required.

📄 Project Purpose

This application was developed as a final term project to demonstrate object-oriented programming, desktop GUI development, and database integration while addressing a real-world healthcare management problem.

👨‍💻 Developer Notes

The reminder system runs in the background while the application is active

All data is stored locally for portability and ease of use

Designed for everyday healthcare management
