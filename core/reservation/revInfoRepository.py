from beyond.db import get_db

def write_revInfo(note, has_arrived, rev_number):
    db = get_db()
    db.execute(
        'INSERT INTO revInfo (admin_note, has_arrived, rev_number)'
        ' VALUES (?,?,?)',
        (note, has_arrived, rev_number)
        )
    db.commit()
    db.close


def read_all_revInfo():
    db = get_db()
    db.row_factory = make_dicts
    info_records = db.execute('SELECT  * FROM revInfo').fetchall()
    db.commit()
    db.close
    return info_records

def update_revInfo_note(note, rev_number):
    db = get_db()
    db.row_factory = make_dicts
    db.execute(
            'UPDATE revInfo SET admin_note=?'
            'WHERE rev_number = ?',
            (note, rev_number)
            )
    db.commit()
    db.close

def update_revInfo_arrive(has_arrived, rev_number):
    db = get_db()
    db.row_factory = make_dicts
    db.execute(
            'UPDATE revInfo SET has_arrived=?'
            'WHERE rev_number = ?',
            (has_arrived, rev_number)
            )
    db.commit()
    db.close

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))