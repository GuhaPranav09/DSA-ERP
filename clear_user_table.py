import mysql.connector


con = mysql.connector.connect(host='localhost', user='root', passwd='mysql')
myc = con.cursor()

myc.execute("use user_info")
insert_query = "delete from users"
myc.execute(insert_query)
con.commit()
