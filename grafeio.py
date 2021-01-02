# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 16:51:29 2020

@author: Billy
"""
import random
import datetime
import dateutil.relativedelta
import sqlite3

def get_random_date(start, end):
    delta = end - start
    days_delta = random.randrange(delta.days)
    return start + datetime.timedelta(days=days_delta)

conn = sqlite3.connect('grafeio.sqlite3')
c = conn.cursor()

c.execute('''PRAGMA foreign_keys = ON;''')

c.execute('''CREATE TABLE IF NOT EXISTS ENDIAFEROMENOS(
	kod_endiaferomenou INTEGER PRIMARY KEY,
	onoma VARCHAR,
	eponymo VARCHAR,
	hlikia INTEGER,
	fylo VARCHAR,
	email VARCHAR UNIQUE,
	topos_katoikias VARCHAR,
	dieyuynsh_katoikias VARCHAR,
	CHECK(fyllo IN('M','F','O'))
);
          ''')
          
          
c.execute('''CREATE TABLE IF NOT EXISTS AITHSH_ERGASIAS (
	kod_aithshs INTEGER PRIMARY KEY,
	topos_endiaferontos VARCHAR,
	hmeromhnia_aithshs DATE DEFAULT CURRENT_DATE,
	hmeromhnia_lhxhs_aithshs DATE,
	kod_endiaferomenou_aithshs VARCHAR,
	FOREIGN KEY(kod_endiaferomenou_aithshs) REFERENCES ENDIAFEROMENOS(kod_endiaferomenou) ON DELETE CASCADE
);
          ''')          

c.execute('''CREATE TABLE IF NOT EXISTS TOMEAS_ERGASIAS(
	onoma VARCHAR,
	perigrafi TEXT,
	PRIMARY KEY(onoma)
)WITHOUT ROWID;
          ''')
          
c.execute('''CREATE TABLE IF NOT EXISTS ERGODOTHS(
	kod_ergodoth INTEGER PRIMARY KEY,
	onoma VARCHAR,
	eponymo VARCHAR,
	fylo VARCHAR,
	email VARCHAR,
	dieyuynsh VARCHAR,
	CHECK(fyllo IN('M','F','O'))
);
          ''')
          
c.execute('''CREATE TABLE IF NOT EXISTS THESI_ERGASIAS (
	kod_theshs INTEGER PRIMARY KEY,
	etairia VARCHAR,
	topos VARCHAR,
	misthos INTEGER,
	perigrafi TEXT,
	orario VARCHAR,
	hmeromhnia_enarxhs DATE DEFAULT CURRENT_DATE,
	hmeromhnia_lhxhs DATE,
	ergodoths VARCHAR,
	FOREIGN KEY(ergodoths) REFERENCES ERGODOTHS(kod_ergodoth) ON DELETE CASCADE
);
          ''')

c.execute('''CREATE TABLE IF NOT EXISTS PROIPIRESIA(
    kod_proipiresias INTEGER PRIMARY KEY,
    etairia VARCHAR,
    posto VARCHAR,
    hmeromhnia_enarksis DATE,
    hmeromhnia_liksis DATE,
    tomeas VARCHAR,
	FOREIGN KEY(tomeas) REFERENCES TOMEAS_ERGASIAS(onoma)
);
          ''')

c.execute('''CREATE TABLE IF NOT EXISTS PROSONTA (
    kod_prosontos INTEGER PRIMARY KEY,
    perigrafi TEXT
);
          ''')

c.execute('''CREATE TABLE IF NOT EXISTS PTYXIO(
    kod_prosontos VARCHAR,
    antikeimeno VARCHAR,
    vathmos FLOAT,
    eksidikeysi VARCHAR,
    etos_apoktisis DATE,
    foreas VARCHAR,
	PRIMARY KEY(kod_prosontos, antikeimeno),
	FOREIGN KEY(kod_prosontos) REFERENCES PROSONTA(kod_prosontos)
)WITHOUT ROWID;
          ''')

c.execute('''CREATE TABLE IF NOT EXISTS GNOSH (
    kod_prosontos VARCHAR,
    antikeimeno VARCHAR,
    eparkia VARCHAR,
	PRIMARY KEY(kod_prosontos,antikeimeno),
	FOREIGN KEY(kod_prosontos) REFERENCES PROSONTA(kod_prosontos)
)WITHOUT ROWID;
          ''')

c.execute('''CREATE TABLE IF NOT EXISTS AFORA (
    aithsh VARCHAR,
    tomeas_ergasias VARCHAR,
	PRIMARY KEY(aithsh, tomeas_ergasias),
	FOREIGN KEY(aithsh) REFERENCES AITHSH_ERGASIAS(kod_aithshs) ON DELETE CASCADE,
	FOREIGN KEY(tomeas_ergasias) REFERENCES TOMEAS_ERGASIAS(onoma)
)WITHOUT ROWID;
          ''')

c.execute('''CREATE TABLE IF NOT EXISTS DIATHETEI (
    aithsh VARCHAR,
    proipiresia VARCHAR,
	PRIMARY KEY(aithsh, proipiresia),
	FOREIGN KEY(aithsh) REFERENCES AITHSH_ERGASIAS(kod_aithshs) ON DELETE CASCADE,
	FOREIGN KEY(proipiresia) REFERENCES PROIPIRESIA(kod_proipiresias)
)WITHOUT ROWID;
          ''')

c.execute('''CREATE TABLE IF NOT EXISTS PERILAMVANEI (
    aithsh VARCHAR,
    proson VARCHAR,
	PRIMARY KEY(aithsh, proson),
	FOREIGN KEY(aithsh) REFERENCES AITHSH_ERGASIAS(kod_aithshs) ON DELETE CASCADE,
	FOREIGN KEY(proson) REFERENCES PROSONTA(kod_prosontos)
)WITHOUT ROWID;
          ''')

c.execute('''CREATE TABLE IF NOT EXISTS ANHKEI (
    thesi_ergasias VARCHAR,
    tomeas_ergasias VARCHAR,
	PRIMARY KEY(thesi_ergasias,tomeas_ergasias),
	FOREIGN KEY(thesi_ergasias) REFERENCES THESI_ERGASIAS(kod_theshs) ON DELETE CASCADE,
	FOREIGN KEY(tomeas_ergasias) REFERENCES TOMEAS_ERGASIAS(onoma)
)WITHOUT ROWID;
          ''')       
          
c.execute('''CREATE TABLE IF NOT EXISTS PROYPOTHETEI (
    thesi_ergasias VARCHAR,
    proipiresia VARCHAR,
    aparaithth INTEGER DEFAULT 10,
	PRIMARY KEY(thesi_ergasias,proipiresia),
	FOREIGN KEY(thesi_ergasias) REFERENCES THESI_ERGASIAS(kod_theshs) ON DELETE CASCADE,
	FOREIGN KEY(proipiresia) REFERENCES PROIPIRESIA(kod_proipiresias)
)WITHOUT ROWID;
          ''')  
          
c.execute('''CREATE TABLE IF NOT EXISTS APAITEI (
    thesi_ergasias VARCHAR,
    proson VARCHAR,
    shmantikothta INTEGER,
	PRIMARY KEY(thesi_ergasias,proson),
	FOREIGN KEY(thesi_ergasias) REFERENCES THESI_ERGASIAS(kod_theshs) ON DELETE CASCADE,
	FOREIGN KEY(proson) REFERENCES PROSONTA(kod_prosontos)
)WITHOUT ROWID;
          ''')  
         
c.execute('''CREATE TABLE IF NOT EXISTS THLEFWNO_ENDIAFEROMENOU (
    endiaferomenos VARCHAR,
    thlefwno VARCHAR 
	CHECK(length(thlefwno) >= 10),
	PRIMARY KEY(endiaferomenos,thlefwno),
	FOREIGN KEY(endiaferomenos) REFERENCES ENDIAFEROMENOS(kod_endiaferomenou) ON DELETE CASCADE
)WITHOUT ROWID;
          ''')  
          
c.execute('''CREATE TABLE IF NOT EXISTS THLEFWNO_ERGODOTH (
    ergodoths VARCHAR,
    thlefwno VARCHAR
	CHECK(length(thlefwno) >= 10),
	PRIMARY KEY(ergodoths,thlefwno),
	FOREIGN KEY(ergodoths) REFERENCES ERGODOTHS(kod_ergodoth) ON DELETE CASCADE
)WITHOUT ROWID;
          ''')  


### insert people into tables
c.execute('DELETE FROM AFORA;')
c.execute('DELETE FROM DIATHETEI;')
c.execute('DELETE FROM PROIPIRESIA;')
c.execute('DELETE FROM AITHSH_ERGASIAS;')
c.execute('DELETE FROM TOMEAS_ERGASIAS;')
c.execute('DELETE FROM ENDIAFEROMENOS;')
c.execute('DELETE FROM ERGODOTHS;')

male_names = open('male-first-names-list.txt',encoding="utf8").read().splitlines()
female_names = open('female-first-names-list.txt',encoding="utf8").read().splitlines()
male_last_names = open('male-last-names-list.txt',encoding="utf8").read().splitlines()
female_last_names = open('female-last-names-list.txt',encoding="utf8").read().splitlines()
emails = open('email-list.txt',encoding="utf8").read().splitlines()
nomoi = open('nomoi-list.txt',encoding="utf8").read().splitlines()
addresses = open('addresses-list.txt',encoding="utf8").read().splitlines()
companies = open('Companies.txt',encoding="utf8").read().splitlines()
degrees = open('Degrees.txt',encoding="utf8").read().splitlines()
job_departments = open('Job_Departments.txt',encoding="utf8").read().splitlines()
job_titles = open('Job_Titles.txt',encoding="utf8").read().splitlines()
universities = open('Universities.txt',encoding="utf8").read().splitlines()

for department in job_departments:
    c.execute('''INSERT INTO TOMEAS_ERGASIAS
    VALUES (?,NULL)''',(department,))

for i in range(100):
    sex = random.choice(['M','F'])
    if sex == 'M':
        myname = random.choice(male_names)
        mylastname = random.choice(male_last_names)  
    else:
        myname = random.choice(female_names)
        mylastname = random.choice(female_last_names)
    age = random.randint(18,65)
    myemail = random.choice(emails)
    mynomos = random.choice(nomoi)
    myaddress = random.choice(addresses)
      
    emails.remove(myemail)
    c.execute('''INSERT INTO ENDIAFEROMENOS
    VALUES (?,?,?,?,?,?,?,?)''',(i+1, myname, mylastname, age, sex, myemail, mynomos, myaddress))
    
    for _ in range(random.choice([1,1,1,1,1,1,1,2])):
        nomos = random.choice(nomoi)
        start_date = get_random_date(datetime.date(2020,1,1), datetime.date(2020,12,31))
        end_date = start_date + dateutil.relativedelta.relativedelta(years=+1)
        c.execute('''INSERT INTO AITHSH_ERGASIAS
        VALUES (NULL,?,?,?,?)''',(nomos, start_date, end_date, i+1))
        
        #add to afora
        departments_copy = job_departments.copy()
        for _ in range(random.randint(1,3)):
            department = random.choice(departments_copy)
            departments_copy.remove(department)
            c.execute('''INSERT INTO AFORA
            VALUES ((SELECT MAX(kod_aithshs)
            FROM AITHSH_ERGASIAS),?)''',(department,))
            
        #add to proipiresia
        job_copy = job_titles.copy()
        many = random.randint(0,3)
        if age < 20:
            many = 0
        if age < 22 and many > 1:
            many = 1
        for j in range(many):
            company = random.choice(companies)
            job = random.choice(job_copy)
            job_copy.remove(job)
            delta = datetime.date(2018,12,31) - datetime.date(2020-age+18,1,1)
            days = round(delta.days/many)
            start_date = get_random_date(datetime.date(2020-age+18,1,1)+j*dateutil.relativedelta.relativedelta(days=+days), datetime.date(2020-age+18,1,1)+(j+1)*dateutil.relativedelta.relativedelta(days=+days))
            week = random.randint(5, (age-18)*54/many)
            end_date = start_date + dateutil.relativedelta.relativedelta(weeks=+week)
            department = random.choice(job_departments)
            c.execute('''INSERT INTO PROIPIRESIA
            VALUES (NULL,?,?,?,?,?)''',(company, job, start_date, end_date, department))
            
            #add to diathetei
            c.execute('''INSERT INTO DIATHETEI
            VALUES ((SELECT MAX(kod_aithshs)
            FROM AITHSH_ERGASIAS),(SELECT MAX(kod_proipiresias)
            FROM PROIPIRESIA))''')
    
    


for i in range(20):
    sex = random.choice(['M','F'])
    if sex == 'M':
        myname = random.choice(male_names)
        mylastname = random.choice(male_last_names)  
    else:
        myname = random.choice(female_names)
        mylastname = random.choice(female_last_names)
    myemail = random.choice(emails)
    myaddress = random.choice(addresses)
      
    emails.remove(myemail)
    c.execute('''INSERT INTO ERGODOTHS
    VALUES (NULL,?,?,?,?,?)''',(myname, mylastname, sex, myemail, myaddress))



conn.commit()
conn.close()

    
