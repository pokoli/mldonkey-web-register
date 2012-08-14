#/usr/bin/python
# encoding: utf-8
from os import urandom
from flask import Flask,render_template,request,redirect,url_for,flash,get_flashed_messages
from flask.ext.shelve import get_shelve,init_app
from pwgen import pwgen
from validate_email import validate_email

import mldonkey 
import hashlib

def md5(string):
    """
        Utilitat per calcular el md5 de una cadena
    """
    m = hashlib.md5()
    m.update(string)
    return m.digest()


app = Flask(__name__)
#Use pyjade extension for rendering jade templates.
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

@app.route("/")
def start():
    return render_template("index.jade",
            success=get_flashed_messages(category_filter=["success"]),
            errors=get_flashed_messages(category_filter=["error"]))

@app.route("/new_user")
def new_user():
    return render_template("new_user.jade",
            success=get_flashed_messages(category_filter=["success"]),
            errors=get_flashed_messages(category_filter=["error"]))

@app.route("/lost_password")
def lost_pass():
    return render_template("lost_password.jade",
            success=get_flashed_messages(category_filter=["success"]),
            errors=get_flashed_messages(category_filter=["error"]))

@app.route("/change_password")
def change_pass():
    return render_template("change_password.jade",
            success=get_flashed_messages(category_filter=["success"]),
            errors=get_flashed_messages(category_filter=["error"]))

def validate_new_form(request):
    invalid = False 
    if not request.form['username']: 
        flash('Es obligatori indicar un usuari','error')
        invalid = True 
    if not request.form['email']: 
        flash(u'Es obligatori indicar un correu electrònic','error')    
        invalid = True 
    if request.form['email'] != request.form['email2']: 
        flash(u'Les direccions de correu electrònic no conicideixen','error')    
        invalid = True 
    if not validate_email(request.form['email']):
        flash(u'Direcció de correo electrònic invàlida','error')
        invalid = True

    return invalid

@app.route("/new/",methods=["POST"])
def new():
    db = get_shelve()
    invalid = validate_new_form(request)
    email = str(request.form['email'])
    username = str(request.form['username'])
    if(not invalid and db.has_key(email)):
        flash(u'La direcció de correu ja existeix.','error')
        invalid = True
    if not invalid and username in [ x['username'] for x in db.values()]:     
        flash(u'El nom d\'usuari ja existeix.','error')
        invalid = True
    if invalid: 
        return redirect(url_for("new_user"))
    pwd = str(pwgen(10, no_symbols=True))
    print pwd
    #TODO: Provar la connexió amb MLDonkey
    #with mldonkey.MLDonkey() as ml:
    #    ml.new_user(request.form['username'],request.form['email'],pwd)
    #Afegir el usuari a la BD (fitxer)
    db[email] = {
        'username' : username,
        'password' : md5(pwd),
    } 
    #TODO: Enviar un email al usuari
    flash(u'Les dades d\'accès s\'han enviat al vostre correu electrònic.','success')
    return redirect(url_for("new_user"))

@app.route("/lost/",methods=["POST"])
def lost():
    db = get_shelve()
    email = str(request.form['email'])
    if not db.has_key(email):
        flash(u'La direcció de correu no existeix al sistema.','error')
        return redirect(url_for("lost_pass"))
    username = db[email]['username']
    pwd = pwgen(10, no_symbols=True)
    print pwd
    #TODO: Provar la connexió amb MLDonkey
    #with mldonkey.MLDonkey() as ml:
    #    ml.change_pass(username,pwd)
    user_data = db[email]
    user_data['password'] = md5(pwd)
    db[email] = user_data
    #TODO: Enviar un email al usuari
    flash(u'Les dades d\'accès s\'han enviat al vostre correu electrònic.','success')
    return redirect(url_for("lost_pass"))

@app.route("/change/",methods=["POST"])
def change():
    db = get_shelve()
    email = str(request.form['email'])
    if not db.has_key(email):
        flash(u'La direcció de correu no existeix al sistema.','error')
        return redirect(url_for("change_pass"))
    if request.form['password'] != request.form['password2']: 
        flash(u'Les contrasenyes no conicideixen.','error')    
        return redirect(url_for("change_pass"))
    old_password = db[email]['password']
    if md5(str(request.form['old_password'])) != old_password:
        flash(u'Contrasenya anterior incorrecta.','error')    
        return redirect(url_for("change_pass"))
    username = db[email]['username']
    pwd = str(request.form['password'])
    #TODO: Provar la connexió amb MLDonkey
    #with mldonkey.MLDonkey() as ml:
    #    ml.change_pass(username,pwd)
    user_data = db[email]
    user_data['password'] = md5(pwd)
    db[email] = user_data
    print pwd
    flash(u'La vostra contrasenya s\'ha actualitzat correctament','success')
    return redirect(url_for("change_pass"))

#Remove this on production server:
app.debug=True

app.secret_key = urandom(24)
app.config['SHELVE_FILENAME'] = 'users.db'
init_app(app)
if __name__ == "__main__":
    app.run(host='0.0.0.0')
