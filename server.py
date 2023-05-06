from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)
import csv


# Ara aprendrem a fer tota l'associació de diferents pàgines a HTML d'una forma eficient i sense haver d'afegir cada cop una funció per cada pàgina.

@app.route('/')
def my_home():
    return render_template('index.html')


@app.route(
    '/<string:page_name>')  # Fent això enlloc d'haver de copiar tants fx per pàgines que tinguem agafarà el page_name i el mostrarà!
def html_page(page_name):
    return render_template(page_name)


# Ara crearem una altra ruta per poder grab data de l'apartat del formulari utilitzant Py i Flask: The request Object
# Modificarem el form del contact html i posarem que la acció és submit_form i el method = 'post' perquè ens porti
# A la pàgina submit_form i posi thank you !
# Ara per això no estem rebent aquestes dades, de moment li donem feedback al que les envia, ara aprendrem a rebre-les nosaltres.
# Primer posarem attribute name = 'subject' i message i email per poder fer grab d'aquestes dades al nostre server.
# Ara podem accedir a aquestes dades amb el Flask attribute request.

# Ara farem que les dades que estem generant es guardin en un fitxer nou database.txt
def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\n{email},{subject},{message}')


# Però és més útil utilitzar excel o CSV per poder accedir a les dades:
# utilitzarem un mòdul de py csv modul i refarem la funció anterior:

def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database2:  # newline per tenir headers al CSV i que cada entrada de data sigui una nova línia.
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])


# Afegirem un Try and except block per tenir present els errors i poder corregir-los:

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()  # Aquí diem que la request la transformi en diccionari.
            write_to_file(data)
            write_to_csv(data)
            return redirect(
                '/thankyou.html')  # Amb aquest method el que fem és redireccionar-los a la pagina thank you!
        except:
            return 'Information not saved in our database!'
    else:
        return 'Something went wrong, try again!'
'''
Les bases de dades són conjunts de dades diferents emagatzemades i hi ha les DBMS : Data base management system que són colecions de programes
que ens permetes accedir a les bases de dades i treballar amb dades i controlar l'accés a les dades.
Hi ha bases de dades relacionals i noSQL: Les relacionals són les més populars (Mongo DB, Postgree, SQLServer, HIVE..)
Segueixen el mateix format que vol dir que tenen 2 o més taules amb files i columnes on les files representen entrades de dades i
les columnes representen tipus de dades diferents i la relació entre files i columnes és l'esquema que en una base de dades relacionals
s'ha de definir prèviament a l'entrada de les dades.
Hi haurà valors que es repetiran en les diferents taules (foreign key) i que ens permetran entrenllaçar una taula amb una altrei per tant relacionar-les.
Totes les BDD relacionals utilitzen SQL que és el protocol de comunicació entre el servidor i la base de dades!

Les bases de dades no relacionals o NoSQL com Cassandra, CouchDB, mongoDB, hbase, etc. et permeten poder crear una app sense haver de definir
l'esquema previ de les dades. Així com en les relacionals havies de definir l'esquema de les dades amb les no relacionals, NO!
Això fa que puguin ser molt diferents les unes de les altres a diferència de les bases de dades relacionals que normalment segueixen un mateix esquema.
Però en canvi serveixen en ocasions on hi ha una quantitat enorme de dades no estructurades i és més com una estructura de carpetes que 
poden emmagatzemar dades semblants però amb info en qualsevol tipus d'arxiu.

Mongo DB és document orientated i guarda la info com a documents. PEr fer-nos una idea podem pensar en les bases de ddes relacionals com:
Una carpeta que conté 1 fitxer users, 1 fitxer tweets, 1 fitxer following..
En canvi una No SQL com MongoDB faria un fitxer per user1, un altre fitxer per user2 i dins de cada fitxer tota la info relacionada.
Si volguessim extreure average de followers per exemple és molt més ràpida una SQL on tenim directament el fitxer de followers perquè
NOSQL hauríem d'accedir a cadascun dels users per extreure els followers.

Mongo DB té el seu propi Query lenguage però fa el mateix que faria el SQL.
Ara el que farem serà crear la nostra pròpia base de dades a fora perquè no sigui localhost sinó que estigui fora. 
Utilitzarem python anyware que ens permetrà fer un post dels nostres arxius que tenim en local gratix.
I github. Crearem un projecte al github i posarem al terminal git clone i l'adreça: git clone https://github.com/markuzkuz/portfo.git
Fent això hem creat la carpeta portfo dins el nostre Portfolio i ara hem de copiar als arxius de la nostre web


'''






'''

Aquesta seria la forma poc eficient de fer la pàgina web:

@app.route('/index.html') #Aquesta és la main page que associem a index.html
def my_home():
    return render_template('index.html') #podem relacionar el servidor amb el nostre fitxer html així on ./ és current directory nom fitxer si està a la mateixa carpeta només nom del fitxer.

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/about.html') #Aquí estem creant la pàgina about dins del nostre server que s'executa posant url/about o clicant al botó
def about():
    return render_template('about.html')

@app.route('/works.html')
def work():
    return render_template('works.html')

'''
