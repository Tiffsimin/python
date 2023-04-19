from datetime import date,datetime,time

class Pickup_order:
    def __init__(self, order_number, customer_name, phone, email, pickup_time, delayed_mins, order):
        self.order_number = order_number
        self.customer_name = customer_name
        self.phone = phone
        self.email = email
        self.pickup_time = pickup_time
        self.delayed_mins = delayed_mins
        self.order = order

    @staticmethod
    def validate_time(pickup_datetime):
        pickup_date = pickup_datetime.date()
        order_time = datetime.now()
        #there should be at least 20 mins between the pickup time and the order time
        cookting_time = pickup_datetime - order_time
        cookting_time_mins = cookting_time.total_seconds()/60

        #Check is the pickup time is within the restaurant's openning hours
        #here hard code the restaurant openning hours, maybe later use the set openning hours
        #The hardcoded opening hour: 11:50-2; 6:20-10
        #Should I check if its week day or weekend?
        def is_restaurant_open_at(pickup_datetime):
            lunch_start = datetime.combine(pickup_date,time(11, 20))
            lunch_end = datetime.combine(pickup_date,time(14, 0))
            dinner_start = datetime.combine(pickup_date,time(18, 20))
            dinner_end = datetime.combine(pickup_date,time(22, 00))
            if ((pickup_datetime >= lunch_start and pickup_datetime <= lunch_end) 
            or (pickup_datetime >= dinner_start and pickup_datetime <= dinner_end)):
                return True
            return False
        if(is_restaurant_open_at(pickup_datetime) == False):
            return 'The restaurant is closed at the desinated pickup time!'
        if(cookting_time_mins < 20):
            return 'Please allow at least 20 minutes for us to prepare for your order!'
        return 'valid'
    
#The general order
class Order:
    def __init__(self, ordered_items, cost, placed_at=datetime.now(), discount_rate=1):
        #ordered_items is an array here,give reason later
        if(type(ordered_items) is dict):
            self.ordered_items =  self.generate_ordered_item_dic(ordered_items)
        else:
            self.ordered_items = ordered_items
        self.placed_at = placed_at
        self.discount_rate = discount_rate
        self.ori_cost = int(cost)
        self.final_cost =  self.calculate_price()
    
    def generate_ordered_item_dic(self, ordered_items):
        items = []
        for key in  ordered_items:
            item = Ordered_item(ordered_items[key]['code'],ordered_items[key]['name'],
            ordered_items[key]['price'],ordered_items[key]['quantity'], ordered_items[key]['specifications'])
            items.append(item)
        return items

    def set_discount_rate(self, rate):
        self.discount_rate = rate
        
    def calculate_price(self):
        return self.ori_cost * self.discount_rate
    
    def to_string(self):
        ordered_items_str = ''
        for item in self.ordered_items:
            ordered_items_str = ordered_items_str + ';  Next item: ' + item.to_string()
        result = f'''The order : time: {self.placed_at}, cost: {self.final_cost},
         ordered items: {ordered_items_str}'''
        return result

        
#The takeaway order taken from a customer
class Takeaway(Order):
    #Constructor, if customer_id=null,then the customer is not registered, in this case email and mobile must
    #be provided.
    #The total price and the discount is is caculated.
    def __init__(self, ordered_items, placed_at, receive_time, is_pickedup, prices, pack_method, payment_method,
                 customor_name, customer_id=-1, email="", mobile=""):
        super().__init__(self, ordered_items, placed_at)
        self.receive_time = receive_time
        self.is_pickedup = is_pickedup
        self.pack_method = pack_method
        self.payment_method = payment_method
        self.customor_name = customor_name
        self.customer_id = customer_id
        self.email = email
        self.mobile = mobile
        self.discount = self.calculate_discount()

    def calculate_discount(self):
        pass

#The order item, could be main course, drink, combo and could be multiple
#id code name price quantity price_sum 
class Ordered_item:   
    #id, code, name: String
    #price, price_sum: float; quantity: int
    #specification: Order_specification
    def __init__(self, code, name, price, quantity, specifications):
        self.code = code
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)
        self.price_sum = float(price) * float(quantity)
        self.set_specification(specifications)

    def set_specification(self, specs):
        self.specifications = []
        for spec in specs:
         #no need if(type(spec) is dict), all are dic
            spec_in_memory = Order_specification(spec['quantity'], spec['spiciness'], spec['saltiness'], spec['oiliness'],spec['avoided_ingredients'], spec['note'])
            self.specifications.append(spec_in_memory)
    
    def to_string(self):
        spec_str = ''
        for spec in self.specifications:
            spec_str = spec_str + ';  Next specification: ' + spec.to_string()
        result = f'''The ordered item: code: {self.code}, name: {self.name}, price:  {self.price},  
         quantity: {self.quantity}, price_sum: {self.price_sum}, specifications: {spec_str}'''
        return result

class Order_specification:
    #Spiciness: int(-1,0,1); saltiness: int(-1,0,1) less, same, more
    #oil_level: int(-1, 0,1) less, same, more; note: String
    #avoided_ingredients: dictionary {garlic:bool, nuts:bool, msg:bool, meat:bool}
    def  __init__(self, quantity, spiciness=0, saltiness=0, oiliness=0, avoided_ingredients=
                    {'garlic': False, 'nuts': False, 'msg':False, 'meat': False},
                     note=''):
        self.quantity = quantity
        self.spiciness = spiciness
        self.saltiness = saltiness
        self.oiliness = oiliness
        self.avoided_ingredients = avoided_ingredients
        self.note = note
    
    def to_string(self):
        result = f'''The specification: quantity: {self.quantity}, spiciness: {self.spiciness}, 
         saltiness: {self.saltiness}, oiliness: {self.oiliness}, avoided_ingredients: 
         {self.avoided_ingredients}, note: {self.note}'''
        return result
        

        

        
