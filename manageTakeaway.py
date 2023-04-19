from datetime import timedelta,datetime
import os
from flask import (Flask, Blueprint, jsonify, flash, g, redirect, render_template, request, url_for,
    current_app)
from werkzeug.utils import secure_filename
from flask_babel import (Babel, _, refresh)
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb
from beyond.core.order.order import Pickup_order, Order, Ordered_item
from beyond.core.order.order_repository import write_order, read_order
from beyond.db import get_db
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb
from beyond.webForms import GeneralInfoForm
from beyond.admin.auth import login_required
from beyond.core.order.order_repository import delete_order, delete_ordered_item
from beyond.constants import ORDER_PARTIALLY_CANCEL_CUSTOMER, ORDER_DELAY_CUSTOMER, ORDER_CANCEL_CUSTOMER
from flask_mail import Mail, Message


bp = Blueprint('manageTakeaway', __name__, url_prefix='/<lang_code>/takeaway')

@bp.route('/overview')
@register_breadcrumb(bp, '.', 'Takeaway Management')
def overview():
    return render_template('admin/manageTakeaway/overview.html')

@bp.route('/new_orders', methods=('GET', 'POST'))
@register_breadcrumb(bp, '.Takeaway Management', 'New Orders')
@login_required
def new_orders():
    pickup_orders =[]
    db = get_db()
    db.row_factory = make_dicts
    #DESC or ASC
    db_pickup_orders = db.execute( 
        'SELECT * FROM pickupOrder WHERE is_cancelled = ? AND is_checked = ? AND pickup_time >= ?'
        'ORDER BY pickup_time ASC',
        (0, 0, datetime.now(),)
        ).fetchall()
    for order in db_pickup_orders:
        orderinfo = read_order(order['order_number'])
        pickup_orders.append(Pickup_order(order['order_number'], order['customer_name'], 
        order['phone'], order['email'], order['pickup_time'], order['time_delay'], orderinfo))
    return render_template('admin/manageTakeaway/newOrders.html', pickup_orders = pickup_orders,
    count= len(pickup_orders), lang_code = g.lang_code)

@bp.route('/all_orders', methods=('GET', 'POST'))
@register_breadcrumb(bp, '.New Orders', 'All Orders')
@login_required
def all_orders():
    error = None
    if request.method == 'POST':
        date_from = request.form['fromDate']
        date_to = request.form['toDate']
        if date_from > date_to:
            error = "The start date is later than the end date!"
        else:
            pickup_orders =[]
            db = get_db()
            db.row_factory = make_dicts
            db_pickup_orders = db.execute(
            'SELECT * FROM pickupOrder'
            ' WHERE is_cancelled=? And date(added) BETWEEN ? AND ?'
            ' ORDER BY added DESC'
            , (0, date_from, date_to,)        
            ).fetchall()
            for order in db_pickup_orders:
                orderinfo = read_order(order['order_number'])
                pickup_orders.append(Pickup_order(order['order_number'], order['customer_name'], 
                order['phone'], order['email'], order['pickup_time'],order['time_delay'], orderinfo))
            return render_template('admin/manageTakeaway/displayOrders.html', pickup_orders = pickup_orders,
                                    msg = _('From ')+date_from+_(' to ')+date_to)
        flash(error)  
    return render_template('admin/manageTakeaway/allOrders.html')

@bp.route('/delay_order', methods=('GET', 'POST'))
@login_required
def delay_order():
    error = None
    if request.method == 'POST':
        delayed_mins = int(request.form['delayedMins'])
        order_num = request.form['orderedNum']
        db = get_db()
        db.row_factory = make_dicts
        info = db.execute(
            'SELECT email, pickup_time, time_delay FROM pickupOrder'
            ' WHERE order_number=?',
            (order_num,)
        ).fetchone()       
        delayed_time = timedelta(minutes=delayed_mins)
        pickup_datetime = info['pickup_time'] + delayed_time
        delayed_mins = delayed_mins + info['time_delay']
        db.execute(
            'UPDATE pickupOrder SET pickup_time=?, time_delay=?'
            'WHERE order_number=?',
            (pickup_datetime, delayed_mins, order_num)
        )
        db.commit()
        #send_mail('ORDER_DELAY_CUSTOMER', info['email'], order_num)
        flash('The order is delayed, a email will be sent to the customer!')
        return redirect(url_for('manageTakeaway.new_orders'))
    return 'ok'

