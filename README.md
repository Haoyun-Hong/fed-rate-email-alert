# Fed Rate Email Alert 🔔

A Python script that checks for U.S. Federal Reserve interest rate changes and sends email notifications after each FOMC meeting.

## Features
- Uses NewsAPI to monitor Fed rate announcements.
- Sends an email if a rate change is detected in the news.
- Easily customizable and automatable with cron.

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/fed-rate-email-alert.git
cd fed-rate-email-alert
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
Edit `config.py` with your email and NewsAPI credentials.

### 4. Run
```bash
python fed_alert.py
```

## License
MIT
