from beyond.db import get_db

def write_revAcceptedNum(num):
    db = get_db()
    if db.execute('SELECT number FROM revAcceptedNum WHERE id = ?', (1,)
        ).fetchone() is None:
        #------
        print('First record ' + str(num))
        #------
        db.execute(
            'INSERT INTO revAcceptedNum (id, number)'
            ' VALUES (?,?)',
            (1, num)
            )
    else:
        #------
        print('Update record ' + str(num))
        #------
        db.execute(
            'UPDATE revAcceptedNum  SET number=?'
            'WHERE id = ?',
            (num, 1)
            )
    db.commit()
    db.close


def read_revAcceptedNum():
    db = get_db()
    db.row_factory = make_dicts
    num_record = db.execute('SELECT  * FROM revAcceptedNum').fetchone()
    if num_record is None:
        return 0
    num = num_record['number']
    #------
    print('The revAcceptedNum is: ' + str(num))
    #------
    db.commit()
    db.close
    return num

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))