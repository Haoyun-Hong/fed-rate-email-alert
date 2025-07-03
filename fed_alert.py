import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import os 

def check_fed_news():
    url = 'https://newsapi.org/v2/everything'
    time_24h_ago = datetime.utcnow() - timedelta(days=1)
    from_time = time_24h_ago.strftime("%Y-%m-%dT%H:%M:%SZ")

    params = {
        'q': 'federal reserve interest rate',
        'apiKey': os.getenv("NEWS_API_KEY"),
        'sortBy': 'publishedAt',
        "from": from_time,
        'language': 'en'
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error fetching news: {response.status_code}")
        return []

    data = response.json()
    articles = data.get("articles", [])

    keywords = ["raise", "cut", "hike", "lower", "increase", "decrease", 
                "hold", "unchanged", "pause", "steady", "keeps", "maintain"]

    relevant_articles = []
    for article in articles:
        title = article['title'].lower()
        if any(kw in title for kw in keywords):
            relevant_articles.append(article)

    return relevant_articles

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = os.getenv("EMAIL_ADDRESS")
    msg['To'] = os.getenv("TO_EMAIL")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)

def main():
    articles = check_fed_news()
    if articles:
        html_lines = ['<h2>Latest Fed News Updates</h2>', '<ul>']
        for article in articles:
            title = article['title']
            url = article['url']
            html_lines.append(f'<li><a href="{url}" style="text-decoration:none; color:#1a0dab;">{title}</a></li>')
        html_lines.append('</ul>')
        body = '\n'.join(html_lines)
        send_email("[Fed Update] Latest Articles", body, html=True)
    else:
        send_email("[Fed Update]", "No Fed update detected.")

if __name__ == "__main__":
    main()
