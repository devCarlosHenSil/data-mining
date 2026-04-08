import httpx
from datetime import datetime, timedelta

async def fetch_upcoming_animes(days: int = 30):
    query = """
    query ($page: Int, $perPage: Int, $start: String) {
      Page(page: $page, perPage: $perPage) {
        media(type: ANIME, status_in: [NOT_YET_RELEASED, RELEASING], startDate_greater: $start) {
          title { romaji }
          startDate { year month day }
        }
      }
    }
    """
    variables = {"page": 1, "perPage": 50, "start": (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")}

    async with httpx.AsyncClient(verify=False) as client:
        r = await client.post("https://graphql.anilist.co", json={"query": query, "variables": variables})
        data = r.json()["data"]["Page"]["media"]

    events = []
    for m in data[:10]:  # top 10 relevantes
        title = m["title"]["romaji"]
        d = m["startDate"]
        date_str = f"{d['day']:02d}/{d['month']:02d}/{d['year']}" if d["year"] else "em breve"
        days_left = (datetime(d["year"], d["month"], d["day"]) - datetime.now()).days if d["year"] else 30
        relevance = "Alta relevância" if days_left < 15 else "Relevante"
        events.append({"title": title, "date": date_str, "days": days_left, "relevance": relevance})
        await save_event(title, date_str, relevance)  # idempotente

    return events