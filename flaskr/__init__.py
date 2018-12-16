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

        if g.found:
            g.found = False
            return render_template("finish.html", msg="done")
        form = Registration()
        if form.validate_on_submit():
            print(form.name.data)
            print(form.surname.data)
            print(form.passport.data)
            if hasattr(g, 'dbw'):
                desk = RegistrationDesk(100500, g.dbw)
                desk.dbw.connect()
                person = desk.find_by_passport(form.passport.data)
                print('query DB')
                if person is not None and len(person) != 0:
                    pg = Passenger(*list(person[0]))
                    form.name.data = pg.name
                    form.surname.data = pg.surname
                    print("RET 1")
                    g.found = True
                    g.uid = pg.passport
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
        print("CALLED FINISH")
        form = Registration()
        if form.validate_on_submit():
            print(form.name.data)
            print(form.surname.data)
            print(form.passport.data)
        msg = "Moving Forward..."
        return render_template('finish.html', msg=msg)

    from . import db
    db.init_app(app)
    ctx = app.app_context()
    ctx.g.dbw = db.get_db()
    ctx.g.found = False
    ctx.g.uid = -1
    ctx.g.ls = ["CZ5900", "AR2321", "VS2544"]
    ctx.push()

    return app
