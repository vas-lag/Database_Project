# -*- coding: utf-8 -*-
"""

@author: Billy
"""
import random
import datetime
import dateutil.relativedelta
import json
import sqlite3

def get_random_date(start, end):
    delta = end - start
    days_delta = random.randrange(delta.days)
    return start + datetime.timedelta(days=days_delta)

def connect_to_db(dbname):
    connection = sqlite3.connect(dbname + '.sqlite3')
    cursor = connection.cursor()
    return connection,cursor

def delete_all_data(cursor):
    cursor.execute('DELETE FROM THLEFWNO_ENDIAFEROMENOU;')
    cursor.execute('DELETE FROM THLEFWNO_ERGODOTH;')
    cursor.execute('DELETE FROM AFORA;')
    cursor.execute('DELETE FROM DIATHETEI;')
    cursor.execute('DELETE FROM PERILAMVANEI;')
    cursor.execute('DELETE FROM ANHKEI;')
    cursor.execute('DELETE FROM PROYPOTHETEI;')
    cursor.execute('DELETE FROM APAITEI;')
    cursor.execute('DELETE FROM PROIPIRESIA;')
    cursor.execute('DELETE FROM GNOSH;')
    cursor.execute('DELETE FROM PTYXIO;')
    cursor.execute('DELETE FROM PROSONTA;')
    cursor.execute('DELETE FROM AITHSH_ERGASIAS;')
    cursor.execute('DELETE FROM TOMEAS_ERGASIAS;')
    cursor.execute('DELETE FROM ENDIAFEROMENOS;')
    cursor.execute('DELETE FROM ERGODOTHS;')
    return

