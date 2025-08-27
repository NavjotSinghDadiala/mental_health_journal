# Akshar Mental Health Journal

## Overview
Akshar is a comprehensive mental health journal and assistant platform designed to help users track their mental well-being, schedule therapy calls, analyze emotions, and receive recommendations. It integrates journaling, reporting, scheduling, and analysis features, with a user-friendly interface and data visualization.

## Features
- **Journaling:** Log daily mental health entries and activities.
- **Emotion Analysis:** Visualize emotional trends and user activity.
- **Therapy Calls:** Schedule and manage therapy sessions.
- **Recommendations:** Get personalized suggestions for mental wellness.
- **Pomodoro Timer:** Use productivity tools to manage time and focus.
- **Reports:** Generate mental health reports and summaries.
- **User Management:** Secure user authentication and data storage.

## Folder Structure
```
├── akshar.py                  # Akshar module (details TBD)
├── assistantmain.py           # Main assistant logic
├── build.sh                   # Build script
├── cbt.py                     # Cognitive Behavioral Therapy module
├── gui.py                     # Graphical User Interface
├── instance/
│   └── users.db               # User database (SQLite)
├── journal_logs.csv           # Journal log data
├── logs/                      # (Empty or for future logs)
├── mental_health_report.pdf    # Example report
├── models.py                  # Database models
├── payment.py                 # Payment processing
├── pomodoro.py                # Pomodoro timer logic
├── recommendation.py          # Recommendation engine
├── record.mp3.mp3             # Audio recording
├── report.py                  # Report generation
├── requirements.txt           # Python dependencies
├── research_module.py         # Research and analysis tools
├── schedule_call_module.py    # Therapy call scheduling
├── static/
│   └── analysis/
│       ├── confidence_distribution.png
│       ├── emotion_by_user.png
│       ├── emotion_distribution.png
│       ├── posts_over_time.png
│       └── user_activity.png
├── templates/
│   ├── admin_dashboard.html   # Admin dashboard UI
│   ├── anjum_wrapper.html     # UI wrapper
│   ├── community.html         # Community page
│   ├── home.html              # Home page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
├── textmodel.py               # Text analysis/modeling
├── tomato.png                 # Pomodoro icon
├── users.db                   # User database (duplicate)
├── user_analysis.py           # User data analysis
├── __pycache__/               # Python cache files
```

## Usage
- Log in or register via the web interface.
- Add journal entries and view emotion analysis charts.
- Schedule therapy calls and generate reports.
- Use the Pomodoro timer for productivity.

## Data & Visualization
- Visualizations are stored in `static/analysis/` as PNG files.
- Journal logs are saved in `journal_logs.csv`.
- User data is managed in `instance/users.db`.

## License
This project is licensed under the MIT License.

