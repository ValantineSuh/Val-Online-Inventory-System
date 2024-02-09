from flask import Flask, render_template

app = Flask(__name__)

@app.route('/main')
def main():
    # return 'Online inventory system'
    return render_template("main.html")

app.run(host='0.0.0.0', port=5000)