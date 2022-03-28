###     TASK 1      ###
import mysql.connector  # Here we import the MySql-Python connector (Task 1.1)
import csv

cnx = mysql.connector.connect(user='root', password='Prijedor9393!', # (Task 1.4)
host ='127.0.0.1', buffered=True)  # connecting to MySql

DB_NAME = "cikota"    # The database name (My last name)

My_cursor = cnx.cursor()    # we define a cursor so we can navigate in the database

My_cursor.execute("SHOW DATABASES")    # registers the existing databases in the My_cursor

db_found = False

for a in My_cursor:    # checking if database "Cikota" exists (Task 1.2 and task 1.3)
    if a == (DB_NAME,):
        db_found = True
        My_cursor.execute("USE %s" % DB_NAME)
        break       # i use break so that the for-loop doesent interfere with code further down

if db_found == False:      # if database Cikota does not exist, we create the database Cikota with tables showing data according to our files.
    print("creating DATABASE")
    My_cursor.execute("CREATE DATABASE %s" % DB_NAME)
    My_cursor.execute("USE %s" % DB_NAME) 

    My_cursor.execute("CREATE TABLE IF NOT EXISTS planets (name varchar(50) not null, rotation_period nvarchar(50), orbital_period nvarchar(50), diameter nvarchar(50), climate nvarchar(50), gravity nvarchar(50), terrain nvarchar(50), surface_water nvarchar(50), population nvarchar(50), primary key(name))")
    # Here we create a table for Planets.csv with all of its attributes.
    with open('planets.csv', 'r') as file: # Here we open the file
        read = csv.DictReader(file, delimiter=',')    # Here we want to delimit every column with a comma (this will be ignored if the comma is within quotes.)
        for line in read:
            My_cursor.execute("INSERT INTO planets (name,rotation_period,orbital_period,diameter,climate,gravity,terrain,surface_water,population)" \
                            "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (line['name'], line['rotation_period'], line['orbital_period'], line['diameter'], line['climate'], line['gravity'], line['terrain'], line['surface_water'], line['population']))
    # %s is a placeholder for values to be inserted in the various attributes/positions. So when the row for planet 1 comes then we will place its values next to it until we have filled all attributes/positions
    cnx.commit() # This saves the changes we have currently made in the database

    My_cursor.execute("CREATE TABLE IF NOT EXISTS species (name varchar(50) not null,classification nvarchar(50),designation nvarchar(50),average_height nvarchar(50),skin_colors nvarchar(50),hair_colors nvarchar(50),eye_colors nvarchar(50),average_lifespan nvarchar(50),language nvarchar(50),homeworld nvarchar(50), primary key(name))")
    # Here we create the table for species.csv
    with open('species.csv', 'r') as file: # Here we open the file
        reader = csv.DictReader(file, delimiter=',')
        for line in reader:
            line['name'] = str(line['name']).replace("'", "´")
            line['language'] = str(line['language']).replace("'", "´")
            line['homeworld'] = str(line['homeworld']).replace("'", "´")    # Here we switch out the single quotations (escape characters) to apostrophies.
            My_cursor.execute("INSERT INTO species (name,classification,designation,average_height,skin_colors,hair_colors,eye_colors,average_lifespan,language,homeworld)" \
                            "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (line['name'], line['classification'], line['designation'], line['average_height'], line['skin_colors'], line['hair_colors'], line['eye_colors'], line['average_lifespan'], line['language'], line['homeworld']))
                    
    cnx.commit()

###     TASK 2      ###

while True:     #(Line 52-61: This is a menu we are creating together with a variable called menu that enables us to choose each number)
    print("__________________________")     # using lines of underscores to create lines in the terminal, making it a bit more readable.
    print("1. List all planets.")
    print("2. Search for planet details.")
    print("3. Search for species with height higher than given number.")
    print("4. What is the most likely desired climate of the given species.")
    print("5. What is the average lifespan per species classification?")
    print("Q. Quit")
    print("______________________________")
    menu = input("Please choose one option:")   # We can choose any feature in the menu by the number (1-5, Q)

    if menu == '1':     # Task 2.1
        My_cursor.execute("SELECT name FROM planets;")      #Selecting names of all planets in the cursor
        print("name of planets\n______________________________")
        for x in My_cursor:
            print("%s" % x)     #Printing all information that the cursor holds (names of the planets)
    
    elif menu == '2':       #Task 2.2
        choice = input("choose a planet : ")        #We want to get details about a GIVEN planet so we need to input it
        My_cursor.execute("SELECT * FROM planets WHERE name = '%s'" % choice)   #Selecting all information (*) from planets by name and putting the value "choice" to it.
        planetdetail = My_cursor.fetchall()     # The fetchall function extracts all information that the cursor "points to".
        print(planetdetail)
        
    elif menu == '3':       #Task 2.3
         higher_than = int(input("select your height: "))
         My_cursor.execute("SELECT name FROM species WHERE average_height > %s;" % higher_than)     # We only want to select the names that are larger than the input we have given.
         print("speiceies taller than by Name:\n______________________________")        # a simple print for esthetic reasons in the terminal
         for name in My_cursor:
             print(str(name).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))       # Removing all special characters because its ugly when we only want to display a list of species larger than the given value

    elif menu == '4':       # Task 2.4
        choice = input("Choose species : ")     #input
        My_cursor.execute("SELECT homeworld FROM species WHERE name = '%s'" % choice.replace("'", "´"))    #Because the single quote is an escape character an error will be given when python tries reading through it so we need to replace it with a proper apostrophe.
        homeworld = My_cursor.fetchall()        # Extracting all information that the cursor points to
        homeworld = str(homeworld).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("[", "").replace("]", "")    #Here we NEED to remove all special signs because line 88 will not be able to handle it properly
        print(homeworld)
        My_cursor.execute("SELECT climate FROM planets WHERE name = '%s'" % homeworld)     #We now want to select climate from planets and give it the value "homeworld"
        desiredclimate = My_cursor.fetchall()      #This new selection will be called "desiredclimate"
        print("climate\n______________________________")
        for x in desiredclimate:
            print(str(x).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))   #   print all instances of x (the preferred climate)

    elif menu == '5':   #Task 2.5
        average_lifespan = {}       # We create a dictionary to hold information that will later be used.
        My_cursor.execute("SELECT classification FROM species")     # we aim our cursor at classification in species
        Classification = My_cursor.fetchall()       # Use fetchall to extract all of the classifications
        for c in Classification:        #For all instances c in classification (Line 98-103)....
            c = str(c).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("[", "").replace("]", "")    #Replace all of the special characters to make it look nice.
            My_cursor.execute("SELECT AVG(average_lifespan) FROM species WHERE classification = '%s'" % c)  # We select the AVERAGE of each classification by searching through it with our value-holder.
            lifespan = My_cursor.fetchall()     #We create a new variable called lifespan that will hold all of the averaged lifespans for each classification
            lifespan = str(lifespan).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("[", "").replace("]", "")
            average_lifespan[c] = lifespan  # the value lifespan will now be given to all instances c in the set average_lifespan
        
        print("species_classification \t average_lifespan\n______________________________")
        for x, y in average_lifespan.items():
            print(x, " ", y)    #We want to print both x and y, meaning, we want to print the classification and the average lifespan in one line

    elif menu == 'Q':
        quit()  # the option to quit the program is given by pressing "Q"
    
    else:       #If we write anything other than 1, 2, 3, 4, 5, Q the menu will simply ask for a valid input.
        print("invalid input! please choose 1-5 or Q to quit")