# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 16:51:29 2020

@author: Billy
"""
import sqlite3
conn = sqlite3.connect('grafeio.sqlite3')
c = conn.cursor()

c.execute('''PRAGMA foreign_keys = ON;''')

c.execute('''CREATE TABLE IF NOT EXISTS ENDIAFEROMENOS(
	kod_endiaferomenou INTEGER PRIMARY KEY,
	onoma VARCHAR,
	eponymo VARCHAR,
	hlikia INTEGER,
	fyllo VARCHAR,
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
	fyllo VARCHAR,
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



conn.commit()
conn.close()