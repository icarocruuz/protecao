
from fastapi import FastAPI, Request
import httpx

app = FastAPI()

API_BULLEX_URL = "https://api-bullex.onrender.com"

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, path: str):
    url = f"{API_BULLEX_URL}/{path}"
    method = request.method
    headers = dict(request.headers)
    body = await request.body()

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method, url, headers=headers, content=body
        )

    try:
        content = response.json()
    except Exception:
        content = response.text

    print("REQUEST:", method, url)
    print("STATUS:", response.status_code)
    print("HEADERS:", dict(response.headers))
    print("RESPONSE:", content)

    return {
        "status_code": response.status_code,
        "body": content,
    }
