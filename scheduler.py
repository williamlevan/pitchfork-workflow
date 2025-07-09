from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from jobs import fetch_pitchfork, process_pitchfork, store_pitchfork
from utils.logger import log

def run_daily_job():
    log("Running daily job")
    articles = fetch_pitchfork()
    music = process_pitchfork(articles)
    store_pitchfork(music)
    log("Daily job completed")

def main():
    scheduler = BlockingScheduler()
    
    # Schedule the job to run daily at 9:00 AM
    scheduler.add_job(
        run_daily_job,
        trigger=CronTrigger(hour=9, minute=0),
        id="daily_pitchfork_job",
        name="Daily Pitchfork data fetch",
        replace_existing=True
    )
    
    log("Scheduler started - daily job scheduled for 9:00 AM")
    log("Press Ctrl+C to exit")
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        log("Scheduler stopped by user")
        scheduler.shutdown()

if __name__ == "__main__":
    main() 