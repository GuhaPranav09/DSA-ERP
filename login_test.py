import mysql.connector


con = mysql.connector.connect(host='localhost', user='root', passwd='mysql')
myc = con.cursor()

myc.execute("use user_info")
myc.execute("create table if not exists login(username varchar (50), password varchar (50))")
insert_query = "insert into login (username, password) values (%s, %s)"
data = ("user", "pwd")
myc.execute(insert_query, data)
con.commit()
