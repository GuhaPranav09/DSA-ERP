import mysql.connector


con = mysql.connector.connect(host='localhost', user='root', passwd="Techno$pider2099")
myc = con.cursor()

myc.execute("use user_info")
myc.execute("create table if not exists login(Site int, username varchar (50), password varchar (50))")
insert_query = "insert into login (Site, username, password) values (%s, %s, %s)"
data = (1,"user1", "pwd")
myc.execute(insert_query, data)
con.commit()
