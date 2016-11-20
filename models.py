import sqlite3 as sql

def insertUser(email, password):
  con = sql.connect("myData.db")
  cur = con.cursor()
  cur.execute("INSERT INTO users (email,password) VALUES (?,?)", (email,password))
  con.commit()
  con.close()

def retrieveUsers():
  con = sql.connect("myData.db")
  cur = con.cursor()
  cur.execute("SELECT email, password FROM users")
  users = cur.fetchall()
  con.close()
  return users
