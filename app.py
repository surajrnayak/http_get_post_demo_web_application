from datetime import datetime
from flask import Flask, render_template, request
import sqlite3 as sql
import logging

app = Flask(__name__)

conn = sql.connect('database.db')
cursor = conn.cursor()
listOfTables = cursor.execute(
    """SELECT name FROM sqlite_master WHERE type='table'
    AND name='data_table'; """).fetchall()

if listOfTables == []:
    table = """CREATE TABLE data_table(TimeStamp VARCHAR(255), FirstName VARCHAR(255), LastName VARCHAR(255), URL VARCHAR(255));"""
    cursor.execute(table)


@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/postreq')
def new_student():
    return render_template('postreq.html')


@app.route('/getreq')
def get_req():
    return render_template('getreq.html')


@app.route('/requestsuccess', methods=['POST', 'GET'])
def requestsuccess():
    try:
        if request.method == 'POST':
            Fname = request.form['fnm']
            Lname = request.form['lnm']

        elif request.method == 'GET':
            Fname = request.args.get('fnm')
            Lname = request.args.get('lnm')

        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y %H:%M:%S")

        url = request.url

        with sql.connect("database.db") as con:
            cur = con.cursor()

            cur.execute("INSERT INTO data_table (TimeStamp,FirstName,LastName,URL)VALUES(?, ?, ?, ?)",
                        (date_str, Fname, Lname, url))

            con.commit()
            msg = "Hurray..! Contents added to database table successfully"

            # writting into text file
            with open("content.txt", "a") as nf:
                nf.write(date_str + '\t' + Fname + '\t' + Lname + '\t' + url)
                nf.write('\n')
                nf.close()
    except:
        con.rollback()
        msg = "Oops..! Failed adding contents to database."

    finally:
        return render_template("info.html", msg=msg, date_str=date_str, Fname=Fname, Lname=Lname, url=url)
        con.close()


@app.route('/content')
def conetent():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from data_table")

    rows = cur.fetchall();
    return render_template("contents.html", rows=rows)


if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.INFO)
    app.run(debug=True,host='0.0.0.0')
