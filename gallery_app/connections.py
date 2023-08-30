import pymysql
db = pymysql.connect(user="root",password="",host="localhost",database="art_gallery")

def insert(qry):
    cur = db.cursor()
    cur.execute(qry)
    db.commit()

def selectall(qry):
    cur = db.cursor()
    cur.execute(qry)
    data= cur.fetchall()
    return data

def select(qry):
    cur = db.cursor()
    cur.execute(qry)
    data = cur.fetchone()
    return data

def delete(qry):
    cur = db.cursor()
    cur.execute(qry)
    db.commit()

def update(qry):
    cur = db.cursor()
    cur.execute(qry)
    db.commit()