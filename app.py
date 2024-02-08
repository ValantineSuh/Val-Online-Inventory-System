from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Online inventory system'

app.run(host='0.0.0.0', port=5000)