from beyond.core import test_objects
from beyond.core.reservation.reservation_models import Reservation
from beyond.core.reservation.reservation_management import total_customer_quantity, is_reservation_auto_accepted
from beyond.core.reservation import reservation_repository
from beyond.core.reservation import reservation_managment
from datetime import date, datetime,time,date

def test_write_and_read_rev(rev):
    reservation_repository.write_reservation(rev)
    retrieved_rev = reservation_repository.read_reservation(rev.number)
    return

def test_get_revs(status=0, time_after=datetime.now(), time_before=datetime(2032,12,5)):
    revs = reservation_repository.get_reservations(status, time_after, time_before)
    pass

def test_del_rev(revNum):
    pass

def test_is_rev_auto_accepted(rev):
    result = is_reservation_auto_accepted(rev)
    pass

reservations = test_objects.creat_test_objects()
for rev in reservations:
    test_write_and_read_rev(rev)


