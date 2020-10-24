import pymysql
import var

# class db():
#     def __init__(self, ip, )

def create_db():
    databaseServerIP = var.db_ip # IP address of the MySQL database server
    port = var.db_port
    databaseUserName = var.db_user       # User name of the database server
    databaseUserPassword = var.db_pass           # Password for the database user
    newDatabaseName = var.db_name # Name of the database that is to be created
    charSet = "utf8mb4"     # Character set
    cusrorType = pymysql.cursors.DictCursor
    connectionInstance = pymysql.connect(host=databaseServerIP, port=port, user=databaseUserName, password=databaseUserPassword, charset=charSet,cursorclass=cusrorType)

    try:
        # Create a cursor object
        cursorInsatnce = connectionInstance.cursor()
        # try:  
        #     sqlStatement            = "DROP DATABASE "+self.newDatabaseName  
        #     # Execute the create database SQL statment through the cursor instance
        #     cursorInsatnce.execute(sqlStatement)  
        # except Exception as e:
        #       print("Exeception occured:{}".format(e)) 
        try:                             
            # SQL Statement to create a database
            sqlStatement = "CREATE DATABASE " + newDatabaseName  
            # Execute the create database SQL statment through the cursor instance
            cursorInsatnce.execute(sqlStatement)
             # SQL query string
            sqlQuery = "SHOW DATABASES"
            # Execute the sqlQuery
            cursorInsatnce.execute(sqlQuery)
            #Fetch all the rows
            databaseList = cursorInsatnce.fetchall()
            for datatbase in databaseList:
                print(datatbase)
            
        except Exception as e:
            print("Exeception occured:{}".format(e))
       

    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        connectionInstance.close()

    con = db_ceate()
    con.create_table()
    con.close()


class db_ceate():
    def __init__(self):
        db_ip = var.db_ip # IP address of the MySQL database server
        db_port = var.db_port
        db_user = var.db_user       # User name of the database server
        db_pass = var.db_pass           # Password for the database user
        db_name = var.db_name # Name of the database that is to be created
        self.db = pymysql.connect(host=db_ip, port=db_port, user=db_user, password=db_pass, db=db_name)
        
    def create_table(self):
        try:
            try:
                # Create a cursor object
                cursor = self.db.cursor()

                # Drop table if it already exist using execute() method.
                # cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

                # Create table as per requirement
                sql = """CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username  VARCHAR(255) NOT NULL,
                password  VARCHAR(255) NOT NULL,
                playlist  VARCHAR(255) NOT NULL, 
                proxy_ip VARCHAR(255) NOT NULL, 
                site  VARCHAR(255) NOT NULL
                )"""

                cursor.execute(sql)
            except Exception as e:
                print("Exeception occured:{}".format(e))

            sql = """CREATE TABLE songs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            count INT DEFAULT 0,
            stream_link  VARCHAR(255) NOT NULL,
            song_name  VARCHAR(255) NOT NULL,
            playlist  VARCHAR(255) NOT NULL,  
            site  VARCHAR(255) NOT NULL
            )"""

            cursor.execute(sql)


        except Exception as e:
            print("Exeception occured:{}".format(e))

    def create_demo_playlist(self):
        try:
            songsList = ["https://open.spotify.com/track/09AFPW849hF9AR37J48oDY" ,
            "https://open.spotify.com/track/7oKRShByLwzgbHirdZcPrE"]

            cursor = self.db.cursor()

            for song in songsList:
                sql = """INSERT INTO songs(stream_link,
                song_name, playlist, site)
                VALUES ("{}", "Random song", "Demo", "spotify")""".format(song)

                cursor.execute(sql)

            self.db.commit()
        except Exception as e:
            print("Exeception occured:{}".format(e))
            self.db.rollback()

    def add_song(self, info):
        try:
            cursor = self.db.cursor()

            sql = """INSERT INTO songs(stream_link,
            song_name, playlist, site)
            VALUES ("{}", "{}", "{}", "{}")""".format( info[0], info[1], info[2], info[3])

            cursor.execute(sql)

            self.db.commit()
        except Exception as e:
            print("Exeception occured:{}".format(e))
            self.db.rollback()
    
    def update_count(self, id):
        try:
            cursor = self.db.cursor()

            sql = """UPDATE songs SET count = count + 1
                          WHERE songs.id = {}""".format(id)

            cursor.execute(sql)
            
            self.db.commit()
        except Exception as e:
            print("Exeception occured:{}".format(e))
            self.db.rollback()

    def add_account(self, info):
        try:
            cursor = self.db.cursor()

            sql = """INSERT INTO users(username,
            password, playlist, proxy_ip, site)
            VALUES ("{}", "{}", "{}", "{}", "{}"
            )""".format( info[0], info[1], info[2], info[3], info[4])

            cursor.execute(sql)
            
            self.db.commit()
        except Exception as e:
            print("Exeception occured:{}".format(e))
            self.db.rollback()

    def update_user_playlist(self, id, playlist, proxy_ip):
        try:
            cursor = self.db.cursor()

            sql = """UPDATE users SET playlist = "{}", proxy_ip = "{}"
                    WHERE users.id = {}""".format( playlist, proxy_ip, id)

            cursor.execute(sql)
            
            self.db.commit()
        except Exception as e:
            print("Exeception occured:{}".format(e))
            self.db.rollback()
    
    def remove_account(self, id):
        try:
            cursor = self.db.cursor()

            sql = """DELETE FROM users
            WHERE users.id = {}""".format(id)

            cursor.execute(sql)
            
            self.db.commit()
        except Exception as e:
            print("Exeception occured:{}".format(e))
            self.db.rollback()
    
    def remove_song(self, id):
        try:
            cursor = self.db.cursor()

            sql = """DELETE FROM songs
            WHERE songs.id = {}""".format(id)

            cursor.execute(sql)
            
            self.db.commit()
        except Exception as e:
            print("Exeception occured:{}".format(e))
            self.db.rollback()

    def fetch_table(self, table_name):
        try:
            cursor = self.db.cursor()

            sql = """Select * FROM {}""".format(table_name)

            cursor.execute(sql)
            result = cursor.fetchall()

            return result
            
        except Exception as e:
            print("Exeception occured:{}".format(e))

    def get_playlist(self, playlist):
        try:
            cursor = self.db.cursor()

            sql = """Select * FROM songs
            WHERE songs.playlist = '{}'""".format(playlist)

            cursor.execute(sql)
            result = cursor.fetchall()

            return result
            
        except Exception as e:
            print("Exeception occured:{}".format(e))

    def close(self):
        self.db.close()




if __name__ == "__main__":
    create_db()
    temp = db_ceate()
    # temp.create_table()
    temp.create_demo_playlist()
    temp.close()