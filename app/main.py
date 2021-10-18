import uvicorn
from fastapi import FastAPI

from app.watchdog import Watchdog
from config import settings

app = FastAPI()
watchdog = Watchdog(settings.paths)


@app.get("/")
async def get():
    return {"status": "ok"}


@app.get("/stats")
async def get_stats():
    stats = watchdog.get_stats()
    return stats


@app.post("/keep_alive/{player_id}")
async def keep_alive(player_id: str):
    watchdog.handle_player_call(player_id)
    return "succesfull ping"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, workers=1)
