from fastapi import FastAPI, HTTPException, Query, Request
from scraper import Scraper
import hashlib, time
from functools import wraps
from typing import Any, Callable

app = FastAPI(
    title="Aptoide Scraper API",
    description="An API that scrapes Aptoide app data using package name.",
    version="1.0.0",
)

# Initialize scraper instance
scraper = Scraper()

# Initialize API
app = FastAPI()

# Simple Rate limiter to enable scability and fair usage of resources by the users
def rate_limit(max_calls: int, period: int):
    """
    Simple in-memory rate limiter (per client IP).
    max_calls = number of allowed requests
    period = time window in seconds
    """
    usage: dict[str, list[float]] = {}

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:

            request: Request | None = kwargs.get("request")

            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if not request or not request.client:
                raise HTTPException(status_code=400, detail="Cannot determine client IP")

            # Unique ID = hash of IP
            ip_address = request.client.host
            unique_id = hashlib.sha256(ip_address.encode()).hexdigest()

            now = time.time()
            timestamps = usage.setdefault(unique_id, [])
            timestamps[:] = [t for t in timestamps if now - t < period]

            if len(timestamps) >= max_calls:
                wait = period - (now - timestamps[0])
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. Try again in {wait:.1f} seconds",
                )

            timestamps.append(now)
            return await func(*args, **kwargs)

        return wrapper

    return decorator


@app.get("/aptoide")
@rate_limit(max_calls=10, period=60)
async def getAppData(
    request: Request,
    package_name: str = Query(
        ...,
        # Input validation to make the endpoint more secure
        min_length=3,
        max_length=100,
        pattern=r"^[a-zA-Z0-9._-]+$",
        description="The Aptoide package name (e.g., com.facebook.katana)"
    )
):
    try:
        # Result of the scraping 
        result = scraper.scrapeData(package_name)

        if not result:
            raise HTTPException(status_code=404, detail="App not found or scraping failed.")
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


