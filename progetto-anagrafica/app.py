from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'chiave-super-segreta'

# Funzione iniziale per creare tabella
def crea_tabella():
    conn = sqlite3.connect('dati.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS anagrafica (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nome TEXT,
                 cognome TEXT,
                 email TEXT,
                 professione TEXT,
                 anni_servizio INTEGER)''')
    conn.commit()
    conn.close()

crea_tabella()

# ======== LOGIN ==========

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Login statico per esempio
        if username == 'admin' and password == '1234':
            session['utente'] = username
            return redirect('/dashboard')
        else:
            return "Login fallito"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('utente', None)
    return redirect('/login')

# ======== FORM + INSERIMENTO DATI ==========

@app.route('/')
@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    nome = request.form['nome']
    cognome = request.form['cognome']
    email = request.form['email']
    professione = request.form['professione']
    anni_servizio = request.form['anni_servizio']

    conn = sqlite3.connect('dati.db')
    c = conn.cursor()
    c.execute("INSERT INTO anagrafica (nome, cognome, email, professione, anni_servizio) VALUES (?, ?, ?, ?, ?)",
              (nome, cognome, email, professione, anni_servizio))
    conn.commit()
    conn.close()

    return render_template('conferma.html', nome=nome, cognome=cognome)

# ======== DASHBOARD ==========

@app.route('/dashboard')
def dashboard():
    if 'utente' not in session:
        return redirect('/login')
    conn = sqlite3.connect('dati.db')
    c = conn.cursor()
    c.execute("SELECT * FROM anagrafica")
    dati = c.fetchall()
    conn.close()
    return render_template('dashboard.html', dati=dati)

# ======== MODIFICA ==========

@app.route('/modifica/<int:id>', methods=['GET', 'POST'])
def modifica(id):
    if 'utente' not in session:
        return redirect('/login')

    conn = sqlite3.connect('dati.db')
    c = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        cognome = request.form['cognome']
        email = request.form['email']
        professione = request.form['professione']
        anni_servizio = request.form['anni_servizio']
        c.execute('''UPDATE anagrafica SET nome=?, cognome=?, email=?, professione=?, anni_servizio=? WHERE id=?''',
                  (nome, cognome, email, professione, anni_servizio, id))
        conn.commit()
        conn.close()
        return redirect('/dashboard')

    c.execute("SELECT * FROM anagrafica WHERE id=?", (id,))
    record = c.fetchone()
    conn.close()
    return render_template('modifica.html', record=record)

# ======== ELIMINA ==========

@app.route('/elimina/<int:id>')
def elimina(id):
    if 'utente' not in session:
        return redirect('/login')
    conn = sqlite3.connect('dati.db')
    c = conn.cursor()
    c.execute("DELETE FROM anagrafica WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/dashboard')


# ======== AVVIO SERVER ==========

if __name__ == '__main__':
    app.run(debug=True)