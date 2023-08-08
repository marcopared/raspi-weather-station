# Add the necessary imports
import mysql.connector as mysql
import os
import datetime
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

def add_to_db(**kwargs):
    db = mysql.connect(user=kwargs["user"], password=kwargs["password"], host=kwargs["host"])
    cursor = db.cursor()
    cursor.execute(f"USE {kwargs['db_name']}")

    try:
        query = f"INSERT INTO {kwargs['table_name']} (light, humidity, temperature) values (\"{kwargs['light']}\", \"{kwargs['humidity']}\", \"{kwargs['temp']}\");"
        cursor.execute(query)
        db.commit()
    except RuntimeError as err:
        print("runtime error: {0}".format(err))
        print(f"Light: {kwargs['light']}, Humidity: {kwargs['humidity']}, Temp: {kwargs['temp']}")

    cursor.close()
    db.close()


class DatabaseManager:
    def __init__(self):
        # Read Database connection variables
        load_dotenv("credentials.env")
        db_host = os.environ['MYSQL_HOST']
        db_user = os.environ['MYSQL_USER']
        db_pass = os.environ['MYSQL_PASSWORD']
        self.db_name = os.environ['MYSQL_DATABASE']

        # Connect to the db and create a cursor object
        self.db = mysql.connect(user=db_user, password=db_pass, host=db_host)
        self.cursor = self.db.cursor()
        self.table_name = "Weather"

        self.cursor.execute(f"CREATE DATABASE if not exists {self.db_name}")
        self.cursor.execute(f"USE {self.db_name}")

        self.cursor.execute(f"drop table if exists {self.table_name};")

        try:
            self.cursor.execute(f"""
                CREATE TABLE {self.table_name} (
                    item_id         INTEGER AUTO_INCREMENT PRIMARY KEY,
                    light           DECIMAL(10,2) NOT NULL,
                    humidity        DECIMAL(10,2) NOT NULL,
                    temperature     DECIMAL(10,2) NOT NULL
                );
            """)
        except RuntimeError as err:
            print("runtime error: {0}".format(err))

        self.fetchall()

    # Fetch all rows from menu and store into list
    # Return as JSON
    def fetchall(self):
        # execute the SELECT statement to fetch all rows from the table
        self.cursor.execute(f"SELECT * FROM {self.table_name};")
        self.table = self.cursor.fetchall() # store them in table

        # Convert to JSON
        self.table_JSON = []
        for row in self.table:
            self.table_JSON.append({"item_id": row[0], "light": float(str(row[1])), "humidity": float(str(row[2])), "temperature": float(str(row[2]))})

        return self.table_JSON

    def add(self, light: float, humidity: float, temp: float):
        try:
            query = f"INSERT INTO {self.table_name} (light, humidity, temperature) values (\"{light}\", \"{humidity}\", \"{temp}\");"
            self.cursor.execute(query)
            self.db.commit()
        except RuntimeError as err:
            print("runtime error: {0}".format(err))
            print(f"Light: {light}, Humidity: {humidity}, Temp: {temp}")

    def add_all(self, light_list, humidity_list, temp_list, debug=False):
        query = f"INSERT INTO {self.table_name}"
        query += "(light, humidity, temperature) VALUES (%s, %s, %s)"
        values = []
        if light_list and humidity_list and temp_list:
            for i in range(len(light_list)):
                values.append((light_list[i], round(humidity_list[i],2), round(temp_list[i],2)))
            
            print("Query:", query)
            print("Values:", values)
            try:
                self.cursor.executemany(query, values)
                self.db.commit()
            except RuntimeError as err:
                print("runtime error: {0}".format(err))
                print(f"Light: {light_list}, Humidity: {humidity_list}, Temp: {temp_list}")

            if debug:
                return self.fetchall()

    def exit(self):
        try:
            self.cursor.close()
            self.db.close()
        except RuntimeError as err:
            print("Cursor and DB has been closed before.")
        finally:
            print("Cursor and DB closed.")