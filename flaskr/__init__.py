import os

from flask import Flask, render_template, g, session, current_app, request
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
        print("CALLED REGISTER")
        form = Registration()
        print(form.name.data)
        print(form.surname.data)
        print(form.passport.data)
        print(form.flight.data)
        if g.first:
            g.first = False
            return render_template("search.html", form=form, msg="provide passport number and hit Search", found=False)

        if not hasattr(g, 'found'):
            return render_template("search.html", form=form, msg="provide passport number and hit Search", found=False)
        if g.found:
            print("INSERT USER")
            g.found = False
            ret = g.desk.register_passenger(g.uid, form.flight.data)
            print('retval=', ret)
            return render_template("finish.html", msg="done")
        else:
            print("FOUND")
        if hasattr(g, 'dbw'):
            person = g.desk.find_by_passport(form.passport.data)
            print('query DB')
            if person is not None and len(person) != 0:
                pg = Passenger(*list(person[0]))
                form.name.data = pg.name
                form.surname.data = pg.surname
                print("RET 1")
                g.found = True
                g.uid = pg.passport
                form.flight.choices = g.flights
                return render_template("register.html", form=form, msg="", found=True)
            else:
                form.name.data = ""
                form.surname.data = ""
                print("RET 2")
                return render_template("search.html", form=form, msg="", found=False)
        else:
            print("No DB connection")
        return render_template("search.html", form=form, msg="", found=False)

    @app.route("/finish", methods=['GET', 'POST'])
    def finish():
        g.first = True
        print("CALLED FINISH")
        form = Registration()
        if form.validate_on_submit():
            print(form.name.data)
            print(form.surname.data)
            print(form.passport.data)
        msg = "passenger registration finished..."
        return render_template('finish.html', msg=msg)

    from . import db
    db.init_app(app)
    ctx = app.app_context()
    ctx.g.dbw = db.get_db()
    ctx.g.desk = RegistrationDesk(15, ctx.g.dbw)
    ctx.g.desk.dbw.connect()
    ctx.g.found = False
    ctx.g.uid = -1
    ctx.g.first = True
    ctx.g.flights = []
    for f in ["1052", "1053", "1059", "1056"]:
        ctx.g.flights.append((f, f))
    ctx.push()

    return app
