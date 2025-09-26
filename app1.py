#uvoz potrebnih biblioteka
from datetime import datetime
from flask import Flask, flash, render_template, url_for, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector


def get_db_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='root',
        database='evidencija_zaposlenih_u_firmi'
    )
app = Flask(__name__)
app.secret_key = 'sifra123'


conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='evidencija_zaposlenih_u_firmi'
)
cursor = conn.cursor()
# Hešuj lozinku "lazar"
nova_lozinka = generate_password_hash("lazar")
# Ažuriraj samo korisnika sa ID 8
cursor.execute("""
    UPDATE korisnici
    SET lozinka = %s
    WHERE korisnik_id = %s
""", (nova_lozinka, 8))
conn.commit()
cursor.close()
conn.close()
print("✔ Lozinka za korisnika 'lazar' uspešno hešovana.")


@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        korisnicko_ime = request.form['username']
        lozinka = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM korisnici WHERE korisnicko_ime = %s", (korisnicko_ime,))
        korisnik = cursor.fetchone()
        cursor.close()
        conn.close()

        if korisnik and check_password_hash(korisnik['lozinka'], lozinka):
            session['uloga'] = korisnik['uloga']
            session['id'] = korisnik['korisnik_id']
            if korisnik['uloga'] == 'HR':
                return redirect('/hr')
            else:
                return redirect(f'/zaposleni/{korisnik["korisnik_id"]}')
        else:
            return render_template('login.html', poruka='Neispravni podaci')

    return render_template('login.html')

# ---------------- HR DASHBOARD ----------------
@app.route('/hr')
def hr_panel():
    if session.get('uloga') != 'HR':
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT z.zaposleni_id, z.ime, z.prezime, z.pozicija, z.email, z.datum_zaposlenja,
           k.korisnicko_ime, k.uloga
        FROM zaposleni z
        JOIN korisnici k ON z.korisnik_id = k.korisnik_id
        ORDER BY z.prezime ASC
    """)

    zaposleni = cursor.fetchall()
    cursor.close()
    conn.close()

 
    return render_template('hr_dashboard.html', zaposleni=zaposleni)

# ---------------- BRISANJE ZAPOSLENI ----------------
@app.route('/obrisi-zaposlenog/<int:zaposleni_id>', methods=['POST'])
def obrisi_zaposlenog(zaposleni_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM zaposleni WHERE zaposleni_id = %s", (zaposleni_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Zaposleni obrisan.", "warning")
    return redirect('/hr')

# ---------------- IZMENA ZAPOSLENI ----------------
@app.route('/izmena-zaposleni/<int:zaposleni_id>', methods=['GET', 'POST'])
def izmena_zaposleni(zaposleni_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        ime = request.form['ime']
        prezime = request.form['prezime']
        pozicija = request.form['pozicija']
        email = request.form['email']

        cursor.execute("""
            UPDATE zaposleni
            SET ime = %s, prezime = %s, pozicija = %s, email = %s
            WHERE zaposleni_id = %s
        """, (ime, prezime, pozicija, email, zaposleni_id))

        conn.commit()
        cursor.close()
        conn.close()
        flash("Podaci su uspešno izmenjeni!", "success")
        return redirect('/hr')

    cursor.execute("SELECT * FROM zaposleni WHERE zaposleni_id = %s", (zaposleni_id,))
    zaposleni = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('izmena_zaposleni.html', zaposleni=zaposleni)

# ---------------- NOVI ZAPOSLENI ----------------
@app.route('/novi-zaposleni', methods=['GET', 'POST'])
def novi_zaposleni():
    if session.get('uloga') != 'HR':
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        ime = request.form['ime']
        prezime = request.form['prezime']
        pozicija = request.form['pozicija']
        email = request.form['email']
        korisnicko_ime = request.form['korisnicko_ime']
        lozinka = generate_password_hash(request.form['lozinka'])
        uloga = request.form['uloga']

        # upis u korisnici
        cursor.execute("""
            INSERT INTO korisnici (korisnicko_ime, lozinka, uloga)
            VALUES (%s, %s, %s)
        """, (korisnicko_ime, lozinka, uloga))

        korisnik_id = cursor.lastrowid

        # upis u zaposleni 
        cursor.execute("""
            INSERT INTO zaposleni (korisnik_id, ime, prezime, pozicija, email, datum_zaposlenja)
            VALUES (%s, %s, %s, %s, %s, CURRENT_DATE)
        """, (korisnik_id, ime, prezime, pozicija, email))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Uspešno ste dodali novog zaposlenog!", "success")
        return redirect(url_for('novi_zaposleni'))

    return render_template('novi_zaposleni.html')


# ---------------- ODOBRI ZAHTEV ZA ODMOR ----------------
@app.route('/odobri-zahtev/<int:zahtev_id>', methods=['POST'])
def odobri_zahtev(zahtev_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE zahtevi SET status = 'Odobreno' WHERE zahtev_id = %s", (zahtev_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Zahtev je odobren.", "success")
    return redirect('/zahtevi-hr')


# ---------------- OTKAZI ZAHTEV ZA ODMOR ----------------
@app.route('/otkazi-zahtev/<int:zahtev_id>', methods=['POST'])
def otkazi_zahtev(zahtev_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE zahtevi SET status = 'Otkazano' WHERE zahtev_id = %s", (zahtev_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Zahtev je otkazan.", "warning")
    return redirect('/zahtevi-hr')


# ---------------- ZAPOSLENI DASHBOARD ----------------
@app.route('/zaposleni/<int:id>', methods=['GET', 'POST'])
def zaposleni_dashboard(id):
    # Provera pristupa
    if session.get('uloga') != 'Zaposleni' or session.get('id') != id:
        return redirect('/login')

    korisnik_id = session['id']
    conn = get_db_connection()
    today = datetime.today().date()

    # Dobavi zaposleni_id na osnovu korisnik_id
    cursor_lookup = conn.cursor(dictionary=True)
    cursor_lookup.execute("SELECT zaposleni_id FROM zaposleni WHERE korisnik_id = %s", (korisnik_id,))
    rezultat = cursor_lookup.fetchone()
    cursor_lookup.close()

    if not rezultat:
        conn.close()
        return "Greška: Zaposleni nije pronađen."

    zaposleni_id = rezultat['zaposleni_id']

    # Unos prisustva
    unet_dolazak = None
    unet_odlazak = None

    if request.method == 'POST':
        unet_dolazak = request.form.get('vreme_dolaska')
        unet_odlazak = request.form.get('vreme_odlaska')

        cursor = conn.cursor()
        if unet_dolazak and not unet_odlazak:
            cursor.execute("""
                INSERT INTO prisustvo (zaposleni_id, datum, vreme_dolaska)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE vreme_dolaska = %s
            """, (zaposleni_id, today, unet_dolazak, unet_dolazak))

        elif unet_dolazak and unet_odlazak:
            cursor.execute("""
                INSERT INTO prisustvo (zaposleni_id, datum, vreme_dolaska, vreme_odlaska)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE vreme_dolaska = %s, vreme_odlaska = %s
            """, (zaposleni_id, today, unet_dolazak, unet_odlazak, unet_dolazak, unet_odlazak))

        conn.commit()
        cursor.close()

    # Podaci o zaposlenom
    cursor1 = conn.cursor(dictionary=True)
    cursor1.execute("""
        SELECT ime, prezime, pozicija, email, datum_zaposlenja
        FROM zaposleni
        WHERE korisnik_id = %s
    """, (korisnik_id,))
    zaposleni = cursor1.fetchone()
    cursor1.close()

    # Zahtevi za odmor
    cursor2 = conn.cursor(dictionary=True)
    cursor2.execute("""
        SELECT datum_od, datum_do, razlog, status
        FROM zahtevi_za_odmor
        WHERE zaposleni_id = %s
        ORDER BY zahtev_id DESC
        LIMIT 2
    """, (zaposleni_id,))
    zahtevi = cursor2.fetchall()
    cursor2.close()

    conn.close()

    return render_template('zaposleni_dashboard.html',
                           zaposleni=zaposleni,
                           zahtevi=zahtevi,
                           today=today,
                           unet_dolazak=unet_dolazak,
                           unet_odlazak=unet_odlazak)
# ---------------- HR ZAHTEVI ----------------
@app.route('/zahtevi-hr')
def zahtevi_hr():
    if session.get('uloga') != 'HR':
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.zahtev_id, z.ime, z.prezime, z.pozicija, z.email,
            o.datum_od, o.datum_do, o.razlog, o.status
        FROM zahtevi_za_odmor o
        JOIN zaposleni z ON o.zaposleni_id = z.zaposleni_id
        ORDER BY o.datum_od DESC
    """)
    zahtevi = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('zahtevi_hr.html', zahtevi=zahtevi)

