import os

from flask import Flask, render_template, g, session, current_app
from .forms import Registration
from .conn import DBWrapper, RegistrationDesk, GroundService
from .types import Passenger


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    app.config.update(
        TESTING=True,
        SECRET_KEY='dev'
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/register", methods=['GET', 'POST'])
    def registration():
        form = Registration()
        if form.validate_on_submit():
            print(form.name.data)
            print(form.surname.data)
            print(form.passport.data)
            print('g=', type(g))
            if hasattr(g, 'dbw'):
                desk = RegistrationDesk(100500, g.dbw)
                desk.dbw.connect()
                person = desk.find_by_passport(form.passport.data)
                if person is not None:
                    pg = Passenger(*list(person[0]))
                    form.name.data = pg.name
                    form.surname.data = pg.surname

            else:
                print("No DB connection")
        return render_template("registration.html", form=form)

    print("gonna init APP")
    from . import db
    db.init_app(app)
    ctx = app.app_context()
    ctx.g.dbw = db.get_db()
    ctx.push()
    return app
