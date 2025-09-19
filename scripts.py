import requests

url = "https://newsapi.org/v2/top-headlines"
params = {
    "country": "us",      
    "pageSize": 1,
    "apiKey": "940f88fa68244975ad6c3cd66b41dbca"
}

response = requests.get(url, params=params)
data = response.json()

print(data)

if data.get("status") == "ok":
    for article in data.get("articles", []):
        print(article["title"], "→", article["url"])
else:
    print("Ошибка:", data)
