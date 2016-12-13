def insert_record(db, name, year):

    cur = db.cursor()
    cur.execute('INSERT IGNORE INTO main (`Название публикации`, `Год издания`) VALUES (%s, %s)', (name, year))
    db.commit()


# select all publications
def select_pb(db):

    cur = db.cursor()
    cur.execute('SELECT `Название публикации` FROM main')
    db.commit()

    answer = list()
    for str_name in cur:
        answer.append(str_name[0])

    return answer


def select_pb_by_year(db, year):

    cur = db.cursor()
    cur.execute('SELECT `Название публикации` FROM main WHERE `Год издания` = %s', year)
    db.commit()

    answer = list()
    for str_name in cur:
        answer.append(str_name[0])

    return answer


def select_year_by_pb(db, pb):

    cur = db.cursor()
    cur.execute('SELECT `Год издания` FROM main WHERE `Название публикации` = %s', pb)
    db.commit()

    answer = None
    for str_year in cur:
        answer = str_year[0]

    return answer