def create_tables(cursor):
    cursor.execute('''PRAGMA foreign_keys = ON;''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS ENDIAFEROMENOS(
    	kod_endiaferomenou INTEGER PRIMARY KEY,
    	onoma VARCHAR,
    	eponymo VARCHAR,
    	hlikia INTEGER,
    	fylo VARCHAR,
    	email VARCHAR UNIQUE,
        afm VARCHAR UNIQUE,
    	topos_katoikias VARCHAR,
    	dieyuynsh_katoikias VARCHAR,
    	CHECK(fylo IN('M','F'))
    );
              ''')
                         
    cursor.execute('''CREATE TABLE IF NOT EXISTS AITHSH_ERGASIAS (
    	kod_aithshs INTEGER PRIMARY KEY,
    	topos_endiaferontos VARCHAR,
    	hmeromhnia_aithshs DATE DEFAULT CURRENT_DATE,
    	hmeromhnia_lhxhs_aithshs DATE,
    	kod_endiaferomenou_aithshs INTEGER,
    	FOREIGN KEY(kod_endiaferomenou_aithshs) REFERENCES ENDIAFEROMENOS(kod_endiaferomenou) ON DELETE CASCADE
    );
              ''')          
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS TOMEAS_ERGASIAS(
    	onoma VARCHAR,
    	perigrafi TEXT,
    	PRIMARY KEY(onoma)
    )WITHOUT ROWID;
              ''')
              
    cursor.execute('''CREATE TABLE IF NOT EXISTS ERGODOTHS(
    	kod_ergodoth INTEGER PRIMARY KEY,
    	onoma VARCHAR,
    	eponymo VARCHAR,
    	fylo VARCHAR,
    	email VARCHAR,
        afm VARCHAR UNIQUE,
    	dieyuynsh VARCHAR,
    	CHECK(fylo IN('M','F'))
    );
              ''')
              
    cursor.execute('''CREATE TABLE IF NOT EXISTS THESI_ERGASIAS (
    	kod_theshs INTEGER PRIMARY KEY,
    	etairia VARCHAR,
    	topos VARCHAR,
    	misthos INTEGER,
    	perigrafi TEXT,
    	orario VARCHAR,
    	hmeromhnia_enarxhs DATE DEFAULT CURRENT_DATE,
    	hmeromhnia_lhxhs DATE,
    	ergodoths INTEGER,
    	FOREIGN KEY(ergodoths) REFERENCES ERGODOTHS(kod_ergodoth) ON DELETE CASCADE
    );
              ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS PROIPIRESIA(
        kod_proipiresias INTEGER PRIMARY KEY,
        etairia VARCHAR,
        posto VARCHAR,
        hmeromhnia_enarksis DATE,
        hmeromhnia_liksis DATE,
        diarkeia INTEGER,
        tomeas VARCHAR,
    	FOREIGN KEY(tomeas) REFERENCES TOMEAS_ERGASIAS(onoma)
    );
              ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS PROSONTA (
        kod_prosontos INTEGER PRIMARY KEY,
        perigrafi TEXT
    );
              ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS PTYXIO(
        kod_prosontos INTEGER,
        antikeimeno VARCHAR,
        vathmos FLOAT,
        eksidikeysi VARCHAR,
        etos_apoktisis DATE,
        foreas VARCHAR,
    	PRIMARY KEY(kod_prosontos, antikeimeno),
    	FOREIGN KEY(kod_prosontos) REFERENCES PROSONTA(kod_prosontos)
    )WITHOUT ROWID;
              ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS GNOSH (
        kod_prosontos INTEGER,
        antikeimeno VARCHAR,
        eparkia VARCHAR,
    	PRIMARY KEY(kod_prosontos,antikeimeno),
    	FOREIGN KEY(kod_prosontos) REFERENCES PROSONTA(kod_prosontos)
    )WITHOUT ROWID;
              ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS AFORA (
        aithsh INTEGER,
        tomeas VARCHAR,
    	PRIMARY KEY(aithsh, tomeas),
    	FOREIGN KEY(aithsh) REFERENCES AITHSH_ERGASIAS(kod_aithshs) ON DELETE CASCADE,
    	FOREIGN KEY(tomeas) REFERENCES TOMEAS_ERGASIAS(onoma)
    )WITHOUT ROWID;
              ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS DIATHETEI (
        aithsh INTEGER,
        kod_proipiresias INTEGER,
    	PRIMARY KEY(aithsh, kod_proipiresias),
    	FOREIGN KEY(aithsh) REFERENCES AITHSH_ERGASIAS(kod_aithshs) ON DELETE CASCADE,
    	FOREIGN KEY(kod_proipiresias) REFERENCES PROIPIRESIA(kod_proipiresias)
    )WITHOUT ROWID;
              ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS PERILAMVANEI (
        aithsh INTEGER,
        proson INTEGER,
    	PRIMARY KEY(aithsh, proson),
    	FOREIGN KEY(aithsh) REFERENCES AITHSH_ERGASIAS(kod_aithshs) ON DELETE CASCADE,
    	FOREIGN KEY(proson) REFERENCES PROSONTA(kod_prosontos)
    )WITHOUT ROWID;
              ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS ANHKEI (
        kod_ergasias INTEGER,
        tomeas VARCHAR,
    	PRIMARY KEY(kod_ergasias,tomeas),
    	FOREIGN KEY(kod_ergasias) REFERENCES THESI_ERGASIAS(kod_theshs) ON DELETE CASCADE,
    	FOREIGN KEY(tomeas) REFERENCES TOMEAS_ERGASIAS(onoma)
    )WITHOUT ROWID;
              ''')       
              
    cursor.execute('''CREATE TABLE IF NOT EXISTS PROYPOTHETEI (
        kod_ergasias INTEGER,
        kod_proipiresias INTEGER,
        aparaithth INTEGER DEFAULT 10,
    	PRIMARY KEY(kod_ergasias,kod_proipiresias),
    	FOREIGN KEY(kod_ergasias) REFERENCES THESI_ERGASIAS(kod_theshs) ON DELETE CASCADE,
    	FOREIGN KEY(kod_proipiresias) REFERENCES PROIPIRESIA(kod_proipiresias)
    )WITHOUT ROWID;
              ''')  
              
    cursor.execute('''CREATE TABLE IF NOT EXISTS APAITEI (
        kod_ergasias INTEGER,
        proson INTEGER,
        shmantikothta INTEGER,
    	PRIMARY KEY(kod_ergasias,proson),
    	FOREIGN KEY(kod_ergasias) REFERENCES THESI_ERGASIAS(kod_theshs) ON DELETE CASCADE,
    	FOREIGN KEY(proson) REFERENCES PROSONTA(kod_prosontos)
    )WITHOUT ROWID;
              ''')  
             
    cursor.execute('''CREATE TABLE IF NOT EXISTS THLEFWNO_ENDIAFEROMENOU (
        endiaferomenos INTEGER,
        thlefwno VARCHAR 
    	CHECK(length(thlefwno) >= 10),
    	PRIMARY KEY(endiaferomenos,thlefwno),
    	FOREIGN KEY(endiaferomenos) REFERENCES ENDIAFEROMENOS(kod_endiaferomenou) ON DELETE CASCADE
    )WITHOUT ROWID;
              ''')  
              
    cursor.execute('''CREATE TABLE IF NOT EXISTS THLEFWNO_ERGODOTH (
        ergodoths INTEGER,
        thlefwno VARCHAR
    	CHECK(length(thlefwno) >= 10),
    	PRIMARY KEY(ergodoths,thlefwno),
    	FOREIGN KEY(ergodoths) REFERENCES ERGODOTHS(kod_ergodoth) ON DELETE CASCADE
    )WITHOUT ROWID;
              ''')
    return




conn, c = connect_to_db('grafeioDB')
create_tables(c)
delete_all_data(c)

male_names = open('male-first-names-list.txt',encoding="utf8").read().splitlines()
female_names = open('female-first-names-list.txt',encoding="utf8").read().splitlines()
male_last_names = open('male-last-names-list.txt',encoding="utf8").read().splitlines()
female_last_names = open('female-last-names-list.txt',encoding="utf8").read().splitlines()
emails = open('email-list.txt',encoding="utf8").read().splitlines()
nomoi = open('nomoi-list.txt',encoding="utf8").read().splitlines()
addresses = open('addresses-list.txt',encoding="utf8").read().splitlines()
companies = open('Companies.txt',encoding="utf8").read().splitlines()
job_departments = open('Job_Departments.txt',encoding="utf8").read().splitlines()
universities_raw = open('Universities.txt',encoding="utf8").read()
universities = json.loads(universities_raw)
degrees_raw = open('Degrees.txt',encoding="utf8").read()
degrees = json.loads(degrees_raw)
knowledge = open('knowledge.txt',encoding="utf8").read().splitlines()
jobs = open('Job_Titles_dict.txt',encoding="utf8").read()
job_titles = json.loads(jobs)


for department in job_departments:
    c.execute('''INSERT INTO TOMEAS_ERGASIAS
    VALUES (?,NULL)''',(department,))

for i in range(200):
    sex = random.choice(['M','F'])
    if sex == 'M':
        myname = random.choice(male_names)
        mylastname = random.choice(male_last_names)  
    else:
        myname = random.choice(female_names)
        mylastname = random.choice(female_last_names)
    age = random.randint(18,65)
    myemail = random.choice(emails)
    #print(myemail)
    mynomos = random.choice(nomoi)
    myaddress = random.choice(addresses)
    emails.remove(myemail)
    myafm = random.randint(100000000,999999999)
    c.execute('''INSERT INTO ENDIAFEROMENOS
    VALUES (?,?,?,?,?,?,?,?,?)''',(i+1, myname, mylastname, age, sex, myemail, myafm, mynomos, myaddress))
    
    for _ in range(random.randint(1,2)):
        c.execute('''INSERT INTO THLEFWNO_ENDIAFEROMENOU
        VALUES (?,?)''', (i+1, str(69) + str(random.randint(10000000,99999999))))
    
    for _ in range(random.choice([1])):
        nomos = random.choice(nomoi)
        start_date = get_random_date(datetime.date(2020,1,1), datetime.date(2020,12,31))
        end_date = start_date + dateutil.relativedelta.relativedelta(years=+1)
        c.execute('''INSERT INTO AITHSH_ERGASIAS
        VALUES (NULL,?,?,?,?)''',(nomos, start_date, end_date, i+1))
        
        #add to afora
        departments_copy = job_departments.copy()
        for _ in range(random.randint(1,4)):
            department = random.choice(departments_copy)
            departments_copy.remove(department)
            c.execute('''INSERT INTO AFORA
            VALUES ((SELECT MAX(kod_aithshs)
            FROM AITHSH_ERGASIAS),?)''',(department,))
            
        #add to proipiresia
        many = random.randint(0,3)
        if age < 20:
            many = 0
        if age < 22 and many > 1:
            many = 1
        for j in range(many):
            department = random.choice(job_departments)
            company = random.choice(companies)
            job = random.choice(job_titles[department])
            delta = datetime.date(2018,12,31) - datetime.date(2020-age+18,1,1)
            days = round(delta.days/many)
            start_date = get_random_date(datetime.date(2020-age+18,1,1)+j*dateutil.relativedelta.relativedelta(days=+days), datetime.date(2020-age+18,1,1)+(j+1)*dateutil.relativedelta.relativedelta(days=+days))
            week = random.randint(5, (age-18)*54/many)
            end_date = start_date + dateutil.relativedelta.relativedelta(weeks=+week)
            duration = end_date.year - start_date.year
            c.execute('''INSERT INTO PROIPIRESIA
            VALUES (NULL,?,?,?,?,?,?)''',(company, job, start_date, end_date, duration, department))
            
            #add to diathetei
            c.execute('''INSERT INTO DIATHETEI
            VALUES ((SELECT MAX(kod_aithshs)
            FROM AITHSH_ERGASIAS),(SELECT MAX(kod_proipiresias)
            FROM PROIPIRESIA))''')
                                   
        #add to prosonta
        for j in range(random.randint(0,4)):
            c.execute('''INSERT INTO PROSONTA
            VALUES (NULL,NULL)''')
            #add to gnosh
            myknowledge = random.choice(knowledge)
            c.execute('''INSERT INTO GNOSH
            VALUES ((SELECT MAX(kod_prosontos)
            FROM PROSONTA),?,?)''',(myknowledge, random.randint(4,10)))
            #add to perilamvanei
            c.execute('''INSERT INTO PERILAMVANEI
            VALUES ((SELECT MAX(kod_aithshs)
            FROM AITHSH_ERGASIAS),(SELECT MAX(kod_prosontos)
            FROM PROSONTA))''')
                                   
        for j in range(random.randint(0,2)):
            c.execute('''INSERT INTO PROSONTA
            VALUES (NULL,NULL)''')
            #add to ptyxio
            uni = random.choice(universities[str(j+1)])
            degree = random.choice(degrees[uni])
            get_date = get_random_date(datetime.date(2020-age+21,1,1), datetime.date(2020-age+25,12,31))
            if j == 0:
                grade = random.randint(10,20) / 2
            else:
                grade = random.choice(['A','B','C'])
            c.execute('''INSERT INTO PTYXIO
            VALUES ((SELECT MAX(kod_prosontos)
            FROM PROSONTA),?,?,NULL,?,?)''',(degree, grade, get_date, uni))
            #add to perilamvanei
            c.execute('''INSERT INTO PERILAMVANEI
            VALUES ((SELECT MAX(kod_aithshs)
            FROM AITHSH_ERGASIAS),(SELECT MAX(kod_prosontos)
            FROM PROSONTA))''')
    
    


for i in range(30):
    sex = random.choice(['M','F'])
    if sex == 'M':
        myname = random.choice(male_names)
        mylastname = random.choice(male_last_names)  
    else:
        myname = random.choice(female_names)
        mylastname = random.choice(female_last_names)
    myemail = random.choice(emails)
    myaddress = random.choice(addresses)
    myafm = random.randint(100000000,999999999)
    
    emails.remove(myemail)
    c.execute('''INSERT INTO ERGODOTHS
    VALUES (NULL,?,?,?,?,?,?)''',(myname, mylastname, sex, myemail, myafm, myaddress))
    
    for _ in range(random.randint(1,2)):
        c.execute('''INSERT INTO THLEFWNO_ERGODOTH
        VALUES (?,?)''', (i+1, str(69) + str(random.randint(10000000,99999999))))
        
    for _ in range(random.randint(1,10)):
        company = random.choice(companies)
        nomos = random.choice(nomoi)
        start_date = get_random_date(datetime.date(2020,1,1), datetime.date(2020,12,31))
        end_date = start_date + dateutil.relativedelta.relativedelta(months=+6)
        hours = random.choice(["Πλήρης Απασχόληση", "Μερική Απασχόληση"])
        c.execute('''INSERT INTO THESI_ERGASIAS
        VALUES (NULL,?,?,?,NULL,?,?,?,?)''',(company, nomos, random.randint(5,40)*2000, hours, start_date, end_date, i+1))
        
        #add to anhkei
        department = random.choice(job_departments)
        c.execute('''INSERT INTO ANHKEI
        VALUES ((SELECT MAX(kod_theshs)
        FROM THESI_ERGASIAS),?)''',(department,))
         
        choice = random.choice([0,1])
        if choice == 1:
            #add to proipiresia
            duration = random.randint(1,5)
            department = random.choice(job_departments)
            c.execute('''INSERT INTO PROIPIRESIA
            VALUES (NULL,NULL,NULL,NULL,NULL,?,?)''',(duration, department))
            
            #add to proypothetei
            c.execute('''INSERT INTO PROYPOTHETEI
            VALUES ((SELECT MAX(kod_theshs)
            FROM THESI_ERGASIAS),(SELECT MAX(kod_proipiresias)
            FROM PROIPIRESIA),?)''',(1,))
                                   
        #add to prosonta
        for j in range(random.choice([0,0,1,1,2])):
            c.execute('''INSERT INTO PROSONTA
            VALUES (NULL,NULL)''')
            #add to gnosh
            myknowledge = random.choice(knowledge)
            c.execute('''INSERT INTO GNOSH
            VALUES ((SELECT MAX(kod_prosontos)
            FROM PROSONTA),?,?)''',(myknowledge, random.randint(4,10)))
            #add to apaitei
            c.execute('''INSERT INTO APAITEI
            VALUES ((SELECT MAX(kod_theshs)
            FROM THESI_ERGASIAS),(SELECT MAX(kod_prosontos)
            FROM PROSONTA),?)''',(random.randint(1,10),))
                                   
        for j in range(random.choice([0,0,0,1,1])):
            c.execute('''INSERT INTO PROSONTA
            VALUES (NULL,NULL)''')
            #add to ptyxio
            index= random.randint(1,2)
            uni = random.choice(universities[str(index)])
            degree = random.choice(degrees[uni])
            if index == 1:
                grade = random.randint(10,17) / 2
            else:
                grade = random.choice(['B','C'])
            #get_date = get_random_date(datetime.date(2020-age+21,1,1), datetime.date(2020-age+25,12,31))
            c.execute('''INSERT INTO PTYXIO
            VALUES ((SELECT MAX(kod_prosontos)
            FROM PROSONTA),?,?,NULL,NULL,NULL)''',(degree, grade))
            #add to perilamvanei
            c.execute('''INSERT INTO APAITEI
            VALUES ((SELECT MAX(kod_theshs)
            FROM THESI_ERGASIAS),(SELECT MAX(kod_prosontos)
            FROM PROSONTA),?)''',(random.randint(1,10),))


conn.commit()
conn.close()