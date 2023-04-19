from beyond.db import get_db

def write_revLGroupNum(num):
    db = get_db()
    if db.execute('SELECT number FROM revLGroupNum WHERE id = ?', (1,)
        ).fetchone() is None:
        db.execute(
            'INSERT INTO revLGroupNum (id, number)'
            ' VALUES (?,?)',
            (1, num)
            )
    else:
        db.execute(
            'UPDATE revLGroupNum  SET number=?'
            'WHERE id = ?',
            (num, 1)
            )
    db.commit()
    db.close

def read_revLGroupNum():
    db = get_db()
    db.row_factory = make_dicts
    num_record = db.execute('SELECT  * FROM revLGroupNum').fetchone()
    if num_record is None:
        return 0
    num = num_record['number']
    db.commit()
    db.close
    return num

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))