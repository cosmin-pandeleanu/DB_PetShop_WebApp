from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import sys

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'TemaBD0.'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()

#Variabile Globale
_nr_card = 0
_id_cat = 0

@app.route('/')
###------------------------------------------ VIZUALIZARE CLIENTI ---------------------------------------------------###
@app.route('/clienti')
def clienti():
    clienti_ = []
    cursor = conn.cursor()
    cursor.execute('SELECT clienti.nr_card , nume_client , email, data_nasterii, gen, oras, adresa '
                'FROM clienti, detalii_clienti '
                'WHERE clienti.nr_card = detalii_clienti.nr_card '
                'ORDER BY clienti.nr_card')
    for result in cursor:
        client = {'nr_card': result[0], 'nume_client': result[1], 'email': result[2],
                  'gen': result[4], 'oras': result[5], 'adresa': result[6]}
        if str(result[3]) != 'None':
            client['data_nasterii'] = datetime.strptime(str(result[3]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y')
        else:
            client['data_nasterii'] = result[3]
        clienti_.append(client)
    cursor.close()
    return render_template('Clienti/clienti.html', clienti=clienti_)

###--------------------------------------------- ADAUGARE CLIENTI ---------------------------------------------------###
@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    error = " "
    try:
        if request.method == 'POST':
            cursor = conn.cursor()
            values = []
            values.append("'" + request.form['nume_client'] + "'")
            fields = ['nume_client']
            query = 'INSERT INTO %s (%s) VALUES (%s)' % ('clienti', ', '.join(fields), ', '.join(values))
            cursor.execute(query)
            values = []
            cursor.execute('SELECT max(nr_card) FROM clienti')
            last_nr_card = cursor.fetchone()
            values.append(str(last_nr_card)[1:-2])
            values.append("'" + request.form['email'] + "'")
            if request.form['data_nasterii'] != "":
                values.append("STR_TO_DATE('" + request.form['data_nasterii'] + "', '%d.%m.%Y')")
            else:
                values.append("null")
            values.append("'" + request.form['gen'] + "'")
            values.append("'" + request.form['oras'] + "'")
            values.append("'" + request.form['adresa'] + "'")
            fields = ["nr_card", 'email', 'data_nasterii', 'gen', 'oras', 'adresa']
            query = 'INSERT INTO %s (%s) VALUES (%s)' % ('detalii_clienti', ', '.join(fields), ', '.join(values))
            cursor.execute(query)
            cursor.execute('commit')
            cursor.close()
            return redirect('/clienti')
    except Exception as err:
        print("Something went wrong: {}".format(err), file=sys.stderr)
        error = err
    finally:
        return render_template('Clienti/add_client.html', error=error)

###-------------------------------------------- STERGERE CLIENTI ----------------------------------------------------###
@app.route('/delete_client', methods=['POST'])
def delete_client():
    try:
        client = request.form['nr_card']
        cursor  = conn.cursor()
        cursor.execute('DELETE FROM detalii_clienti WHERE nr_card = ' + client)
        cursor.execute('commit')
        cursor.execute('DELETE FROM clienti WHERE nr_card = ' + client)
        cursor.execute('commit')
        cursor.close()
        return redirect('/clienti')
    except Exception as err:
        print("Something went wrong: {}".format(err), file=sys.stderr)
        return render_template('Clienti/clienti.html', error=err)


###-------------------------------------------- EDITEAZA CLIENTI ----------------------------------------------------###
@app.route('/edit_client', methods=['GET', 'POST'])
def edit_client():
    try:
        if request.method == 'POST':
            ## update into clienti
            cursor = conn.cursor()
            values = []
            values.append("'" + request.form['nume_client'] + "'")
            fields = ['nume_client']
            query = 'UPDATE clienti SET %s=%s WHERE nr_card = %s' % (fields[0], values[0], _nr_card)
            cursor.execute(query)
            ## update into detalii_clienti
            values = []
            values.append("'" + request.form['email'] + "'")
            if request.form['data_nasterii'] not in ["", "None"] :
                values.append("STR_TO_DATE('" + request.form['data_nasterii'] + "', '%d.%m.%Y')")
            else:
                values.append("null")
            values.append("'" + request.form['gen'] + "'")
            values.append("'" + request.form['oras'] + "'")
            values.append("'" + request.form['adresa'] + "'")
            fields = ['email', 'data_nasterii', 'gen', 'oras', 'adresa']
            query = "UPDATE detalii_clienti SET %s=%s, %s=%s, %s=%s, %s=%s, %s=%s WHERE nr_card = %s" %(
                fields[0], values[0], fields[1], values[1],fields[2], values[2], fields[3],values[3], fields[4], values[4], str(_nr_card))
            print(query, file=sys.stderr)
            cursor.execute(query)
            cursor.execute('commit')
            cursor.close()
        return redirect('/clienti')
    except Exception as err:
        print("Something went wrong: {}".format(err), file=sys.stderr)
        return render_template('Clienti/clienti.html', error=err)

###-------------------------------------- PRELUARE INFORMATII CLIENTI -----------------------------------------------###
@app.route('/get_client', methods=['POST'])
def get_client():
    nr_card = request.form['nr_card']
    global _nr_card
    _nr_card = nr_card
    cursor = conn.cursor()
    cursor.execute('SELECT nume_client, email, data_nasterii, gen, oras, adresa '
                   'FROM clienti, detalii_clienti '
                   'WHERE clienti.nr_card = detalii_clienti.nr_card AND clienti.nr_card = %s '
                   'ORDER BY clienti.nr_card' %(nr_card) )
    result = cursor.fetchone()
    client = {'nume_client': result[0], 'email': result[1],
              'gen': result[3], 'oras': result[4], 'adresa': result[5]}
    if str(result[2]) != 'None':
        client['data_nasterii'] = datetime.strptime(str(result[2]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y')
    else:
        client['data_nasterii'] = result[2]
    cursor.close()
    return render_template('Clienti/edit_client.html', client=client)

###--------------------------------------------------- PRODUSE ------------------------------------------------------###
@app.route('/produse')
def produse():
    produse_ = []
    cursor = conn.cursor()
    cursor.execute(
        'SELECT p.id_produs, denumire_produs, stoc , pret, um, tp.denumire_tip, f.denumire_furnizor, ca.denumire_categorie '
        'FROM produse as p, tipuri_produse as tp, furnizori as f, categorii_animale as ca '
        'WHERE p.id_tip = tp.id_tip AND p.id_furnizor = f.id_furnizor AND p.id_categorie = ca.id_categorie '
        'ORDER BY p.id_produs')
    for result in cursor:
        produs = {'id_produs': result[0], 'denumire_produs': result[1], 'stoc': result[2], 'pret': result[3],
                  'um': result[4], 'tip': result[5], 'furnizor': result[6], 'categorie': result[7]}
        produse_.append(produs)
    cursor.close()
    return render_template('Produse/produse.html', produse=produse_)

###----------------------------------------------- ADAUGARE PRODUSE -------------------------------------------------###
@app.route('/add_produs', methods=['GET', 'POST'])
def add_produs():
    try:
        furnizori = []
        cursor = conn.cursor()
        cursor.execute('SELECT id_furnizor, denumire_furnizor FROM furnizori ORDER BY id_furnizor')
        for result in cursor:
            furnizor = {'id_furnizor': result[0], 'denumire_furnizor': result[1]}
            furnizori.append(furnizor)
        cursor.close()

        categorii_animale = []
        cursor = conn.cursor()
        cursor.execute('SELECT id_categorie, denumire_categorie FROM categorii_animale ORDER BY id_categorie')
        for result in cursor:
            categorie = {'id_categorie': result[0], 'denumire_categorie':result[1]}
            categorii_animale.append(categorie)
        cursor.close()

        tipuri_produse = []
        cursor = conn.cursor()
        cursor.execute('SELECT id_tip, denumire_tip FROM tipuri_produse ORDER BY id_tip')
        for result in cursor:
            tip = {'id_tip': result[0], 'denumire_tip': result[1]}
            tipuri_produse.append(tip)
        cursor.close()

        if request.method == 'POST':
            cursor = conn.cursor()
            values = []
            values.append("'" + request.form['denumire_produs'] + "'")
            values.append("'" + request.form['stoc'] + "'")
            values.append("'" + request.form['pret'] + "'")
            values.append("'" + request.form['um'] + "'")
            values.append("'" + request.form['id_furnizor'] + "'")
            values.append("'" + request.form['id_categorie'] + "'")
            values.append("'" + request.form['id_tip'] + "'")
            fields = ['denumire_produs', 'stoc', 'pret','um', 'id_furnizor', 'id_categorie', 'id_tip']
            query = 'INSERT INTO %s (%s) VALUES (%s)' % ('produse', ', '.join(fields), ', '.join(values))
            cursor.execute(query)
            cursor.execute('commit')
            cursor.close()
            return redirect('/produse')
    except Exception as err:
        print("Something went wrong: {}".format(err), file=sys.stderr)
        return render_template('Produse/produse.html', error=err)
    return render_template('Produse/add_produs.html', furnizori=furnizori, categorii_animale=categorii_animale, tipuri_produse=tipuri_produse)


###--------------------------------------------------- VANZARI ------------------------------------------------------###
@app.route('/vanzari')
def vanzari():
    vanzari_ = []
    cur = conn.cursor()
    cur.execute('SELECT nr_bon, data_achizitiei, nr_card, p.id_produs, p.denumire_produs,p.um, cantitate, pret '
                'FROM vanzari as v, produse as p '
                'WHERE v.id_produs = p.id_produs '
                'ORDER BY nr_bon DESC')
    for result in cur:
        vanzare = {'nr_bon': result[0], 'nr_card': result[2], 'id_produs': result[3], 'denumire_produs': result[4],
                   'um': result[5], 'cantitate': result[6], 'pret': result[7],
                   'data_achizitiei': datetime.strptime(str(result[1]), '%Y-%m-%d %H:%M:%S').strftime(
                       '%d.%m.%Y %H:%M:%S')}
        vanzari_.append(vanzare)
    cur.close()
    return render_template('Vanzari/vanzari.html', vanzari=vanzari_)

###----------------------------------------------- ADAUGARE VANZARI -------------------------------------------------###
@app.route('/add_vanzare', methods=['GET', 'POST'])
def add_vanzare():
    try:
        produse_ = []
        cursor = conn.cursor()
        cursor.execute('SELECT id_produs, denumire_produs FROM produse ORDER BY id_produs')
        for result in cursor:
            produs = {'id_produs': result[0], 'denumire_produs': result[1]}
            produse_.append(produs)
        cursor.close()

        if request.method == 'POST':
            values = []
            cursor = conn.cursor()
            values.append("'" + request.form['nr_card'] + "'")
            values.append("'" + request.form['id_produs'] + "'")
            values.append("'" + request.form['cantitate'] + "'")
            values.append("SYSDATE()")
            fields = ['nr_card', 'id_produs', 'cantitate', 'data_achizitiei']
            query = 'INSERT INTO %s (%s) VALUES (%s)' % ('vanzari', ', '.join(fields), ', '.join(values))
            cursor.execute(query)
            query = 'UPDATE produse SET stoc = stoc-%s WHERE id_produs = %s' % (request.form['cantitate'], request.form['id_produs'])
            cursor.execute(query)
            cursor.execute('commit')
            cursor.close()
            return redirect('/vanzari')
    except Exception as err:
        print("Something went wrong: {}".format(err), file=sys.stderr)
        return render_template('Vanzari/add_vanzare.html', produse=produse_, error=err)
    return render_template('Vanzari/add_vanzare.html', produse=produse_)

###-------------------------------------------------- FURNIZORI -----------------------------------------------------###
@app.route('/furnizori')
def furnizori():
    furnizori_ = []
    cur = conn.cursor()
    cur.execute('SELECT * FROM furnizori ORDER BY id_furnizor')
    for result in cur:
        furnizor = {'id_furnizor': result[0], 'denumire_furnizor': result[1]}
        furnizori_.append(furnizor)
    cur.close()
    return render_template('furnizori.html', furnizori=furnizori_)

###------------------------------------------------ TIPURI PRODUSE --------------------------------------------------###
@app.route('/tipuri_produse')
def tipuri_produse():
    tipuri = []
    cur = conn.cursor()
    cur.execute('SELECT * FROM tipuri_produse ORDER BY id_tip')
    for result in cur:
        tip = {'id_tip': result[0], 'denumire_tip': result[1]}
        tipuri.append(tip)
    cur.close()
    return render_template('tipuri_produse.html', tipuri_produse=tipuri)

###--------------------------------------- VIZUALIZARE CATEGORII ANIMALE --------------------------------------------###
@app.route('/categorii_animale')
def categorii_animale():
    categorii = []
    cur = conn.cursor()
    cur.execute('SELECT * FROM categorii_animale ORDER BY id_categorie')
    for result in cur:
        categorie = {'id_categorie': result[0], 'denumire_categorie': result[1]}
        categorii.append(categorie)
    cur.close()
    return render_template('Categorii_animale/categorii_animale.html', categorii=categorii)

###-------------------------------------- PRELUARE INFORMATII CATEGORIE ---------------------------------------------###
@app.route('/get_categorie', methods=['POST'])
def get_categorie():
    id_categorie = request.form['id_categorie']
    global _id_cat
    _id_cat = id_categorie
    cursor = conn.cursor()
    cursor.execute('SELECT denumire_categorie '
                   'FROM categorii_animale '
                   'WHERE  id_categorie = %s ' %(id_categorie) )
    result = cursor.fetchone()
    cursor.close()
    return render_template('Categorii_animale/edit_categorii_animale.html', denumire_categorie=result[0])

###--------------------------------------------- EDITEAZA CATEGORIE -------------------------------------------------###
@app.route('/edit_categorie', methods=['POST'])
def edit_categorie():
    if request.method == 'POST':
        cursor = conn.cursor()
        id_categorie = _id_cat
        values = []
        values.append("'" + request.form['denumire_categorie'] + "'")
        fields = ['denumire_categorie']
        query = 'UPDATE categorii_animale SET %s = %s WHERE id_categorie = %s' % (fields[0], values[0], id_categorie)
        cursor.execute(query)
        cursor.execute('commit')
        cursor.close()
    return redirect('/categorii_animale')

if __name__ == '__main__':
    app.run(debug=True)
