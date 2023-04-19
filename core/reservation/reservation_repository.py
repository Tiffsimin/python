from beyond.db import get_db
from beyond.core.reservation.reservation_models import Reservation
from datetime import date, datetime,time,date

#Get the reservation with the given reservation number
def read_reservation(revNum):
    db = get_db()
    db.row_factory = make_dicts
    reservation = db.execute('SELECT  * FROM reservation' 
                        ' WHERE number == ?',
                        (revNum,)
                        ).fetchone()
    db.commit()
    db.close
    return reservation

#Get reservations with given status and/or between a certain period
def get_reservations(status=0, time_after=datetime.now(), time_before=datetime(2032,12,5)):
    db = get_db()
    db.row_factory = make_dicts
    reservations = db.execute('SELECT * FROM reservation WHERE status == ? AND datetime > ? AND datetime < ?', 
    (status, time_after, time_before,)
    ).fetchall()
    db.commit()
    db.close
    return reservations

#Update a certain reservation's status or update the whole reservation
def undate_reservation(revNum, status=0, rev=None):
    db = get_db()
    if rev == None:
        db.execute('UPDATE reservation SET status = ? WHERE number = ?',
                    (1,  revNum)
                )
    else:
        write_reservation(rev)
        return
    db.commit()
    db.close

#Write a new reservation to the database
def write_reservation(rev):
    db = get_db()
    db.execute(
               'INSERT INTO reservation (number, status, datetime, customer_name,customer_mobile, customer_email, customer_quantity, customer_note)'
               ' VALUES (?,?,?,?,?,?,?,?)',
                (rev.number, 0, rev.datetime, rev.name, rev.mobile,rev.email,rev.quantity,rev.note)
           )
    db.commit()
    db.close

#Delete a reservation from the database
def delete_reservation(revNum):
    db = get_db()
    db.execute('DELETE FROM reservation WHERE number = ?', (revNum,))
    db.commit()
    db.close

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))