from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

def load_json(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'r') as file:
        return json.load(file)

def save_json(filename, data):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    notices = load_json('notices.json')
    return render_template('index.html', notices=notices)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_json('users.json')
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)

        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Credenciais inválidas', 401

    return render_template('login.html')

@app.route('/tickets')
def tickets():
    if 'username' not in session:
        return redirect(url_for('login'))

    tickets = load_json('tickets.json')
    user_tickets = [t for t in tickets if t['user'] == session['username']]
    return render_template('tickets.html', tickets=user_tickets)

@app.route('/add_ticket', methods=['POST'])
def add_ticket():
    if 'username' not in session:
        return redirect(url_for('login'))

    tickets = load_json('tickets.json')
    new_ticket = {
        'user': session['username'],
        'description': request.form['description'],
        'status': 'Aberto',
        'response': ''
    }
    tickets.append(new_ticket)
    save_json('tickets.json', tickets)
    return redirect(url_for('tickets'))

@app.route('/admin/tickets')
def admin_tickets():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = next((u for u in load_json('users.json') if u['username'] == session['username']), None)
    if user and user['role'] == 'admin':
        tickets = load_json('tickets.json')
        return render_template('admin_tickets.html', tickets=tickets)
    return redirect(url_for('index'))

@app.route('/admin/response_ticket/<int:ticket_id>', methods=['POST'])
def response_ticket(ticket_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    user = next((u for u in load_json('users.json') if u['username'] == session['username']), None)
    if user and user['role'] == 'admin':
        tickets = load_json('tickets.json')
        ticket = tickets[ticket_id]
        ticket['response'] = request.form['response']
        ticket['status'] = request.form['status']
        save_json('tickets.json', tickets)
        return redirect(url_for('admin_tickets'))

    return redirect(url_for('index'))

@app.route('/accounts')
def accounts():
    if 'username' not in session:
        return redirect(url_for('login'))

    accounts = load_json('accounts.json')
    user_accounts = [a for a in accounts if a['user'] == session['username']]
    return render_template('accounts.html', accounts=user_accounts)

@app.route('/admin/accounts')
def admin_accounts():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = next((u for u in load_json('users.json') if u['username'] == session['username']), None)
    if user and user['role'] == 'admin':
        accounts = load_json('accounts.json')
        return render_template('admin_accounts.html', accounts=accounts)
    return redirect(url_for('index'))

@app.route('/admin/update_account/<int:account_id>', methods=['POST'])
def update_account(account_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    user = next((u for u in load_json('users.json') if u['username'] == session['username']), None)
    if user and user['role'] == 'admin':
        accounts = load_json('accounts.json')
        account = accounts[account_id]
        account['status'] = request.form['status']
        save_json('accounts.json', accounts)
        return redirect(url_for('admin_accounts'))

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
