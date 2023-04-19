class Customer_info:   
    def __init__(self, name, email, mobile):
        self.name = name
        self.email = email
        self.mobile = mobile

class Reservation:   
    def __init__(self, number, status, datetime, name, mobile, email, quantity, note):
        self.number = number
        self.status = status
        self.datetime = datetime
        self.name = name
        self.mobile = mobile
        self.email = email
        self.quantity = quantity
        self.note = note