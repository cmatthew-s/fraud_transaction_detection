
import sqlite3
import json
import pandas as pd
import csv
import lxml
from os.path import exists
from js import alert, document, console

class Data():

    def check_file(self, database):
        if exists(database):
            return True
        else: 
            return False

    def connect_data(self, database):
        try:
            self.con = sqlite3.connect(database)
            self.cursor = self.con.cursor()
        except Exception as e:
            alert('Connection Error: ', e)

    def check_user(self, data):
        statement = f"SELECT email from employees WHERE email = '{data['email']}' AND password = '{data['password']}' AND role = '{data['role']}';"
        self.cursor.execute(statement)

        if not self.cursor.fetchone():
            return False
        else:
            return True

    def get_login_info(self, database, user_data):
        if self.check_file(database):
            self.connect_data(database)
            if self.check_user(user_data):
                return True

        return False

    def load_json(self, path):
        f = open(path)
        data = json.load(f)
        return data

    def load_csv(self, path):
        with open(path, 'r') as f:
            content = csv.reader(f)
            return content

    def read_all_text(self, path):
        file = open(path, 'r')
        content = file.read()
        file.close()
        return content

    def write_csv(self, path, row):
        with open(path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def html_to_csv(self, rows):
        csv_data = []
        
        for i in range(0, len(rows)):
            cols = rows[i].querySelectorAll('td,th')

            csvrow = []
            for j in range(0, len(cols)):
                csvrow.append(cols[j].innerHTML)

            csv_data.append(','.join(csvrow))
        
        csv_data = '\n'.join(csv_data)

        self.write_csv('manual_result.csv', csv_data)
        console.log(csv_data)


        

       

