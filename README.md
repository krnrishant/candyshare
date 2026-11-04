* * *

🍬 Candy Share — File Sharing Made Easy

Candy Share is a simple, lightweight web application for sharing files securely and easily between devices.Users can upload a file (up to 100 MB) and receive a one-time passcode (OTP) to download it from another device within 24 hours.

* * *

🚀 Features

📤 Upload files up to 100 MB

🔒 Retrieve files securely using a 6-digit OTP code

⏰ Files automatically expire after 24 hours

⚡ Built with Flask (Python) and a responsive UI using Tailwind CSS

🧹 Auto-cleanup system for expired files

* * *

🧩 Tech Stack

Layer Technology

Frontend HTML, CSS (Tailwind CSS)Backend Python (Flask)Storage Local uploads/ folderLibraries Flask, Werkzeug, secrets, datetime, json

* * *

📁 Project Structure

CandyShare/│├── app.py # Main Flask application├── templates/│ └── index.html # Frontend interface├── uploads/ # Directory for uploaded files (auto-created)└── README.md # Project documentation

* * *

🖥️ How It Works

1. Upload a file

Choose or drag & drop a file (max 100 MB)

A unique OTP code (e.g., A1B2C3) is generated

2. Share the code

Give the code to the recipient

3. Receive the file

Enter the code in the “Receive File” modal

The file is downloaded instantly

4. Auto Expiration

Files are automatically deleted after 24 hours

* * *

🧠 Key Backend Logic

File Upload:Validates size & type, saves the file with an OTP prefix (e.g., ABC123_filename.txt)

Code Generation:Uses Python’s secrets library to generate secure 6-character alphanumeric codes

Download Handling:Checks expiration, increments download count, and serves the file

Cleanup:Expired files are deleted automatically before each request

* * *

🔒 Allowed File Types

txt, pdf, png, jpg, jpeg, gif, doc, docx, zip, mp4, mp3

* * *

👨‍💻 Author

Rishant Karn, A high school student & aspiring developer from Janakpur.

🌐 karnrishant.vercel.app

🐙 GitHub: @rishantkarn
