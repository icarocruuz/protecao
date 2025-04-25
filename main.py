
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

    return {
        "status_code": response.status_code,
        "body": response.json() if "application/json" in response.headers.get("content-type", "") else response.text,
    }
