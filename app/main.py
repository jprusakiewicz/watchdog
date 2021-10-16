import uvicorn
from fastapi import FastAPI

from app.watchdog import Watchdog
from config import settings

app = FastAPI()
watchdog = Watchdog(settings.paths)


@app.get("/")
async def get():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001, workers=1)
