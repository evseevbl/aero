
app = Flask(__name__)
sdfasdf

@app.route("/register", methods=['GET', 'POST'])
def registration():
    form = Registration()
    if form.validate_on_submit():
        print(form.name.data)
        print(form.surname.data)
        print(form.Passport.data)
    return render_template('registration.html', form=form)

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'pgdb'):
        g.pgdb.disconnect()

def connect_db():
    g.pgdb.connect()

if __name__ == '__main__':
    app.run(debug=True)
