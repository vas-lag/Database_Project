# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 21:41:29 2021

@author: Billy
"""


import sqlite3
import tabulate as tab
from datetime import datetime
     
def connect_to_db(dbname):
    connection = sqlite3.connect(dbname + '.sqlite3')
    cursor = connection.cursor()
    return connection,cursor

def display_data(cursor,rows):
    columns = [i[0] for i in cursor.description]
    print(tab.tabulate(rows, headers = columns, tablefmt='psql'))
    
def print_info():
    print("---  ΓΡΑΦΕΙΟ ΕΥΡΕΣΗΣ ΕΡΓΑΣΙΑΣ SIMPLE API  ---")
    print("-- 1. Να βρεθούν όλες οι θέσεις εργασίας στον Νομό Χ από την εταιρία Υ")
    print("-- 2. Να βρεθεί ο μέσος μισθός για τις θέσεις εργασίας που έχουν να κάνουν με τον τομέα Χ στον Νομό Υ")
    print("-- 3. Να βρεθεί η περιοχή(ές) με την μεγαλύτερη ζήτηση εργασίας ")
    print("-- 4. Να βρεθούν τα ονόματα και τα τηλέφωνα των ενδιαφερόμενων που κατέχουν πτυχίο X και έχουν δηλώσει τόπο ενδιαφέροντος τον Νομό Y")
    print("-- 5. Να βρεθει ο μεσος μισθός για όλες τις θέσεις εργασιας ανά περιοχή και να γίνει φθίνουσα ταξινόμηση")
    print("-- 6. Να βρεθούν οι ενδιαφερόμενοι που που δεν έχει λήξει η αίτηση τους στον Νομό Χ")
    print("-- 7. Να βρεθούν οι ενδιαφερόμενοι που έχουν προϋπηρεσία στο πόστο Χ και έχουν γνώση Υ")
    print("-- 11. Εισαγωγή νέας αίτησης εργασίας")
    print("-- 12. Εισαγωγή νέας θέσης εργασίας")
    
def option1(cursor):
    topos_raw = input("Εισάγετε τον νομό ενδιαφέρονοτος: ")
    etairia_raw = input("Εισάγεται την εταιρία ενδιαφέροντος: ")
    topos = '%'+topos_raw+'%'
    etairia = '%'+etairia_raw+'%'
    rows = cursor.execute('''SELECT *
    FROM THESI_ERGASIAS
    WHERE topos LIKE ? 
    AND etairia LIKE ?
    ''',(topos,etairia))
    display_data(cursor,rows)

def option2(cursor):
    tomeas_raw = input("Εισάγεται τον τομέα ενδιαφέροντος: ")
    nomos_raw = input("Εισάγετε τον νομό ενδιαφέρονοτος: ")
    tomeas = '%'+tomeas_raw+'%'
    nomos = '%'+nomos_raw+'%'
    rows = cursor.execute('''SELECT CAST(AVG(misthos) AS INT) AS AVG_MISTHOS
    FROM THESI_ERGASIAS t JOIN ANHKEI a
    ON t.kod_theshs = a.kod_ergasias 
    WHERE 	a.tomeas LIKE ?
    AND t.topos LIKE ?
    ''',(tomeas,nomos))
    display_data(cursor,rows)

def option3(cursor):
    rows = cursor.execute('''SELECT topos_endiaferontos AS νομός_με_μεγαλύτερη_ζήτηση
    FROM aithsh_ergasias
    GROUP BY topos_endiaferontos
    HAVING COUNT(*) = (
                   SELECT MAX(Cnt) 
                   FROM(
                         SELECT COUNT(*) as Cnt
                         FROM aithsh_ergasias
                         GROUP BY topos_endiaferontos
                        ) tmp
                    )
    ''')
    display_data(cursor,rows)

def option4(cursor):
    ptyxio_raw = input("Εισάγεται το πτυχίο ενδιαφέροντος: ")
    nomos_raw = input("Εισάγετε τον νομό ενδιαφέρονοτος: ")
    ptyxio = '%'+ptyxio_raw+'%'
    nomos = '%'+nomos_raw+'%'
    rows = cursor.execute('''SELECT onoma,eponymo,email,thlefwno
    FROM ((((ENDIAFEROMENOS e JOIN AITHSH_ERGASIAS a
    ON e.kod_endiaferomenou = a.kod_endiaferomenou_aithshs) JOIN PERILAMVANEI pe
    ON a.kod_aithshs = pe.aithsh) JOIN PROSONTA pr
    ON pe.proson = pr.kod_prosontos) JOIN PTYXIO pt
    ON pr.kod_prosontos = pt.kod_prosontos) JOIN THLEFWNO_ENDIAFEROMENOU t
    ON e.kod_endiaferomenou = t.endiaferomenos
    WHERE a.topos_endiaferontos LIKE ?
    AND pt.antikeimeno LIKE ?''', (nomos,ptyxio))
    display_data(cursor,rows)

def option5(cursor):
    rows = cursor.execute('''SELECT topos,CAST(AVG(misthos) AS INT) AS AVG_MISTHOS
    FROM THESI_ERGASIAS
    GROUP BY topos 
    ORDER BY AVG(misthos) DESC''')
    display_data(cursor,rows)

def option6(cursor):
    nomos_raw = input("Εισάγετε τον τόπο ενδιαφέρονοτος: ")
    nomos = '%'+nomos_raw+'%'
    rows = cursor.execute('''SELECT endiaferomenos.*
    FROM endiaferomenos, aithsh_ergasias
    WHERE endiaferomenos.kod_endiaferomenou = aithsh_ergasias.kod_endiaferomenou_aithshs
        AND aithsh_ergasias.topos_endiaferontos LIKE ?
        AND date('now')<aithsh_ergasias.hmeromhnia_lhxhs_aithshs''',(nomos,))
    display_data(cursor,rows)

def option7(cursor):
    posto_raw = input("Εισάγετε το πόστο ενδιαφέροντος: ")
    gnosh_raw = input("Εισάγετε την επιθυμητή γνώση: ")
    posto = '%'+posto_raw+'%'
    gnosh = '%'+gnosh_raw+'%'
    rows = cursor.execute('''SELECT distinct endiaferomenos.*
    FROM endiaferomenos,aithsh_ergasias,diathetei,proipiresia,perilamvanei,gnosh
    WHERE endiaferomenos.kod_endiaferomenou = aithsh_ergasias.kod_endiaferomenou_aithshs
	AND aithsh_ergasias.kod_aithshs = diathetei.aithsh
	AND diathetei.kod_proipiresias = proipiresia.kod_proipiresias
	AND aithsh_ergasias.kod_aithshs = perilamvanei.aithsh
	AND perilamvanei.proson = gnosh.kod_prosontos
	AND proipiresia.posto LIKE ?
	AND gnosh.antikeimeno LIKE ?''',(posto,gnosh))
    display_data(cursor,rows)

def option11(cursor):
    choice = input("Ο ενδιαφερόμενος της αίτησης έχει υποβάλει ξανά στην εταιρία μας; \n(εισάγετε 'ναι' ή 'οχι'): ")
    if (choice == 'οχι'):      
        name = input("Όνομα: ")
        last_name = input("Επίθετο: ")
        age = input("Ηλικία: ")
        sex = input("Φύλο: ")
        email = input("Email: ")
        nomos = input("Τόπος κατοικίας: ")
        address = input("Διεύθυνση κατοικίας: ")
        cursor.execute('''INSERT INTO endiaferomenos
        VALUES (NULL,?,?,?,?,?,?,?)''',(name,last_name,age,sex,email, nomos, address))
        phone_num = input("Κινητό τηλέφωνο: ")
        row = cursor.execute('''SELECT kod_endiaferomenou
        FROM endiaferomenos
        WHERE email LIKE ?''',(email,))
        kod_endiaf = cursor.fetchone()[0]
        cursor.execute('''INSERT INTO thlefwno_endiaferomenou
        VALUES (?,?)''', (kod_endiaf, phone_num))      
    elif (choice == 'ναι'):
        raw_email = input("Εισάγετε το email του ενδιαφερόμενου: ")
        email = '%'+raw_email+'%'  
        row = cursor.execute('''SELECT kod_endiaferomenou
            FROM endiaferomenos
            WHERE email LIKE ?''',(email,))
        kod_endiaf = cursor.fetchone()[0]
    else:
        return
    
    nomos = input("Εισάγετε τόπο ενδιαφέροντος: ")
    start_str = input("Εισαγετε ημερομηνία υποβολής αίτησης: ")
    start_date = datetime.strptime(start_str,'%d-%m-%Y').date()
    end_str = input("Εισάγετε ημερομηνία λήξης αίτησης: ")
    end_date = datetime.strptime(end_str,'%d-%m-%Y').date()  
    cursor.execute('''INSERT INTO AITHSH_ERGASIAS
    VALUES (NULL,?,?,?,?)''',(nomos,start_date,end_date,kod_endiaf))
    row = cursor.execute('''SELECT MAX(kod_aithshs)
    FROM aithsh_ergasias''')
    kod_aithshs = cursor.fetchone()[0]

    #check for tomea/proipiresia/prosonta
    afora_ch = input("Η αίτηση αφορά γνωστό Τομέα Εργασίας; \n(εισάγετε 'ναι' ή 'οχι'): ")
    if (afora_ch == 'ναι'):
        tomeas = input("Εισάγετε το όνομα του τομέα: ")      
        cursor.execute('''INSERT INTO afora
        VALUES (?,?)''',(kod_aithshs,tomeas))
    proip_ch = input("Ο ενδιαφερόμενος διαθέτει συγκεκριμένη προϋπηρεσία για την αίτηση αυτή; \n(εισάγετε 'ναι' ή 'όχι': ")
    if (proip_ch == 'ναι'):
        etairia = input("Εταιρία: ")
        posto = input("Πόστο: ")
        start_str = input("Ημερομηνία έναρξης: ")
        start_date = datetime.strptime(start_str,'%d-%m-%Y').date()
        end_str = input("Ημερομηνία λήξης: ")
        end_date = datetime.strptime(end_str,'%d-%m-%Y').date()       
        duration = end_date.year - start_date.year
        tomeas_ch = input("Η προϋπηρεσία αυτή ανήκει σε κάποιον γνωστό τομέα εργασίας; \n(εισάγετε 'ναι ή 'οχι': ")
        if (tomeas_ch=='ναι'):
            tomeas = input("Εισάγετε τομέα: ")
            cursor.execute('''INSERT INTO proipiresia
            VALUES (NULL,?,?,?,?,?,?)''',(etairia,posto,start_date,end_date,duration,tomeas))
        else:
            cursor.execute('''INSERT INTO proipiresia
            VALUES (NULL,?,?,?,?,?,?)''',(etairia,posto,start_date,end_date,duration,""))
        row = cursor.execute('''SELECT MAX(kod_proipiresias)
        FROM proipiresia''')
        kod_proip = cursor.fetchone()[0]
        cursor.execute('''INSERT INTO diathetei
        VALUES (?,?)''', (kod_aithshs,kod_proip))
    proson_ch = input("Ο ενδιαφερόμενος κατέχει προσόντα για την αίτηση αυτή (πτυχίο/γνώσεις); \n(εισάγετε 'ναι' ή 'οχι'): ")
    if (proson_ch=='ναι'):
        ptyxio_ch = input("Κατέχει κάποιο πιστοποιημένο πτυχίο; \n(εισάγετε 'ναι' ή 'οχι'): ")
        if (ptyxio_ch=='ναι'):
            row = cursor.execute('''SELECT MAX(kod_prosontos)
            FROM prosonta''')
            kod_prosontos = cursor.fetchone()[0] + 1
            antikeimeno = input("Αντικείμενο: ")
            vathmos = input("Βαθμός: ")
            eksidikeysi = input("Εξειδίκευση: ")
            etos = input("Έτος απόκτησης: ")
            foreas = input("Φορέας: ")
            cursor.execute('''INSERT INTO prosonta VALUES (?,?)''',(kod_prosontos,""))
            cursor.execute('''INSERT INTO perilamvanei VALUES (?,?)''',(kod_aithshs,kod_prosontos))
            cursor.execute('''INSERT INTO ptyxio
            VALUES (?,?,?,?,?,?)''',(kod_prosontos,antikeimeno,vathmos,eksidikeysi,etos,foreas))
        gnoseis_ch = input("Κατέχει γνώσεις που θέλει να δηλώσει; \n(εισάγετε 'ναι' ή 'οχι'): ")
        if (gnoseis_ch =='ναι'):
            row = cursor.execute('''SELECT MAX(kod_prosontos)
            FROM prosonta''')
            kod_prosontos = cursor.fetchone()[0] + 1
            antikeimeno = input("Αντικείμενο: ")
            eparkia = input("Επάρκεια (0-10): ")
            cursor.execute('''INSERT INTO prosonta VALUES (?,?)''',(kod_prosontos,""))
            cursor.execute('''INSERT INTO gnosh
            VALUES (?,?,?)''',(kod_prosontos,antikeimeno,eparkia))


def option12(cursor):
    choice = input("Ο εργοδότης έχει υποβάλει ξανά θέση εργασίας στην εταιρία μας; \n(εισάγετε 'ναι' ή 'οχι'): ")
    if (choice == 'οχι'):      
        name = input("Όνομα: ")
        last_name = input("Επίθετο: ")
        sex = input("Φύλο: ")
        email = input("Email: ")
        address = input("Διεύθυνση κατοικίας: ")
        cursor.execute('''INSERT INTO ergodoths
        VALUES (NULL,?,?,?,?,?)''',(name,last_name,sex,email,address))
        phone_num = input("Κινητό τηλέφωνο: ")
        row = cursor.execute('''SELECT kod_ergodoth
        FROM ergodoths
        WHERE email LIKE ?''',(email,))
        kod_ergodoth = cursor.fetchone()[0]
        cursor.execute('''INSERT INTO thlefwno_ergodoth
        VALUES (?,?)''', (kod_ergodoth, phone_num))      
    elif (choice == 'ναι'):
        raw_email = input("Εισάγετε το email του εργοδότη: ")
        email = '%'+raw_email+'%'  
        row = cursor.execute('''SELECT kod_ergodoth
            FROM ergodoths
            WHERE email LIKE ?''',(email,))
        kod_ergodoth = cursor.fetchone()[0]
    else:
        return

    etairia = input("Εισάγετε εταιρία: ")
    nomos = input("Εισάγετε τόπο ενδιαφέροντος: ")
    misthos = input("Εισάγετε ενδεικτικό μισθό: ")
    perigrafh = input("Εισάγετε περιγραφή: ")
    orario = input("'Πλήρης Απασχόληση' ή 'Μερική Απασχόληση':")
    start_str = input("Εισαγετε ημερομηνία υποβολής της διαθέσιμης θέσης: ")
    start_date = datetime.strptime(start_str,'%d-%m-%Y').date()
    end_str = input("Εισάγετε ημερομηνία λήξης της διαθέσιμης θέσης: ")
    end_date = datetime.strptime(end_str,'%d-%m-%Y').date() 
    cursor.execute('''INSERT INTO THESI_ERGASIAS
    VALUES (NULL,?,?,?,?,?,?,?,?)''',(etairia,nomos,misthos,perigrafh,orario,start_date,end_date,kod_ergodoth))
    row = cursor.execute('''SELECT MAX(kod_theshs)
    FROM thesi_ergasias''')
    kod_theshs = cursor.fetchone()[0]

    #check for tomea/proipiresia/prosonta
    afora_ch = input("Η θέση αφορά γνωστό Τομέα Εργασίας; \n(εισάγετε 'ναι' ή 'οχι'): ")
    if (afora_ch == 'ναι'):
        tomeas = input("Εισάγετε το όνομα του τομέα: ")      
        cursor.execute('''INSERT INTO anhkei
        VALUES (?,?)''',(kod_theshs,tomeas))
    proip_ch = input("Ο εργοδότης απαιτεί συγκεκριμένη προϋπηρεσία για την θέση αυτή; \n(εισάγετε 'ναι' ή 'όχι': ")
    if (proip_ch == 'ναι'):
        etairia = input("Εταιρία: ")
        posto = input("Πόστο: ")
        duration = input("Ελάχιστα χρόνια σε αυτό το πόστο: ")
        aparaithth = input("Πόσο απαραίτητη είναι αυτή η προϋπηρεσία (1-10); ")
        tomeas_ch = input("Η προϋπηρεσία αυτή ανήκει σε κάποιον γνωστό τομέα εργασίας; \n(εισάγετε 'ναι ή 'οχι': ")
        if (tomeas_ch=='ναι'):
            tomeas = input("Εισάγετε τομέα: ")
            cursor.execute('''INSERT INTO proipiresia
            VALUES (NULL,?,?,?,?,?,?)''',(etairia,posto,"","",duration,tomeas))
        else:
            cursor.execute('''INSERT INTO proipiresia
            VALUES (NULL,?,?,?,?,?,?)''',(etairia,posto,start_date,end_date,duration,""))
        row = cursor.execute('''SELECT MAX(kod_proipiresias)
        FROM proipiresia''')
        kod_proip = cursor.fetchone()[0]
        cursor.execute('''INSERT INTO proypothetei
        VALUES (?,?,?)''', (kod_theshs,kod_proip,aparaithth))
    proson_ch = input("Ο εργοδότης απαιτεί προσόντα για την θέση αυτή (πτυχίο/γνώσεις); \n(εισάγετε 'ναι' ή 'οχι'): ")
    if (proson_ch=='ναι'):
        ptyxio_ch = input("Απαιτείται κάποιο πιστοποιημένο πτυχίο; \n(εισάγετε 'ναι' ή 'οχι'): ")
        if (ptyxio_ch=='ναι'):
            row = cursor.execute('''SELECT MAX(kod_prosontos)
            FROM prosonta''')
            kod_prosontos = cursor.fetchone()[0] + 1
            antikeimeno = input("Αντικείμενο: ")
            vathmos = input("Βαθμός: ")
            eksidikeysi = input("Εξειδίκευση: ")
            etos = input("Έτος απόκτησης: ")
            foreas = input("Φορέας: ")
            shmantikothta = input("Σημαντικότητα (1-10): ") 
            cursor.execute('''INSERT INTO prosonta VALUES (?,?)''',(kod_prosontos,""))
            cursor.execute('''INSERT INTO apaitei VALUES (?,?,?)''',(kod_theshs,kod_prosontos,shmantikothta))
            cursor.execute('''INSERT INTO ptyxio 
            VALUES (?,?,?,?,?,?)''',(kod_prosontos,antikeimeno,vathmos,eksidikeysi,etos,foreas))
        gnoseis_ch = input("Απαιτούνται γενικότερες γνώσεις; \n(εισάγετε 'ναι' ή 'οχι'): ")
        if (gnoseis_ch =='ναι'):
            row = cursor.execute('''SELECT MAX(kod_prosontos)
            FROM prosonta''')
            kod_prosontos = cursor.fetchone()[0] + 1
            antikeimeno = input("Αντικείμενο: ")
            eparkia = input("Επάρκεια (0-10): ")
            cursor.execute('''INSERT INTO prosonta VALUES (?,?)''',(kod_prosontos,""))
            cursor.execute('''INSERT INTO gnosh
            VALUES (?,?,?)''',(kod_prosontos,antikeimeno,eparkia))         
            
            
switch = {"1":option1, "2":option2, "3":option3, "4":option4, "5":option5, "6":option6, "7":option7,"11":option11,"12":option12}

while(True):
    conn, c = connect_to_db('grafeio')
    print_info()
    choice = input("Παρακαλώ επιλέξτε μια από τις παραπάνω επιλογές (1-14): ")
    if choice not in ["1","2","3","4","5","6","7","11","12"]:
        print("Πραγματοποιήθηκε έξοδος από το σύστημα...")
        break
    switch[choice](c)
    conn.commit()
    conn.close()
    