# ---------------- NOVI ZAHTEV ----------------
@app.route('/novi-zahtev', methods=['GET', 'POST'])
def novi_zahtev():
    if session.get('uloga') != 'Zaposleni':
        return redirect('/login')

    korisnik_id = session.get('id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Dobavi zaposleni_id na osnovu korisnik_id
    cursor.execute("SELECT zaposleni_id FROM zaposleni WHERE korisnik_id = %s", (korisnik_id,))
    rezultat = cursor.fetchone()

    if not rezultat:
        cursor.close()
        conn.close()
        return "Greška: Zaposleni nije pronađen u bazi."

    zaposleni_id = rezultat['zaposleni_id']

    if request.method == 'POST':
        datum_od = request.form['datum_od']
        datum_do = request.form['datum_do']
        razlog = request.form['razlog']

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO zahtevi_za_odmor (zaposleni_id, datum_od, datum_do, razlog, status)
            VALUES (%s, %s, %s, %s, 'Na čekanju')
        """, (zaposleni_id, datum_od, datum_do, razlog))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(f"/zaposleni/{korisnik_id}")

    cursor.close()
    conn.close()
    return render_template('novi_zahtev.html')


@app.route('/azuriraj-status-zahteva', methods=['POST'])
def azuriraj_status_zahteva():
    podaci = request.get_json(force=True)  # Dodaj force=True
    zahtev_id = podaci.get('zahtev_id')
    status = podaci.get('status')

    if status not in ['Odobreno', 'Otkazano']:
        return jsonify({'uspesno': False, 'poruka': 'Nevažeći status.'})

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE zahtevi_za_odmor SET status = %s WHERE zahtev_id = %s", (status, zahtev_id))
    print("UPDATE izvršen")
    conn.commit()
    cursor.close()
    conn.close()
    print("Primljen zahtev:", zahtev_id, status)

    return jsonify({'uspesno': True})

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------------- START ----------------
if __name__ == '__main__':
    app.run(debug=True)

