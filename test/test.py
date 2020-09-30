from flask import Flask
import redis, rq, time
from task import task

app = Flask(__name__)

r = redis.Redis()
q = rq.Queue(connection=r)


def task():
    print('Hahaha')
    time.sleep(2)
    
@app.route('/')
def home():
    q.enqueue(task)
    return "a"

app.run(debug=True)