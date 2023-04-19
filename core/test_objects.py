from beyond.core.reservation.reservation_models import Customer_info, Reservation 
from beyond.core.reservation.reservation_management import Reservation_management
from datetime import datetime,date, time

def creat_test_objects():
#name, email, mobile
    c1 = Customer_info('ss','ss@gmail.com','00011123456')
    c2 = Customer_info('ii','ii@gmail.com','11100023456')
    c3 = Customer_info('mm','mm@gmail.com','11123456000')
    c4 = Customer_info('nn','nn@gmail.com','11123456111')
    c5 = Customer_info('ee','ee@gmail.com','11123456222')

    datetimes=[datetime(2021,12,17,12,15),datetime(2021,12,17,12,30),datetime(2021,12,17,13,15),datetime(2021,12,17,18,15),
    datetime(2021,12,8,12),datetime(2021,12,18,12,45),datetime(2021,12,18,13,30),datetime(2021,12,18,18,15),
    datetime(2021,12,19,11,30),datetime(2021,12,19,11,30),datetime(2021,12,19,12,00),datetime(2021,12,19,12,15),
    datetime(2021,12,19,13,30),datetime(2021,12,19,13,30),datetime(2021,12,19,18,30),datetime(2021,12,19,19,15)]
    #number, status, datetime, customer, customer_quantity, customer_note
    r1 = Reservation('1002',0,datetimes[0],c1, 2,'c1')
    r2 = Reservation('2003',0,datetimes[1],c1, 3,'c11')
    r3 = Reservation('305',0,datetimes[2],c1, 6,'c111')
    r4 = Reservation('404',0,datetimes[3],c2, 2,'c2')
    r5 = Reservation('505',0,datetimes[4],c2, 4,'c22')
    r6 = Reservation('606',0,datetimes[5],c2, 2,'c222')
    r7 = Reservation('707',0,datetimes[6],c3, 2,'c3')
    r8 = Reservation('808',0,datetimes[7],c3, 2,'c33')
    r9 = Reservation('907',0,datetimes[8],c3, 3,'c333')
    r10 = Reservation('1008',0,datetimes[9],c4, 2,'c4')
    r11 = Reservation('1107',0,datetimes[10],c4, 6,'c44')
    r12 = Reservation('1206',0,datetimes[11],c4, 2,'c444')
    r13 = Reservation('1305',0,datetimes[12],c5, 2,'c5')
    r14 = Reservation('1407',0,datetimes[13],c5, 1,'c55')
    r15 = Reservation('1506',0,datetimes[14],c5, 5,'c555')

    reservations = []
    reservations.append(r1) 
    reservations.append(r2)
    reservations.append(r3)
    reservations.append(r4)
    reservations.append(r5)
    reservations.append(r6)
    reservations.append(r7)
    reservations.append(r8)
    reservations.append(r9)
    reservations.append(r10)
    reservations.append(r11)
    reservations.append(r12)
    reservations.append(r13)
    reservations.append(r14)
    reservations.append(r15)

    return reservations

    date1 = datetimes[0].date()
    date2 = datetimes[5].date()
    date3 = datetimes[10].date()
    r = Reservation_management(reservations)
    results = r.generate_reservations_grouped_by_date()
    #print(results)
    print(r.customers_per_day)
    print(len(results[date3]))







