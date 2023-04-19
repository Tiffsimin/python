from datetime import date, datetime,time,date, timedelta
from beyond.core.reservation.reservation_models import Reservation
from beyond.core.reservation import reservation_repository
from beyond.core.reservation import revAcceptedNumRepository

class Reservation_management:
        
    def __init__(self, reservations):
        self.reservations = reservations
        self.customers_per_day = {}
           
    def generate_reservations_grouped_by_date(self):
        reservations_grouped_by_date = {}
        for reservation in self.reservations:
            date = reservation.datetime.date()
            if date in list(reservations_grouped_by_date):
                reservations_grouped_by_date[date].append(reservation)
                self.customers_per_day[date]+=reservation.customer_quantity
            else:
                reservations_grouped_by_date[date] = [reservation]
                self.customers_per_day[date] = reservation.customer_quantity
        return reservations_grouped_by_date

    def generate_reservations_grouped_by_date_from_db(self):
        reservations_grouped_by_date = {}
        for reservation in self.reservations:
            date = reservation['datetime'].date()
            if date in list(reservations_grouped_by_date):
                reservations_grouped_by_date[date].append(reservation)
                self.customers_per_day[date]+=reservation['customer_quantity']
            else:
                reservations_grouped_by_date[date] = [reservation]
                self.customers_per_day[date] = reservation['customer_quantity']
        return reservations_grouped_by_date


    
def total_customer_quantity(revs):
        total_quantity = 0
        for rev in revs:
            total_quantity += rev['customer_quantity']
        print('Total quantity' + str(total_quantity))
        return total_quantity

def is_reservation_auto_accepted(rev):
        print('is_reservation_auto_accepted called')
        time = rev.datetime
        time_before = time + timedelta(hours=2)
        time_after = time + timedelta(hours=-2)
        status = 1
        revs = reservation_repository.get_reservations(status, time_after, time_before)
        print('Number of the reservations in the period: ')
        revs_customer_quantity = total_customer_quantity(revs)
        total_quantity = revs_customer_quantity + rev.quantity
        default_accepted_quantity = revAcceptedNumRepository.read_revAcceptedNum()
        if total_quantity <= default_accepted_quantity:
            return True
        else:
            return False







       
