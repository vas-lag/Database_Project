# -*- coding: utf-8 -*-
"""

@author: Billy
"""


import sqlite3
import tabulate as tab
from datetime import datetime
import dateutil.relativedelta

def connect_to_db(dbname):
    connection = sqlite3.connect(dbname + '.sqlite3')
    cursor = connection.cursor()
    return connection,cursor

def display_data(cursor,rows):
    columns = [i[0] for i in cursor.description]
    print(tab.tabulate(rows, headers = columns, tablefmt='psql'))

def print_info():
    print("\n---  ΓΡΑΦΕΙΟ ΕΥΡΕΣΗΣ ΕΡΓΑΣΙΑΣ SIMPLE API  ---")
    print("-- 1. Να βρεθούν όλοι οι ενδιαφερόμενοι που ικανοποιούν τις προυποθέσεις της θέσης εργασίας Χ")
    print("-- 2. Να βρεθούν όλες οι θέσεις εργασίας των οποίων τις προυποθέσεις ικανοποιεί ο ενδιαφερόμενος με κωδικό Χ")
    print("-- 3. Εισαγωγή νέας αίτησης εργασίας")
    print("-- 4. Εισαγωγή νέας θέσης εργασίας")
    print("-- 5. Διαγραφή αίτησης εργασίας")
    print("-- 6. Διαγραφή θέσης εργασίας")
    print("-- 7. Να τυπωθούν όλες οι πληροφορίες για τον εργαζόμενο με το επιλεγμένο ΑΦΜ")
    print("-- 8. Να τυπωθούν όλες οι πληροφορίες για τον εργοδότη με το επιλεγμένο ΑΦΜ")
    print("-- 9. Επιπλέον λειτουργίες")
    
def option9(cursor):
    print("\n---  Επιπλέον λειτουργίες  ---")
    print("-- 1. Να βρεθούν όλες οι θέσεις εργασίας στον Νομό Χ από την εταιρία Υ")
    print("-- 2. Να βρεθεί ο μέσος μισθός για τις θέσεις εργασίας που έχουν να κάνουν με τον τομέα Χ στον Νομό Υ")
    print("-- 3. Να βρεθεί η περιοχή(ές) με την μεγαλύτερη ζήτηση εργασίας ")
    print("-- 4. Να βρεθούν τα ονόματα και τα τηλέφωνα των ενδιαφερόμενων που κατέχουν πτυχίο X και έχουν δηλώσει τόπο ενδιαφέροντος τον Νομό Y")
    print("-- 5. Να βρεθει ο μεσος μισθός για όλες τις θέσεις εργασιας ανά περιοχή και να γίνει φθίνουσα ταξινόμηση")
    print("-- 6. Να βρεθούν οι ενδιαφερόμενοι που έχουν τρέχουσα αίτηση τους στον Νομό Χ")
    print("-- 7. Να βρεθούν οι ενδιαφερόμενοι που έχουν προϋπηρεσία στο πόστο Χ και έχουν γνώση Υ")
    choice = input("Παρακαλώ επιλέξτε μια από τις παραπάνω επιλογές (1-7): ")
    while choice not in['1','2','3','4','5','6','7']:
        print("Δώσατε λάθος είσοδο, προσπαθήστε ξανά")
        choice = input("Παρακαλώ επιλέξτε μια από τις παραπάνω επιλογές (1-7): ")
    choice = str(int(choice) + 10)
    switch[choice](c)



def option11(cursor):
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

def option12(cursor):
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

