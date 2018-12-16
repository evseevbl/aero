import os

from flask import Flask, render_template, g
from .forms import Registration

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route("/register", methods=['GET', 'POST'])
    def registration():
        form = Registration()
        if form.validate_on_submit():
            print(form.name.data)
            print(form.surname.data)
            print(form.Passport.data)
        return render_template('registration.html', form=form)

    return app