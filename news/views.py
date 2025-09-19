import requests
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Article
from .serializers import ArticleSerializer


NEWS_API_URL = "https://newsapi.org/v2/top-headlines?country=us"
API_KEY = settings.NEWS_API_KEY


@api_view(["POST"])
def update_articles(request):
    cache_key = "articles_update"
    if cache.get(cache_key):
        return Response({"detail": "Данные недавно обновлялись"}, status=200)

    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(NEWS_API_URL, headers=headers)
    if response.status_code != 200:
        return Response({"error": "Ошибка при запросе к NewsAPI"}, status=500)

    data = response.json().get("articles", [])
    created_count = 0

    for item in data:
        if not Article.objects.filter(url=item["url"]).exists():
            Article.objects.create(
                source_id=item.get("source", {}).get("id"),
                source_name=item.get("source", {}).get("name", ""),
                author=item.get("author"),
                title=item.get("title"),
                description=item.get("description"),
                url=item.get("url"),
                url_to_image=item.get("urlToImage"),
                published_at=item.get("publishedAt"),
                content=item.get("content"),
            )
            created_count += 1

    cache.set(cache_key, True, timeout=30 * 60)
    return Response({"created": created_count}, status=201)


@api_view(["GET"])
def list_articles(request):
    cache_key = f"articles_list_{request.get_full_path()}"
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    qs = Article.objects.all()
    filters = {}

    fresh = request.query_params.get("fresh")
    if fresh == "true":
        since = timezone.now() - timedelta(hours=24)
        filters["published_at__gte"] = since

    title_contains = request.query_params.get("title")
    if title_contains:
        filters["title__icontains"] = title_contains

    if filters:
        qs = qs.filter(**filters)

    serializer = ArticleSerializer(qs, many=True)
    result = serializer.data
    cache.set(cache_key, result, timeout=10 * 60)
    return Response(result)
