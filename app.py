# voice_assistant.py

from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    # Run the Python script in a separate process
    subprocess.Popen(['python', 'voice_assistant.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
