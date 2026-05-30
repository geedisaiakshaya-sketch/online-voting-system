import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/vote', methods=['POST'])
def vote():
    username = request.form['username']
    return render_template('vote.html', username=username)

@app.route('/submit_vote', methods=['POST'])
def submit_vote():

    username = request.form['username']
    candidate = request.form['candidate']

    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM votes WHERE username=?",
        (username,)
    )

    existing_vote = cursor.fetchone()

    if existing_vote:
        conn.close()
        return "<h2>You have already voted!</h2>"

    cursor.execute(
        "INSERT INTO votes (username, candidate) VALUES (?, ?)",
        (username, candidate)
    )

    conn.commit()
    conn.close()

    return render_template(
        'results.html',
        username=username,
        candidate=candidate
    )
@app.route('/admin')
def admin():

    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT candidate, COUNT(*)
        FROM votes
        GROUP BY candidate
    """)

    results = cursor.fetchall()

    conn.close()

    return render_template(
        'admin.html',
        results=results
    )

if __name__ == '__main__':
    app.run(debug=True)