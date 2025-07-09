from fastapi import FastAPI
from jobs import fetch_pitchfork, process_pitchfork, store_pitchfork
from utils.logger import log

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

def run_daily_job():
    log("Running daily job")
    articles = fetch_pitchfork()
    music = process_pitchfork(articles)
    store_pitchfork(music)
    log("Daily job completed")
    

if (__name__ == "__main__"):
    run_daily_job()