class Passenger(object):
    def __init__(self, passport, name, surname, bdate):
        self.passport = passport
        self.name = name
        self.surname = surname
        self.bdate = bdate

    def __str__(self):
        return "Name:\t" + self.name + \
               "\nSurname:\t" + self.surname + \
               "\nPassport:\t" + self.passport + \
               "\nBirth:\t" + str(self.bdate)
