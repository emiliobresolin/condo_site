from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'secret_key'  # Necessário para usar sessões

# Função para carregar os dados de um arquivo JSON
def load_json(filename):
    path = os.path.join(os.path.dirname(__file__), filename)  # Caminho absoluto
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Função para salvar os dados de um arquivo JSON
def save_json(filename, data):
    path = os.path.join(os.path.dirname(__file__), filename)  # Caminho absoluto
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

# Página inicial (avisos)
@app.route('/')
def index():
    notices = load_json('notices.json')
    return render_template('index.html', notices=notices)

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_json('users.json')
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)

        if user:
            session['username'] = username
            # Verificar o papel do usuário
            if user['role'] == 'admin':
                return redirect(url_for('admin'))  # Redireciona para a página admin
            else:
                return redirect(url_for('index'))  # Redireciona para a página inicial
        else:
            return 'Credenciais inválidas', 401

    return render_template('login.html')


# Página de tickets (somente para usuários logados)
@app.route('/tickets')
def tickets():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    tickets = load_json('tickets.json')
    user_tickets = [t for t in tickets if t['user'] == session['username']]
    return render_template('tickets.html', tickets=user_tickets)

# Página de contas (somente para usuários logados)
@app.route('/accounts')
def accounts():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    accounts = load_json('accounts.json')
    user_accounts = [a for a in accounts if a['user'] == session['username']]
    return render_template('accounts.html', accounts=user_accounts)

# Página para admin/síndico gerenciar chamados e contas
@app.route('/admin')
def admin():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Verificar se o usuário logado é um "admin"
    users = load_json('users.json')
    user = next((u for u in users if u['username'] == session['username']), None)

    if user and user['role'] == 'admin':
        tickets = load_json('tickets.json')
        accounts = load_json('accounts.json')
        return render_template('admin.html', tickets=tickets, accounts=accounts)
    else:
        return 'Acesso negado. Você não tem permissão para acessar esta página.', 403  # Pagina de erro 403

# Alterar status de chamados (admin)
@app.route('/update_ticket/<int:ticket_id>', methods=['POST'])
def update_ticket(ticket_id):
    tickets = load_json('tickets.json')
    ticket = tickets[ticket_id]
    ticket['status'] = request.form['status']
    ticket['response'] = request.form.get('response', '')
    save_json('tickets.json', tickets)
    return redirect(url_for('admin'))

# Alterar status das contas (admin)
@app.route('/update_account/<int:account_id>', methods=['POST'])
def update_account(account_id):
    accounts = load_json('accounts.json')
    account = accounts[account_id]
    account['status'] = request.form['status']
    save_json('accounts.json', accounts)
    return redirect(url_for('admin'))

# Deslogar
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
