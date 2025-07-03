import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import os 

def check_fed_news():
    # Mock data simulating NewsAPI articles with Fed rate news
    return [
        {
            "title": "Solid Jobs Report Keeps Fed Rate Cuts at Bay",
            "url": "https://www.nytimes.com/2025/07/03/business/jobs-fed-rate-cuts.html"
        },
        {
            "title": "Powell confirms that the Fed would have cut by now were it not for tariffs",
            "url": "https://www.cnbc.com/2025/07/01/powell-confirms-that-the-fed-would-have-cut-by-now-were-it-not-for-tariffs.html"
        },
        {
            "title": "US dollar rises, British pound falls as markets weigh trade deals, Fed rate cut",
            "url": "https://www.reuters.com/world/middle-east/dollar-wallows-near-3-12-year-low-fed-cuts-trump-bill-focus-2025-07-02/"
        },
    ]
    # url = 'https://newsapi.org/v2/everything'
    # time_24h_ago = datetime.utcnow() - timedelta(days=1)
    # from_time = time_24h_ago.strftime("%Y-%m-%dT%H:%M:%SZ")

    # params = {
    #     'q': 'federal reserve interest rate',
    #     'apiKey': os.getenv("NEWS_API_KEY"),
    #     'sortBy': 'publishedAt',
    #     "from": from_time,
    #     'language': 'en'
    # }

    # response = requests.get(url, params=params)
    # if response.status_code != 200:
    #     print(f"Error fetching news: {response.status_code}")
    #     return []

    # data = response.json()
    # articles = data.get("articles", [])

    # keywords = ["raise", "cut", "hike", "lower", "increase", "decrease", 
    #             "hold", "unchanged", "pause", "steady", "keeps", "maintain"]

    # relevant_articles = []
    # for article in articles:
    #     title = article['title'].lower()
    #     if any(kw in title for kw in keywords):
    #         relevant_articles.append(article)

    # return relevant_articles

def send_email(subject, body, html=False):
    if html:
        msg = MIMEText(body, 'html')
    else:
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
        html_lines = [
            '<div style="font-family: Arial, sans-serif; line-height: 1.5; color: #333;">',
            '<h2 style="color: #2c3e50;">Latest Fed News Updates</h2>',
            '<ul style="padding-left: 20px;">'
        ]
        for article in articles:
            title = article['title']
            url = article['url']
            html_lines.append(
                f'<li style="margin-bottom: 12px;">'
                f'<a href="{url}" '
                f'style="color: #1a73e8; text-decoration: none; font-weight: 600;" '
                f'target="_blank" rel="noopener noreferrer">{title}</a>'
                f'</li>'
            )
        html_lines.append('</ul></div>')
        body = '\n'.join(html_lines)
        send_email("[Fed Update] Latest Articles", body, html=True)
    else:
        send_email("[Fed Update]", "No Fed update detected.")

if __name__ == "__main__":
    main()
