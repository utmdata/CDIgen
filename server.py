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
