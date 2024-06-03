from flask import Flask, render_template, redirect, url_for, request, send_file
import hashlib
import io
from rq import Queue
from redis import Redis
from datetime import date
import time

redis_client = Redis()
queue = Queue(connection=redis_client)

def process_upload(id):
    print(id)
    # TODO: parse spreadsheet
    # TODO: trigger data analysis job
    time.sleep(10)
    redis_client.set(id, "NAME,AGE\nKurtis,38")

def data_analysis(id):
    # TODO: fetch from cache
    # TODO: write csv to cache
    pass

app = Flask(__name__)

@app.get("/new")
def new_upload():
    return render_template("new.html")

@app.post("/upload")
def upload_file():
    file = request.files["data"]
    # TODO: parse file 
    # TODO: cache file with id
    id = hashlib.md5(file.read()).hexdigest()
    queue.enqueue(process_upload, id)
    return redirect(url_for("check_download", id=id))

@app.get("/<id>")
def check_download(id=None):
    if id is None:
        return redirect(url_for("new_upload"))
    
    if redis_client.exists(id):
        return send_file(io.BytesIO(redis_client.get(id)), "text/csv", as_attachment=True, download_name=f"opbs_{date.today()}_{id}.csv")
    
    time.sleep(1)
    return redirect(url_for("check_download", id=id))