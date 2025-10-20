from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
import requests

app = FastAPI()

@app.get("/me")
async def get_me():
    current_timestamp = datetime.now(timezone.utc).isoformat()

    try:
        # Fetch a random cat fact with a short timeout
        response = requests.get("https://catfact.ninja/fact", timeout=3)
        response.raise_for_status()  # raise error for 4xx/5xx
        random_cat_fact = response.json().get("fact", "No fact found.")
        http_status = status.HTTP_200_OK
    except requests.exceptions.RequestException as e:
        # Handle timeout, network issues, or invalid response
        random_cat_fact = "Could not fetch a cat fact right now. Please try again later."
        http_status = status.HTTP_503_SERVICE_UNAVAILABLE

    user_data = {
        "status": "success" if http_status == 200 else "error",
        "user": {
            "email": "kinyattipaul@gmail.com",
            "name": "Paul Kinyatti",
            "stack": "Python, FastAPI"
        },
        "timestamp": current_timestamp,
        "fact": random_cat_fact
    }

    # Return JSON with proper status code
    return JSONResponse(content=user_data, status_code=http_status)
