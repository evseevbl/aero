import psycopg2

class GroundService(object):
    def __init__(self, code, dbw):
        self.code = code
        self.dbw = dbw
        self.dbw.connect()
        pass

    def __del__(self):
        self.dbw.disconnect()
        print (self.id, 'connection closed')


class Passenger(object):
    def __init__(self, dbid, name, surname, country, passport):
        self.dbid = dbid
        self.name = name
        self.surname = surname
        self.country = country
        self.passport = passport


class RegistrarionDesk(GroundService):
    def register_passenger(self, passenger, flight):
        self.dbw.query("INSERT .....")


class DBWrapper(object):
    def __init__(self, dbname='aero', user='zevs', password='zevs', host='localhost'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        print('init db with id =', id(self))


    def connect(self):
        self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host)
        self.cur = self.conn.cursor()


    def disconnect(self):
        self.cur.close()
        self.conn.close()


    def query(self, query, args):
        self.connect()
        self.cur.execute(query, args)
        ret = cur.fetchall()
        self.conn.commit()
        self.disconnect()
        return ret


    def query_list(self, ls):
        self.connect()
        for elem in ls:
            self.cur.execute(elem[0], elem[1])
        self.conn.commit()
        self.disconnect()


def main():
    conn = psycopg2.connect(dbname='aero', user='zevs', password='zevs', host='localhost')
    cur = conn.cursor()
    cur.execute('SELECT * FROM daeroports;')
    x = cur.fetchall()
    print(x)
    conn.commit()
    cur.close()
    conn.close()
