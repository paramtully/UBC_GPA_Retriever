from flask import Flask, redirect, request, url_for
from models.GPACalculator import GPACalculator

app = Flask(__name__)

@app.route('/summary', methods=['POST'])
def summary():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            session = request.form.get('session')
            print(f"username: {username}, password: {password}, session: {session}")
            if not username or not password: raise ValueError('username or password not provided')
            summary = GPACalculator().getSummary(username, password, session)
            if summary: return {'average': summary[0],
                                'gpa4': summary[1],
                                'gpa433': summary[2]}
        return {'error': 'Summary was not found. Try re-entering your login or try a different session.'}
    except Exception as e:
        return {'error': e}

app.run(host="0.0.0.0", port=80)

if __name__ == "__main__":
    app.run(debug=True)