def option13(cursor):
    rows = cursor.execute('''SELECT topos_endiaferontos AS νομός_με_μεγαλύτερη_ζήτηση,COUNT(*) AS αριθμός_θέσεων_εργασίας
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

def option14(cursor):
    ptyxio_raw = input("Εισάγεται το πτυχίο ενδιαφέροντος: ")
    nomos_raw = input("Εισάγετε τον νομό ενδιαφέρονοτος: ")
    ptyxio = '%'+ptyxio_raw+'%'
    nomos = '%'+nomos_raw+'%'
    rows = cursor.execute('''SELECT DISTINCT onoma,eponymo,email,afm,thlefwno
    FROM ((((ENDIAFEROMENOS e JOIN AITHSH_ERGASIAS a
    ON e.kod_endiaferomenou = a.kod_endiaferomenou_aithshs) JOIN PERILAMVANEI pe
    ON a.kod_aithshs = pe.aithsh) JOIN PROSONTA pr
    ON pe.proson = pr.kod_prosontos) JOIN PTYXIO pt
    ON pr.kod_prosontos = pt.kod_prosontos) JOIN THLEFWNO_ENDIAFEROMENOU t
    ON e.kod_endiaferomenou = t.endiaferomenos
    WHERE a.topos_endiaferontos LIKE ?
    AND pt.antikeimeno LIKE ?''', (nomos,ptyxio))
    display_data(cursor,rows)

def option15(cursor):
    rows = cursor.execute('''SELECT topos,CAST(AVG(misthos) AS INT) AS AVG_MISTHOS
    FROM THESI_ERGASIAS
    GROUP BY topos 
    ORDER BY AVG(misthos) DESC''')
    display_data(cursor,rows)

def option16(cursor):
    nomos_raw = input("Εισάγετε τον τόπο ενδιαφέρονοτος: ")
    nomos = '%'+nomos_raw+'%'
    rows = cursor.execute('''SELECT DISTINCT endiaferomenos.*
    FROM endiaferomenos, aithsh_ergasias
    WHERE endiaferomenos.kod_endiaferomenou = aithsh_ergasias.kod_endiaferomenou_aithshs
        AND aithsh_ergasias.topos_endiaferontos LIKE ?
        AND date('now')<aithsh_ergasias.hmeromhnia_lhxhs_aithshs''',(nomos,))
    display_data(cursor,rows)

def option17(cursor):
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
    
def option1(cursor):
    kod_theshs = input("Εισάγετε τον κωδικό θέσης που σας ενδιαφέρει: ")
    rows = cursor.execute('''SELECT DISTINCT t1.*
    FROM (SELECT DISTINCT e.*
    FROM AITHSH_ERGASIAS ai JOIN ((((THESI_ERGASIAS th LEFT JOIN PROYPOTHETEI proipo
    ON th.kod_theshs = proipo.kod_ergasias) LEFT JOIN PROIPIRESIA proipiresia2
    ON proipo.kod_proipiresias = proipiresia2.kod_proipiresias) JOIN PROIPIRESIA proipiresia1
    ON ((proipiresia2.tomeas = proipiresia1.tomeas AND proipiresia2.diarkeia <= proipiresia1.diarkeia) OR proipiresia2.tomeas IS NULL)) JOIN DIATHETEI d
    ON proipiresia1.kod_proipiresias = d.kod_proipiresias)
    ON (ai.kod_aithshs = d.aithsh AND proipiresia1.tomeas IS NOT NULL) OR proipiresia2.tomeas IS NULL JOIN ENDIAFEROMENOS e
    ON ai.kod_endiaferomenou_aithshs = e.kod_endiaferomenou JOIN AFORA af
    ON ai.kod_aithshs = af.aithsh JOIN TOMEAS_ERGASIAS tomeas
    ON af.tomeas = tomeas.onoma JOIN ANHKEI an
    ON tomeas.onoma = an.tomeas AND th.kod_theshs = an.kod_ergasias
    WHERE th.kod_theshs = ?) AS t1,
    (SELECT DISTINCT e.*
    FROM AITHSH_ERGASIAS ai JOIN (THESI_ERGASIAS th LEFT JOIN APAITEI apa
    ON (th.kod_theshs = apa.kod_ergasias AND apa.proson IN (SELECT kod_prosontos FROM PTYXIO p)) LEFT JOIN PTYXIO ptyxio2
    ON (apa.proson = ptyxio2.kod_prosontos) JOIN PTYXIO ptyxio1
    ON (ptyxio2.antikeimeno = ptyxio1.antikeimeno) OR (ptyxio2.antikeimeno IS NULL) JOIN PERILAMVANEI pe
    ON ptyxio1.kod_prosontos = pe.proson)
    ON (ai.kod_aithshs = pe.aithsh AND ptyxio1.antikeimeno IS NOT NULL)	OR ptyxio2.antikeimeno IS NULL JOIN ENDIAFEROMENOS e
    ON ai.kod_endiaferomenou_aithshs = e.kod_endiaferomenou
    WHERE th.kod_theshs = ?) AS t2,
    (SELECT DISTINCT e.*
    FROM AITHSH_ERGASIAS ai JOIN (THESI_ERGASIAS th LEFT JOIN APAITEI apa
    ON (th.kod_theshs = apa.kod_ergasias AND apa.proson IN (SELECT kod_prosontos FROM GNOSH p)) LEFT JOIN GNOSH gnosh2
    ON apa.proson = gnosh2.kod_prosontos JOIN GNOSH gnosh1
    ON (gnosh2.antikeimeno = gnosh1.antikeimeno) OR gnosh2.antikeimeno IS NULL JOIN PERILAMVANEI pe
    ON gnosh1.kod_prosontos = pe.proson)
    ON (ai.kod_aithshs = pe.aithsh AND gnosh1.antikeimeno IS NOT NULL)	OR gnosh2.antikeimeno IS NULL JOIN ENDIAFEROMENOS e
    ON ai.kod_endiaferomenou_aithshs = e.kod_endiaferomenou
    WHERE th.kod_theshs = ?
    GROUP BY ai.kod_aithshs 
    HAVING COUNT(gnosh1.antikeimeno) >= (SELECT COUNT(gnosh2.antikeimeno)
    FROM THESI_ERGASIAS th LEFT JOIN APAITEI apa
    ON (th.kod_theshs = apa.kod_ergasias AND apa.proson IN (SELECT kod_prosontos FROM GNOSH p)) LEFT JOIN GNOSH gnosh2
    ON (apa.proson = gnosh2.kod_prosontos)
    WHERE th.kod_theshs = ?)) AS t3
    WHERE t1.kod_endiaferomenou = t2.kod_endiaferomenou
    AND t2.kod_endiaferomenou = t3.kod_endiaferomenou''',(kod_theshs,kod_theshs,kod_theshs,kod_theshs))
    display_data(cursor,rows)
    
def option2(cursor):
    kod_endiaferomenou = input("Εισάγετε τον κωδικό του ενδιαφερόμενου που σας ενδιαφέρει: ")
    rows = cursor.execute('''SELECT *
    FROM (SELECT DISTINCT t1.*
    FROM (SELECT DISTINCT th.*
    FROM AITHSH_ERGASIAS ai JOIN ((((THESI_ERGASIAS th LEFT JOIN PROYPOTHETEI proipo
    ON th.kod_theshs = proipo.kod_ergasias) LEFT JOIN PROIPIRESIA proipiresia2
    ON proipo.kod_proipiresias = proipiresia2.kod_proipiresias) JOIN PROIPIRESIA proipiresia1
    ON ((proipiresia2.tomeas = proipiresia1.tomeas AND proipiresia2.diarkeia <= proipiresia1.diarkeia) OR proipiresia2.tomeas IS NULL)) JOIN DIATHETEI d
    ON proipiresia1.kod_proipiresias = d.kod_proipiresias)
    ON (ai.kod_aithshs = d.aithsh AND proipiresia1.tomeas IS NOT NULL) OR proipiresia2.tomeas IS NULL JOIN ENDIAFEROMENOS e
    ON ai.kod_endiaferomenou_aithshs = e.kod_endiaferomenou JOIN AFORA af
    ON ai.kod_aithshs = af.aithsh JOIN TOMEAS_ERGASIAS tomeas
    ON af.tomeas = tomeas.onoma JOIN ANHKEI an
    ON tomeas.onoma = an.tomeas AND th.kod_theshs = an.kod_ergasias
    WHERE e.kod_endiaferomenou = ?) AS t1,
    (SELECT DISTINCT th.*
    FROM AITHSH_ERGASIAS ai JOIN (THESI_ERGASIAS th LEFT JOIN APAITEI apa
    ON (th.kod_theshs = apa.kod_ergasias AND apa.proson IN (SELECT kod_prosontos FROM PTYXIO p)) LEFT JOIN PTYXIO ptyxio2
    ON (apa.proson = ptyxio2.kod_prosontos) JOIN PTYXIO ptyxio1
    ON (ptyxio2.antikeimeno = ptyxio1.antikeimeno) OR (ptyxio2.antikeimeno IS NULL) JOIN PERILAMVANEI pe
    ON ptyxio1.kod_prosontos = pe.proson)
    ON (ai.kod_aithshs = pe.aithsh AND ptyxio1.antikeimeno IS NOT NULL)	OR ptyxio2.antikeimeno IS NULL JOIN ENDIAFEROMENOS e
    ON ai.kod_endiaferomenou_aithshs = e.kod_endiaferomenou
    WHERE e.kod_endiaferomenou = ?) AS t2,
    (SELECT DISTINCT th.*
    FROM AITHSH_ERGASIAS ai JOIN (THESI_ERGASIAS th LEFT JOIN APAITEI apa
    ON (th.kod_theshs = apa.kod_ergasias AND apa.proson IN (SELECT kod_prosontos FROM GNOSH p)) LEFT JOIN GNOSH gnosh2
    ON apa.proson = gnosh2.kod_prosontos JOIN GNOSH gnosh1
    ON (gnosh2.antikeimeno = gnosh1.antikeimeno) OR (gnosh2.antikeimeno IS NULL) JOIN PERILAMVANEI pe
    ON gnosh1.kod_prosontos = pe.proson)
    ON (ai.kod_aithshs = pe.aithsh AND gnosh1.antikeimeno IS NOT NULL)	OR gnosh2.antikeimeno IS NULL JOIN ENDIAFEROMENOS e
    ON ai.kod_endiaferomenou_aithshs = e.kod_endiaferomenou
    WHERE e.kod_endiaferomenou = ?
    GROUP BY th.kod_theshs 
    HAVING COUNT(gnosh1.antikeimeno) >= (SELECT COUNT(gnosh2.antikeimeno)
    FROM THESI_ERGASIAS th LEFT JOIN APAITEI apa
    ON (th.kod_theshs = apa.kod_ergasias AND apa.proson IN (SELECT kod_prosontos FROM GNOSH p)) LEFT JOIN GNOSH gnosh2
    ON (apa.proson = gnosh2.kod_prosontos)
    WHERE e.kod_endiaferomenou = ?)) AS t3
    WHERE t1.kod_theshs = t2.kod_theshs
    AND t2.kod_theshs = t3.kod_theshs) table1,ERGODOTHS er
    WHERE table1.ergodoths = er.kod_ergodoth''',(kod_endiaferomenou,kod_endiaferomenou,kod_endiaferomenou,kod_endiaferomenou))
    display_data(cursor,rows)
       
def option3(cursor):
    choice = input("Ο ενδιαφερόμενος της αίτησης έχει υποβάλει ξανά στην εταιρία μας; \n(εισάγετε 'ναι' ή 'οχι'): ")
    if choice == 'οχι':      
        name = input("Όνομα: ")
        last_name = input("Επίθετο: ")
        age = input("Ηλικία: ")
        sex = input("Φύλο, εισάγετε 'M' ή 'F': ")
        email = input("Email: ")
        afm = input("ΑΦΜ: ")
        nomos = input("Τόπος κατοικίας: ")
        address = input("Διεύθυνση κατοικίας: ")
        cursor.execute('''INSERT INTO endiaferomenos
        VALUES (NULL,?,?,?,?,?,?,?,?)''',(name,last_name,age,sex,email,afm,nomos,address))
        phone_num_str = input("Εισάγετε το/τα κινητά τηλέφωνα του ενδιαφερόμενου χωρισμένα με κενά: ")
        phone_nums = phone_num_str.split(" ")
        cursor.execute('''SELECT kod_endiaferomenou
        FROM endiaferomenos
        WHERE email LIKE ?''',(email,))
        kod_endiaf = cursor.fetchone()[0]
        for phone_num in phone_nums:
            cursor.execute('''INSERT INTO thlefwno_endiaferomenou
            VALUES (?,?)''', (kod_endiaf, phone_num))      
    elif choice == 'ναι':
        afm = input("Εισάγετε το ΑΦΜ του ενδιαφερόμενου: ")
        cursor.execute('''SELECT kod_endiaferomenou
            FROM endiaferomenos
            WHERE afm = ?''',(afm,))
        kod_endiaf = cursor.fetchone()[0]
    else:
        return
    
    nomos = input("Εισάγετε τόπο ενδιαφέροντος: ")
    end_str = input("Εισάγετε για πόσους μήνες θέλετε να μείνει ανοιχτή η αίτηση: ")
    start_date = datetime.now().date()
    end_date = start_date + dateutil.relativedelta.relativedelta(months =+ int(end_str))  
    cursor.execute('''INSERT INTO AITHSH_ERGASIAS (kod_aithshs, topos_endiaferontos, hmeromhnia_lhxhs_aithshs, kod_endiaferomenou_aithshs)
    VALUES (NULL,?,?,?)''',(nomos,end_date,kod_endiaf))
    cursor.execute('''SELECT MAX(kod_aithshs)
    FROM aithsh_ergasias''')
    kod_aithshs = cursor.fetchone()[0]

    #check for tomea/proipiresia/prosonta
    afora_ch = input("Η αίτηση αφορά γνωστό Τομέα Εργασίας; \n(εισάγετε 'ναι' ή 'οχι'): ")
    if afora_ch == 'ναι':
        tomeas = input("Εισάγετε το όνομα του τομέα: ")      
        cursor.execute('''INSERT INTO afora
        VALUES (?,?)''',(kod_aithshs,tomeas))
    while(True):
        proip_ch = input("Θέλετε να προσθέσετε επιπλέον προϋπηρεσία που διαθέτει ο ενδιαφερόμενος για την αίτηση αυτή; \n(εισάγετε 'ναι' ή 'όχι': ")
        if proip_ch == 'ναι':
            etairia = input("Εταιρία: ")
            posto = input("Πόστο: ")
            start_str = input("Ημερομηνία έναρξης: ")
            start_date = datetime.strptime(start_str,'%d-%m-%Y').date()
            end_str = input("Ημερομηνία λήξης: ")
            end_date = datetime.strptime(end_str,'%d-%m-%Y').date()       
            duration = end_date.year - start_date.year
            tomeas_ch = input("Η προϋπηρεσία αυτή ανήκει σε κάποιον γνωστό τομέα εργασίας; \n(εισάγετε 'ναι ή 'οχι': ")
            if tomeas_ch=='ναι':
                tomeas = input("Εισάγετε τομέα: ")
                cursor.execute('''INSERT INTO proipiresia
                VALUES (NULL,?,?,?,?,?,?)''',(etairia,posto,start_date,end_date,duration,tomeas))
            else:
                cursor.execute('''INSERT INTO proipiresia
                VALUES (NULL,?,?,?,?,?,NULL)''',(etairia,posto,start_date,end_date,duration))
            cursor.execute('''SELECT MAX(kod_proipiresias)
            FROM proipiresia''')
            kod_proip = cursor.fetchone()[0]
            cursor.execute('''INSERT INTO diathetei
            VALUES (?,?)''', (kod_aithshs,kod_proip))
        elif proip_ch == 'οχι':
            break
        else:
            print("Η απάντηση που δώσατε δεν είναι έγκυρη")
            
    proson_ch = input("Θέλετε να προσθέσετε επιπλέον προσόντα (πτυχίο/γνώσεις) που διαθέτει ο ενδιαφερόμενος για την αίτηση αυτή; \n(εισάγετε 'ναι' ή 'οχι'): ")
    if proson_ch=='ναι':
        ptyxio_ch = input("Κατέχει κάποιο πιστοποιημένο πτυχίο; \n(εισάγετε 'ναι' ή 'οχι'): ")
        if ptyxio_ch=='ναι':
            while(True):
                cursor.execute('''SELECT MAX(kod_prosontos)
                FROM prosonta''')
                kod_prosontos = cursor.fetchone()[0] + 1
                antikeimeno = input("Αντικείμενο: ")
                vathmos = input("Βαθμός: ")
                eksidikeysi = input("Εξειδίκευση: ")
                etos = input("Έτος απόκτησης: ")
                foreas = input("Φορέας: ")
                cursor.execute('''INSERT INTO prosonta VALUES (?,NULL)''',(kod_prosontos,))
                cursor.execute('''INSERT INTO perilamvanei VALUES (?,?)''',(kod_aithshs,kod_prosontos))
                cursor.execute('''INSERT INTO ptyxio
                VALUES (?,?,?,?,?,?)''',(kod_prosontos,antikeimeno,vathmos,eksidikeysi,etos,foreas))
                ptyxio_ch = input("Θέλετε να προσθέσετε επιπλέον πτυχίο; \n(εισάγετε 'ναι' ή 'οχι'): ")
                if ptyxio_ch == 'οχι':
                    break
        gnoseis_ch = input("Κατέχει γνώσεις που θέλει να δηλώσει; \n(εισάγετε 'ναι' ή 'οχι'): ")
        if gnoseis_ch =='ναι':
            while(True):
                cursor.execute('''SELECT MAX(kod_prosontos)
                FROM prosonta''')
                kod_prosontos = cursor.fetchone()[0] + 1
                antikeimeno = input("Αντικείμενο: ")
                eparkia = input("Επάρκεια (0-10): ")
                cursor.execute('''INSERT INTO prosonta VALUES (?,?)''',(kod_prosontos,""))
                cursor.execute('''INSERT INTO perilamvanei VALUES (?,?)''',(kod_aithshs,kod_prosontos))
                cursor.execute('''INSERT INTO gnosh
                VALUES (?,?,?)''',(kod_prosontos,antikeimeno,eparkia))
                gnoseis_ch = input("Θέλετε να προσθέσετε επιπλέον γνώση; \n(εισάγετε 'ναι' ή 'οχι'): ")
                if gnoseis_ch == 'οχι':
                    break


def option4(cursor):
    choice = input("Ο εργοδότης έχει υποβάλει ξανά θέση εργασίας στην εταιρία μας; \n(εισάγετε 'ναι' ή 'οχι'): ")
    if choice == 'οχι':      
        name = input("Όνομα: ")
        last_name = input("Επίθετο: ")
        sex = input("Φύλο, εισάγετε 'M' ή 'F': ")
        email = input("Email: ")
        afm = input("ΑΦΜ: ")
        address = input("Διεύθυνση κατοικίας: ")
        cursor.execute('''INSERT INTO ergodoths
        VALUES (NULL,?,?,?,?,?,?)''',(name,last_name,sex,email,afm,address))
        phone_num_str = input("Εισάγετε το/τα κινητά τηλέφωνα του ενδιαφερόμενου χωρισμένα με κενά: ")
        phone_nums = phone_num_str.split(" ")
        cursor.execute('''SELECT kod_ergodoth
        FROM ergodoths
        WHERE email LIKE ?''',(email,))
        kod_ergodoth = cursor.fetchone()[0]
        for phone_num in phone_nums:
            cursor.execute('''INSERT INTO thlefwno_ergodoth
            VALUES (?,?)''', (kod_ergodoth, phone_num))      
    elif choice == 'ναι':
        afm = input("Εισάγετε το ΑΦΜ του εργοδότη: ")  
        cursor.execute('''SELECT kod_ergodoth
            FROM ergodoths
            WHERE afm = ?''',(afm,))
        kod_ergodoth = cursor.fetchone()[0]
    else:
        return

    etairia = input("Εισάγετε εταιρία: ")
    nomos = input("Εισάγετε τόπο ενδιαφέροντος: ")
    misthos = input("Εισάγετε ενδεικτικό ετήσιο μισθό: ")
    perigrafh = input("Εισάγετε περιγραφή: ")
    orario = input("'Πλήρης Απασχόληση' ή 'Μερική Απασχόληση':")
    end_str = input("Εισάγετε για πόσες εβδομάδες θέλετε να μείνει ανοιχτή η αίτηση: ")
    start_date = datetime.now().date()
    end_date = start_date + dateutil.relativedelta.relativedelta(weeks =+ int(end_str))  
    cursor.execute('''INSERT INTO THESI_ERGASIAS (kod_theshs,etairia,topos,misthos,perigrafi,orario,hmeromhnia_lhxhs,ergodoths)
    VALUES (NULL,?,?,?,?,?,?,?)''',(etairia,nomos,misthos,perigrafh,orario,end_date,kod_ergodoth))
    cursor.execute('''SELECT MAX(kod_theshs)
    FROM thesi_ergasias''')
    kod_theshs = cursor.fetchone()[0]

    #check for tomea/proipiresia/prosonta
    afora_ch = input("Η θέση αφορά γνωστό Τομέα Εργασίας; \n(εισάγετε 'ναι' ή 'οχι'): ")
    if afora_ch == 'ναι':
        tomeas = input("Εισάγετε το όνομα του τομέα: ")      
        cursor.execute('''INSERT INTO anhkei
        VALUES (?,?)''',(kod_theshs,tomeas))
    proip_ch = input("Ο εργοδότης απαιτεί συγκεκριμένη προϋπηρεσία για την θέση αυτή; \n(εισάγετε 'ναι' ή 'όχι': ")
    if proip_ch == 'ναι':
        tomeas = input("Σε ποιόν τομέα πρέπει να ανήκει η προυπηρεσία; ")
        duration = input("Ελάχιστα χρόνια προυπηρεσίας σε αυτόν τον τομέα: ")
        aparaithth = input("Πόσο απαραίτητη είναι αυτή η προϋπηρεσία (1-10); ")
        cursor.execute('''INSERT INTO proipiresia
        VALUES (NULL,NULL,NULL,NULL,NULL,?,?)''',(duration,tomeas))
        cursor.execute('''SELECT MAX(kod_proipiresias)
        FROM proipiresia''')
        kod_proip = cursor.fetchone()[0]
        cursor.execute('''INSERT INTO proypothetei
        VALUES (?,?,?)''', (kod_theshs,kod_proip,aparaithth))
    proson_ch = input("Ο εργοδότης απαιτεί προσόντα για την θέση αυτή (πτυχίο/γνώσεις); \n(εισάγετε 'ναι' ή 'οχι'): ")
    if proson_ch=='ναι':
        ptyxio_ch = input("Απαιτείται κάποιο πιστοποιημένο πτυχίο; \n(εισάγετε 'ναι' ή 'οχι'): ")
        if ptyxio_ch=='ναι':
            cursor.execute('''SELECT MAX(kod_prosontos)
            FROM prosonta''')
            kod_prosontos = cursor.fetchone()[0] + 1
            antikeimeno = input("Αντικείμενο: ")
            vathmos = input("Βαθμός: ")
            eksidikeysi = input("Εξειδίκευση: ")
            shmantikothta = input("Σημαντικότητα για τον εργοδότη (1-10): ") 
            cursor.execute('''INSERT INTO prosonta VALUES (?,?)''',(kod_prosontos,""))
            cursor.execute('''INSERT INTO apaitei VALUES (?,?,?)''',(kod_theshs,kod_prosontos,shmantikothta))
            cursor.execute('''INSERT INTO ptyxio 
            VALUES (?,?,?,?,NULL,NULL)''',(kod_prosontos,antikeimeno,vathmos,eksidikeysi))
        gnoseis_ch = input("Απαιτούνται γενικότερες γνώσεις; \n(εισάγετε 'ναι' ή 'οχι'): ")
        if gnoseis_ch == 'ναι':
            while(True):
                cursor.execute('''SELECT MAX(kod_prosontos)
                FROM prosonta''')
                kod_prosontos = cursor.fetchone()[0] + 1
                antikeimeno = input("Αντικείμενο: ")
                eparkia = input("Επάρκεια (0-10): ")
                shmantikothta = input("Σημαντικότητα για τον εργοδότη (1-10): ") 
                cursor.execute('''INSERT INTO prosonta VALUES (?,?)''',(kod_prosontos,""))
                cursor.execute('''INSERT INTO apaitei VALUES (?,?,?)''',(kod_theshs,kod_prosontos,shmantikothta))
                cursor.execute('''INSERT INTO gnosh
                VALUES (?,?,?)''',(kod_prosontos,antikeimeno,eparkia))    
                gnoseis_ch = input("Η θέση απαιτεί και άλλες γνώσεις; \n(εισάγετε 'ναι' ή 'οχι'): ")
                if gnoseis_ch == 'οχι':
                    break

def option5(cursor):
    choice = '5'
    while choice not in ['1','2']:
        choice = input("Θέλετε να διαγράψετε μια αίτηση εργασίας με βάση τον κωδικό της ή να διαγράψετε έναν ενδιαφερόμενο μαζί με όλες του τις αιτήσεις;\n(εισάγετε '1' ή '2'): ")
        if choice == '1':
            kod = input("Δώστε τον κωδικό της αίτησης που θα διαγραφει: ")
            cursor.execute("DELETE FROM AITHSH_ERGASIAS WHERE kod_aithshs = ?",(kod,))
        elif choice == '2':
            inp = input("Δώστε το ΑΦΜ του ενδιαφερόμενου που θα διαγραφει ή τον κωδικό του: ")
            if len(inp) == 9:
                cursor.execute("DELETE FROM ENDIAFEROMENOS WHERE afm = ?",(inp,))
            else:
                cursor.execute("DELETE FROM ENDIAFEROMENOS WHERE kod_endiaferomenou = ?",(int(inp),))
        else :
            print("Δώσατε λανθασμένη είσοδο")

def option6(cursor):
    choice = '5'
    while choice not in ['1','2']:
        choice = input("Θέλετε να διαγράψετε μια θέση εργασίας με βάση τον κωδικό της\n ή να διαγράψετε έναν εργοδότη μαζί με όλες τις θέσεις που προσφέρει;\n(εισάγετε '1' ή '2'): ")
        if choice == '1':
            kod = input("Δώστε τον κωδικό της θέσης που θα διαγραφει: ")
            cursor.execute("DELETE FROM THESI_ERGASIAS WHERE kod_theshs = ?",(kod,))
        elif choice == '2':
            inp = input("Δώστε το ΑΦΜ του εργοδότη που θα διαγραφει ή τον κωδικό του: ")
            if len(inp) == 9:
                cursor.execute("DELETE FROM ERGODOTHS WHERE afm = ?",(inp,))
            else:
                cursor.execute("DELETE FROM ERGODOTHS WHERE kod_ergodoth = ?",(int(inp),))
        else :
            print("Δώσατε λανθασμένη είσοδο")

def option7(cursor):
    afm = input("Δώστε το ΑΦΜ του ενδιαφερόμενου του οποίου θέλετε να βρείτε τα στοιχεία: ")
    rows = cursor.execute('''SELECT *
            FROM endiaferomenos e, thlefwno_endiaferomenou t
            WHERE e.kod_endiaferomenou = t.endiaferomenos
            AND e.afm = ?''',(afm,))
    display_data(cursor,rows)
            
def option8(cursor):
    afm = input("Δώστε το ΑΦΜ του εργοδότη του οποίου θέλετε να βρείτε τα στοιχεία: ")
    rows = cursor.execute('''SELECT *
            FROM ergodoths e, thlefwno_ergodoth t
            WHERE e.kod_ergodoth = t.ergodoths
            AND e.afm = ?''',(afm,))
    display_data(cursor,rows)
    
    
    
switch = {"1":option1, "2":option2, "3":option3, "4":option4, "5":option5, "6":option6, "7":option7, "8":option8,"9":option9,
          "11":option11, "12":option12, "13":option13, "14":option14, "15":option15}
while(True):
    conn, c = connect_to_db('grafeioDB')
    c.execute('''PRAGMA foreign_keys = ON;''')
    print_info()
    choice = input("Παρακαλώ επιλέξτε μια από τις παραπάνω επιλογές (1-9) η πατήστε q για έξοδο: ")
    if choice == 'q':
        print("Πραγματοποιήθηκε έξοδος από το σύστημα")
        break
    while choice not in['1','2','3','4','5','6','7','8','9','q']:
        print("Δώσατε λάθος είσοδο, προσπαθήστε ξανά")
        choice = input("Παρακαλώ επιλέξτε μια από τις παραπάνω επιλογές (1-9) η πατήστε q για έξοδο: ")
        if choice == 'q':
            print("Πραγματοποιήθηκε έξοδος από το σύστημα")
            break
    if choice == 'q':
        break
    switch[choice](c)
    conn.commit()
    conn.close()
    
