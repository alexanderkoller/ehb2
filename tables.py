# coding: utf-8
from sqlalchemy import Column, DateTime, Float, Integer, SmallInteger, String, Table, text, ForeignKey, Unicode, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


Base = declarative_base()
metadata = Base.metadata

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    code = Column(String(2))
    name_en = Column(String(100))
    name_fr = Column(String(100))


class Geocoding(Base):
    __tablename__ = 'geocoding'

    id = Column(Integer, primary_key=True)
    city = Column(String(100), nullable=False, index=True, server_default=text("''"))
    lat = Column(Float(asdecimal=True))
    long = Column(Float(asdecimal=True))

    def __init__(self, city, lat, long):
        self.city = city
        self.lat = lat
        self.long = long

    def __repr__(self):
        return "%s (%f, %f)" % (self.city, self.lat, self.long)


class Participant(Base):
    __tablename__ = 'participant'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(100))
    lastname = Column(String(100))
    sex = Column(String(10))
    street = Column(String(100))
    city = Column(String(100))
    zip = Column(String(20))
    _country = Column("country", String(2), ForeignKey('countries.code'))
    final_part = Column(SmallInteger, ForeignKey('parts.id'))
    part1 = Column(SmallInteger)
    part2 = Column(SmallInteger)
    paypal_token = Column(String(30), index=True)
    last_paypal_status = Column("last_paypal_status", SmallInteger, ForeignKey("paypal_statuses.id"))
    email = Column(String(100), unique=True)
    exp_quartet = Column(String)
    exp_brigade = Column(String)
    exp_chorus = Column(String)
    exp_musical = Column(String)
    exp_reference = Column(String)
    application_time = Column(DateTime)
    comments = Column(String)
    registration_status = Column(SmallInteger)
    donation = Column(Integer)
    iq_username = Column(String(100))

    s_final_part = relationship("Part", backref=backref("participants"))
    country = relationship("Country", backref=backref("participants"))
    paypal_status = relationship("PaypalStatus", backref=backref("participants"))

    def city_with_country(self):
        return "%s, %s" % (self.city, self._country)

    def makeMapLabel(self):
        line1 = "%s %s (%s / %s)" % (self.firstname, self.lastname, self.shortsex(), self.shortpart())
        line2 = "<a href=\'mailto:%s\'>%s</a>" % (self.email, self.email)
        return '"%s<br/>%s"' % (line1, line2)

    def shortsex(self):
        return self.sex[0].upper()

    def shortpart(self):
        return self.s_final_part.short()

    def fullname(self):
        return "%s %s" % (self.firstname, self.lastname)

    def fullnameLF(self):
        return "%s, %s" % (self.lastname, self.firstname)

    def paypalStatus(self):
        return "xx"

    def __repr__(self):
        return "%s %s (%d)" % (self.firstname, self.lastname, self.id)


class ExtrasCode(Base):
    __tablename__ = "extras_code"

    id = Column(Integer, ForeignKey('participant.id'), primary_key=True)
    code = Column(String(16))

    participant = relationship("Participant", backref=backref("code"))


class Part(Base):
    __tablename__ = 'parts'
    shortparts = ["--", "Tn", "Ld", "Br", "Bs"]

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(10))

    def short(self):
        return self.shortparts[self.id]

    def __repr__(self):
        return self.name


class PaypalHistory(Base):
    __tablename__ = 'paypal_history'

    id = Column(Integer, primary_key=True)
    participant_id = Column(Integer)
    timestamp = Column(DateTime)
    _paypal_status = Column("paypal_status", Integer, ForeignKey("paypal_statuses.id"))
    data = Column(String)
    payment_step = Column(SmallInteger, nullable=False, server_default=text("'1'"))

    paypal_status = relationship("PaypalStatus", backref=backref("history_items"))


paypal_shortnames = ["", "uninit", "token", "callback", "approved", "paid", "cancelled", "error"]

class PaypalStatus(Base):
    __tablename__ = 'paypal_statuses'

    id = Column(Integer, primary_key=True)
    paypal_status_name = Column(String(20))

    def shortname(self):
        return paypal_shortnames[self.id]


class RegistrationStatus(Base):
    __tablename__ = 'registration_statuses'

    id = Column(Integer, primary_key=True)
    registration_status = Column(String(100))


class Sex(Base):
    __tablename__ = 'sexes'

    id = Column(Integer, primary_key=True)
    name = Column(String(10))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    password = Column(String(100))

class Extra(Base):
    __tablename__ = 'extras'

    uid = Column(Integer, primary_key=True)
    id = Column(Integer, ForeignKey('participant.id'), nullable=False)
    roomtype = Column(SmallInteger, nullable=False)
    roompartner = Column(Integer)
    arrival_date = Column(Date, nullable=False)
    departure_date = Column(Date, nullable=False)
    num_show_tickets_regular = Column(SmallInteger, nullable=False)
    num_show_tickets_discount = Column(SmallInteger, nullable=False)
    t_shirt_sex = Column(SmallInteger, nullable=False)
    t_shirt_size = Column(String(5))
    other = Column(String(1000), nullable=False, server_default=text("''"))
    guest = Column(String(1000), nullable=False, server_default=text("''"))
    num_after_concert = Column(SmallInteger, nullable=False)
    num_lunch_saturday = Column(SmallInteger, nullable=False)
    num_dinner_friday = Column(SmallInteger, nullable=False)
    guest1_name = Column(String(200))
    guest1_arrival = Column(Date)
    guest1_departure = Column(Date)
    guest1_roomtype = Column(SmallInteger)
    guest2_name = Column(String(200))
    guest2_arrival = Column(Date)
    guest2_departure = Column(Date)
    guest2_roomtype = Column(SmallInteger)
    last_paypal_status = Column(SmallInteger)
    sat_night_restaurant = Column(String(100))
    sat_night_numpeople = Column(SmallInteger)
    phone = Column(String(100))

    participant = relationship("Participant", backref=backref("extras"))
