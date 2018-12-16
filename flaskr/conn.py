import psycopg2


class GroundService(object):
    def __init__(self, code, dbw):
        self.code = code
        self.dbw = dbw
        pass

    def __del__(self):
        print(self.code, ' gonna close conn')
        self.dbw.disconnect()


class RegistrationDesk(GroundService):
    def __init__(self, code, dbw):
        super().__init__(code, dbw)

    def register_passenger(self, passenger, flight):
        self.dbw.query("INSERT .....")

    def find_by_passport(self, passport):
        passport = str(passport)
        ret = self.dbw.query("SELECT * FROM dpassengers WHERE passport_id = %s", (passport,))
        return ret


class DBWrapper(object):
    def __init__(self, dbname='aero', user='zevs', password='zevs', host='localhost', port='5432'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cur = None
        print('init db with id =', id(self))

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port)
        self.cur = self.conn.cursor()

    def disconnect(self):
        if hasattr(self, 'cur'):
            self.cur.close()
        if hasattr(self, 'conn'):
            self.conn.close()

    def query(self, query, args):
        self.cur.execute(query, args)
        ret = self.cur.fetchall()
        self.conn.commit()
        return ret

    def query_list(self, ls):
        for elem in ls:
            self.cur.execute(elem[0], elem[1])
        self.conn.commit()


def main():
    conn = psycopg2.connect(dbname='aero', user='zevs', password='zevs', host='localhost')
    cur = conn.cursor()
    cur.execute('SELECT * FROM daeroports;')
    x = cur.fetchall()
    print(x)
    conn.commit()
    cur.close()
    conn.close()
