from fastapi import FastAPI, BackgroundTasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from jobs import fetch_pitchfork, process_pitchfork, create_spotify_playlist
from utils.logger import log
import uvicorn
import asyncio
from contextlib import asynccontextmanager

scheduler = None
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global scheduler
    scheduler = AsyncIOScheduler()

    # Schedule the daily job
    scheduler.add_job(
        run_daily_job,
        trigger=CronTrigger(hour=9, minute=0),
        id="daily_pitchfork_job",
        name="Daily Pitchfork data fetch",
        replace_existing=True
    )
    
    scheduler.start()
    log("Scheduler started - daily job scheduled for 9:00 AM")
    
    yield
    
    # Shutdown
    if scheduler:
        scheduler.shutdown()
    log("Scheduler stopped")
    

app = FastAPI(lifespan=lifespan)

def run_daily_job():
    """Run the daily pitchfork data collection job"""
    try:
        log("Running daily job")
        playlistArticles = fetch_pitchfork()
        [songs, albums] = process_pitchfork(playlistArticles)
        create_spotify_playlist(songs, albums)
        log("Daily job completed")
    except Exception as e:
        log(f"Daily job failed: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "AI Playlist Generator Service", "status": "running"}

@app.post("/jobs/trigger")
async def trigger_job(background_tasks: BackgroundTasks):
    """Manually trigger the daily job"""
    background_tasks.add_task(run_daily_job)
    return {"message": "Daily job triggered"}

@app.get("/jobs/status")
def get_job_status():
    """Get the status of the daily job"""
    if not scheduler:
        return {"error": "Scheduler not running"}
    
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "next_run_time": str(job.next_run_time) if job.next_run_time else None,
            "trigger": str(job.trigger)
        })
    return {"jobs": jobs}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    