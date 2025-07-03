import requests
import smtplib
from email.mime.text import MIMEText
import schedule
import time
import os 

def check_fed_news():
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': 'federal reserve interest rate',
        'apiKey': os.getenv("NEWS_API_KEY"),
        'sortBy': 'publishedAt',
        'language': 'en'
    }
    response = requests.get(url, params=params)
    articles = response.json().get('articles', [])

    for article in articles[:5]:  # Limit to latest 5 articles
        title = article['title'].lower()
         # Detect rate change types
        if 'raises rates' in title or 'rate hike' in title or 'increases rates' in title:
            return "[Fed Raises Rates] " + article['title'], article['url']
        elif 'cuts rates' in title or 'lowers rates' in title or 'reduces rates' in title:
            return "[Fed Cuts Rates] " + article['title'], article['url']
        elif 'keeps rates' in title or 'holds rates' in title or 'leaves rates unchanged' in title or 'maintains rates' in title:
            return "[Fed Holds Steady] " + article['title'], article['url']
        
    return None, None

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = os.getenv("EMAIL_ADDRESS")
    msg['To'] = os.getenv("TO_EMAIL")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)

def main():
    title, link = check_fed_news()
    if title:
        send_email(f"[Fed Update] {title}", f"Read more: {link}")
    else:
        send_email(f"[Fed Update]", "No Fed update detected.")
        #print("No Fed update detected.")

if __name__ == "__main__":
    main()
