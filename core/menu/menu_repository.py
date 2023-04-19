from beyond.db import get_db

def write_dish(lang_code, id, name, description, is_vegi,code, uploadedimg_link, spiciness, price, category):
    db = get_db()
    db.execute(
        'INSERT INTO dish (id, is_vegi, code, img, spiciness, price, category)'
        ' VALUES (?,?,?,?,?,?,?)',
        (id, is_vegi, code, uploadedimg_link, spiciness, price, category)
        )
    if lang_code == 'en':
        db.execute(
            'INSERT INTO dishDesEn (name, description, dishId)'
            ' VALUES (?,?,?)',
            (name, description,id))
    elif lang_code == 'zh':
        db.execute(
            'INSERT INTO dishDesZh (name, description, dishId)'
            ' VALUES (?,?,?)',
            (name, description,id))
    elif lang_code == 'de':
        db.execute(
            'INSERT INTO dishDesDe (name, description, dishId)'
            ' VALUES (?,?,?)',
            (name, description,id))
    db.commit()
    db.close

def write_dishDesEn(name, description,dishId):
    db = get_db()
    db.execute(
        'INSERT INTO dishDesEn (name, description, dishId)'
        ' VALUES (?,?,?)',
        (name, description,dishId))
    db.commit()
    db.close

def write_dishDesDe(name, description,dishId):
    db = get_db()
    db.execute(
        'INSERT INTO dishDesDe (name, description, dishId)'
        ' VALUES (?,?,?)',
        (name, description,dishId))
    db.commit()
    db.close

def write_dishDesZh(name, description,dishId):
    db = get_db()
    db.execute(
        'INSERT INTO dishDesZh (name, description, dishId)'
        ' VALUES (?,?,?)',
        (name, description,dishId))
    db.commit()
    db.close

def update_dishDesEn(name, description,dishId):
    db = get_db()
    db.execute(
        'UPDATE dishDesEn Set name=?, description=?'
        ' WHERE dishId=?',
        (name, description,dishId)
        )
    db.commit()
    db.close

def update_dishDesDe(name, description,dishId):
    db = get_db()
    db.execute(
        'UPDATE dishDesDe Set name=?, description=?'
        ' WHERE dishId=?',
        (name, description,dishId)
        )
    db.commit()
    db.close

def update_dishDesZh(name, description,dishId):
    db = get_db()
    db.execute(
        'UPDATE dishDesZh Set name=?, description=?'
        ' WHERE dishId=?',
        (name, description,dishId)
        )
    db.commit()
    db.close

def read_dish(id, lang_code):
        db = get_db()
        db.row_factory = make_dicts
        if lang_code == 'en':
            dish = db.execute(
                'SELECT  d.id, code, is_vegi, img, spiciness, price, category, added, name, description'
                ' FROM dish d JOIN dishDesEn e ON d.id = e.dishId'
                ' WHERE d.id = ?', (id,)
            ).fetchone()
        elif lang_code == 'zh':
            dish = db.execute(
                'SELECT  d.id, code, is_vegi, img, spiciness, price, category, added, name, description'
                ' FROM dish d JOIN dishDesZh z ON d.id = z.dishId'
                ' WHERE d.id = ?', (id,)
            ).fetchone()
        elif lang_code == 'de':
            dish = db.execute(
                'SELECT  d.id, code, is_vegi, img, spiciness, price, category, added, name, description'
                ' FROM dish d JOIN dishDesDe de ON d.id = de.dishId'
                ' WHERE d.id = ?', (id,)
            ).fetchone()
        db.commit()
        db.close
        return dish

def update_dish(id, code, name, description, is_vegi, uploadedimg_link, spiciness, price, category, lang_code):
    db = get_db()
    db.execute(
        'UPDATE dish SET code=?, is_vegi=?,img=?, spiciness=?, price=?, category=?'
        ' WHERE id=?',
        (code, is_vegi, uploadedimg_link,spiciness, price, category, id)
        )
    if lang_code == 'en':
        db.execute(
            'UPDATE dishDesEn SET name=?, description=?'
            ' WHERE dishId=?',
            (name, description, id))
    elif lang_code == 'zh':
        db.execute(
            'UPDATE dishDesZh SET name=?, description=?'
            ' WHERE dishId=?',
            (name, description, id))
    elif lang_code == 'de':
        db.execute(
            'UPDATE dishDesDe SET name=?, description=?'
            ' WHERE dishId=?',
            (name, description, id))
    db.commit()
    db.close

def delete_dish(id):
    db = get_db()
    db.execute('DELETE FROM dish WHERE id = ?', (id,))
    db.execute('DELETE FROM dishDesEn WHERE dishId = ?', (id,))
    db.execute('DELETE FROM dishDesZh WHERE dishId = ?', (id,))
    db.execute('DELETE FROM dishDesDe WHERE dishId = ?', (id,))
    db.commit()
    db.close

def read_all_dishes(lang_code):
    db = get_db()
    db.row_factory = make_dicts
    if lang_code == 'en':
        #important!!!! leave a space between clauses!!
        dishes = db.execute(
            'SELECT dish.id, code, is_vegi, img, spiciness, price, category, added, name, description'
            ' FROM dish'
            ' INNER JOIN dishDesEn'
            ' ON dish.id = dishDesEn.dishId'
            ' ORDER BY code DESC'
        ).fetchall()
    elif lang_code == 'zh':
        dishes = db.execute(
            'SELECT  dish.id, dish.code, dish.is_vegi, dish.img, dish.spiciness, dish.price, dish.category, dish.added,'
            'dishDesZh.name, dishDesZh.description'
            ' FROM dish JOIN dishDesZh ON dish.id = dishDesZh.dishId'
            ' ORDER BY dish.code DESC'
        ).fetchall()
    elif lang_code == 'de':
        dishes = db.execute(
            'SELECT  dish.id, dish.code, dish.is_vegi, dish.img, dish.spiciness, dish.price, dish.category, dish.added,'
            'dishDesDe.name, dishDesDe.description'
            ' FROM dish JOIN dishDesDe ON dish.id = dishDesDe.dishId'
            ' ORDER BY dish.code DESC'
        ).fetchall()


    db.commit()
    db.close
    return dishes

def read_drink(id):
    db = get_db()
    db.row_factory = make_dicts
    drink = db.execute('SELECT * FROM drink WHERE id = ?', (id,)).fetchone()
    db.commit()
    db.close
    return drink

def read_all_drinks():
    db = get_db()
    db.row_factory = make_dicts
    drinks = db.execute('SELECT  * FROM drink ORDER BY added DESC').fetchall()
    db.commit()
    db.close
    return drinks

def write_drink(name, code, size, price, caterory = 'Drinks'):
    db = get_db()
    db.execute(
        'INSERT INTO drink (name, code, size, price, category)'
        ' VALUES (?,?,?,?,?)',
        (name, code, size, price, caterory)
        )
    db.commit()
    db.close

def update_drink_db(name, code, size, price, id):
    db = get_db()
    db.execute('UPDATE drink SET name=?, code=?, size=?, price=? WHERE id=?',
    (name, code, size, price, id))
    db.commit()
    db.close

def delete_drink_db(id):
    db = get_db()
    db.execute('DELETE FROM drink WHERE id = ?', (id,))
    db.commit()
    db.close

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))
