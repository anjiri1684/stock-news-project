import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "XMRWHIY45QR8QTRH"
NEWS_API_KEY = "b24948c97876418eacce8fa0725ccc8b"
account_sid = 'ACdaeb35a45b9a54a57a1ecc89056d33b4'
auth_token = '73a21a79146c8d5f1924ce677498ad0f'

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "⬆️"
else:
    up_down = "⬇️"
dif_percent = round((difference / float(yesterday_closing_price)) * 100)
print(dif_percent)

if abs(dif_percent) > -5:
    news_params = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    print(articles)

    three_articles = articles[:3]
    print(three_articles)

    formatted_articles = [f"{STOCK_NAME}: {up_down}{dif_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in
                          three_articles]
    client = Client(account_sid, auth_token)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+14352646818",
            to="+254705423996"
        )

