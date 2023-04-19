from beyond.db import get_db
from beyond.core.order.order import Order, Ordered_item,Order_specification

def write_order_specification(specification, item_code, order_number):
    db = get_db()
    db.execute(
        'INSERT INTO orderSpecification (quantity, spiciness, saltiness,oiliness, avoided_ingredients, note, ordered_item_code, order_number)'
        ' VALUES (?,?,?,?,?,?,?,?)',
        (specification.quantity,specification.spiciness, specification.saltiness, specification.oiliness,
        specification.avoided_ingredients,specification.note, item_code, order_number)
        )
    db.commit()
    db.close

def delete_order_specification(item_code, order_number):
    db = get_db()
    db.execute('DELETE FROM orderSpecification WHERE ordered_item_code = ? and order_number = ?',
     (item_code, order_number,)
     )
    db.commit()
    db.close

def read_order_specifications(item_code, order_number):
    db = get_db()
    db.row_factory = make_dicts
    specs = db.execute(
        'SELECT * FROM orderSpecification WHERE ordered_item_code = ? AND order_number = ?', 
        (item_code, order_number)
    ).fetchall()
    #print(specs )   
    print(type(specs))        
    if specs == None:
        print('Miaoooooo None none none')
        return []
    #no need for spec in specs:
    #no need     specifications.append(Order_specification(spec['quantity'], spec['spiciness'], spec['saltiness'],
    #no need    spec['oiliness'], spec['avoided_ingredients'], spec['note']))
    return specs

def write_ordered_item(item, order_number):
     db = get_db()
     db.execute(
         'INSERT INTO orderedItem (code, name, price, quantity, price_sum, order_number)'
         ' VALUES (?,?,?,?,?,?)',
         (item.code,item.name, item.price, item.quantity,item.price_sum, order_number)
        )
     for spec in item.specifications: 
         write_order_specification(spec, item.code, order_number)
     db.commit()
     db.close

def delete_ordered_item(item_code, order_number):
    db = get_db()
    db.execute('DELETE FROM orderedItem WHERE code = ? AND order_number = ?',
     (item_code, order_number,)
     )  
    delete_order_specification(item_code, order_number)
    db.commit()
    db.close

def read_ordered_items(order_number):
    ordered_items = []
    db = get_db()
    db.row_factory = make_dicts
    items = db.execute(
        'SELECT * FROM orderedItem WHERE order_number = ?', 
        (order_number,)
    ).fetchall()
    for item in items: 
        specs = read_order_specifications(item['code'], order_number)
        ordered_items.append(Ordered_item(item['code'], item['name'], item['price'], 
        item['quantity'], specs))
    return ordered_items

def write_order(order, order_number):
     db = get_db()
     db.execute(
         'INSERT INTO orderInfo (discount_rate, ori_cost, final_cost, order_number)'
         ' VALUES (?,?,?,?)',
         (order.discount_rate, order.ori_cost, order.final_cost, order_number)
        )
     for item in order.ordered_items: 
         write_ordered_item(item, order_number)
     db.commit()
     db.close

def delete_order(order_number):
     db = get_db()
     db.execute('DELETE FROM orderInfo WHERE order_number = ?', (order_number,))
     db.row_factory = make_dicts
     items = db.execute(
        'SELECT * FROM orderedItem WHERE order_number = ?', 
        (order_number,)
        ).fetchall()
     for item in items: 
         delete_ordered_item(item['code'], order_number)
     db.commit()
     db.close

def read_order(order_number):
    db = get_db()
    db.row_factory = make_dicts
    db_order = db.execute(
        'SELECT * FROM orderInfo WHERE order_number = ?', 
        (order_number,)
    ).fetchone()
    ordered_items = read_ordered_items(order_number)
    order = Order(ordered_items,  db_order['ori_cost'], db_order['placed_at'], db_order['discount_rate'])
    return order

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))