@bp.route('/reject_order', methods=('GET', 'POST'))
@login_required
def reject_order():
    is_wholeorder_cancelled = False
    if request.method == 'POST':
        db = get_db()
        db.row_factory = make_dicts
        order_num = request.form['orderNum']
        itemcodes = request.form.getlist('cancelledItemCodes')
        items = db.execute(
            'SELECT * FROM orderedItem WHERE order_number = ?', 
            (order_num,)
        ).fetchall()
        email = db.execute(
            'SELECT email FROM pickupOrder WHERE order_number = ?', 
            (order_num,)
            ).fetchone()
        if len(itemcodes) == len(items):
            is_wholeorder_cancelled = True
        if is_wholeorder_cancelled:
            db.execute(
                'UPDATE pickupOrder SET is_cancelled=?'
                'WHERE order_number=?',
                (1, order_num)
                )
            delete_order(order_num)
            #send_mail('ORDER_CANCEL_CUSTOMER', email['email'], order_num)
            flash('The order is cancelled, a email will be sent to the customer!')
        else:
            db.execute(
                'UPDATE pickupOrder SET is_partically_cancelled=?'
                'WHERE order_number=?',
                (1, order_num)
                )
            for code in itemcodes:
                delete_ordered_item(code, order_num)
            #send_mail('ORDER_PARTICALLY_CANCEL_CUSTOMER', email['email'], order_num)
            flash('Part of the order is cancelled, a email will be sent to the customer!')
        return redirect(url_for('manageTakeaway.new_orders'))
    return 'ok'

@bp.route('/complete_order', methods=('GET', 'POST'))
@login_required
def complete_order():
    order_num = request.get_json()
    db = get_db()
    db.execute(
        'UPDATE pickupOrder SET is_checked=?'
        'WHERE order_number=?',
        (1, order_num,)
        )
    db.commit()
    ################  msg may translate later #################
    result = 'The order is completed and removed from here!'
    return jsonify(result)

@bp.route('/print_order', methods=('GET', 'POST'))
@login_required
def print_order():
    order_num = request.get_json()
    #os.system("lpr -P printer_name /Users/siminxie/myproject/beyond/static/miao.txt")
    filename = 'miao.txt'
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    f = open(filepath, 'w')
    order = read_order(order_num)
    for item in order.ordered_items:
        line_text = item.name + ' ' + str(item.price) + ' ' + str(item.quantity)
        line_text = line_text + ' portions ' + str(item.price_sum) + '\n'
        f.write(line_text)
    f.write('---------------------------------------------\n')
    f.write('Total:' + str(order.final_cost) + '  chf')
    result = 'The order to be printed!'
    return jsonify(result)

@bp.route('/missed_orders')
@register_breadcrumb(bp, '.All Orders', 'Missed Orders')
@login_required
def missed_orders():
    pickup_orders =[]
    db = get_db()
    db.row_factory = make_dicts
    #DESC or ASC
    db_pickup_orders = db.execute( 
        'SELECT * FROM pickupOrder WHERE is_cancelled = ? And is_checked = ?'
        'ORDER BY added DESC',
        (0, 0,)
        ).fetchall()
    for order in db_pickup_orders:
        orderinfo = read_order(order['order_number'])
        pickup_orders.append(Pickup_order(order['order_number'], order['customer_name'], 
        order['phone'], order['email'], order['pickup_time'], order['time_delay'], orderinfo))
    return render_template('admin/manageTakeaway/missedOrders.html', pickup_orders = pickup_orders)

@bp.route('/cancelled_orders')
@register_breadcrumb(bp, '.Missed Orders', 'Cancelled Orders')
@login_required
def cancelled_orders():
    pickup_orders =[]
    db = get_db()
    db.row_factory = make_dicts
    pickup_orders = db.execute( 
        'SELECT * FROM pickupOrder WHERE is_cancelled = ?'
        'ORDER BY added DESC',
        (1,)
        ).fetchall()
    return render_template('admin/manageTakeaway/cancelledOrders.html', pickup_orders = pickup_orders)


def send_mail(type, email, order):
    if type == 'ORDER_DELAY_CUSTOMER':
        msg = Message('Restaurant Beyond Order Delay Notification', sender = 'siminxietiffany@gmail.com', 
        recipients = [email])
        msg.html = ORDER_DELAY_CUSTOMER(order)
    elif type == 'ORDER_CANCEL_CUSTOMER':
        msg = Message('Restaurant Beyond Order Cancalled', sender = 'siminxietiffany@gmail.com', 
        recipients = [email])
        msg.html = ORDER_CANCEL_CUSTOMER(order)
    elif type == 'ORDER_PARTIALLY_CANCEL_CUSTOMER':
        msg = Message('Restaurant Beyond Order Partially Cancalled', sender = 'siminxietiffany@gmail.com', 
        recipients = [email])
        msg.html = ORDER_PARTIALLY_CANCEL_CUSTOMER(order)
    mail=Mail(current_app)
    mail.send(msg)
    return "Sent"
    
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

@bp.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)

@bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')