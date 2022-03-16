import csv
from mysql.connector import errorcode
import mysql.connector
from random import randrange

connection_args = {
    "host": "localhost",
    "user": "root",
    "password": "root"
}
DB_NAME = "drakborgen"

def numberofplayers(cursor, mydb):
    string = "CREATE VIEW Current_players AS SELECT players.name FROM players WHERE players.hero <> 'NULL'"
    cursor.execute(string)
    ans = str(cursor.fetchall())

def new_player(cursor, mydb):
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    gender = input("Enter your gender: ")

    while True:
        ans = input("Enter number between 1 and 4: ")
        string = "SELECT players.name FROM players WHERE players.hero='"+ans+"'"
        cursor.execute(string)
        try:
            player = str(cursor.fetchall()[0][0])
            print("This hero belongs to " + player)
        except:
            string = "SELECT name FROM heroes WHERE id ='"+ans+"'"
            cursor.execute(string)
            hero = str(cursor.fetchall()[0][0])
            id = ans
            question = input(hero + " has not been picked by anyone. Do you want him? y/n")
            if question == "y":
                print("You choose " + hero + "As your hero")
                string = "INSERT INTO players values(%s,%s,%s,%s)"
                ans = (name, age, gender, id)
                cursor.execute(string, ans)
                mydb.commit()
                break
            else:
                continue

def boardstate():
    pass

def playerherolist(cursor):
    string = "SELECT heroes.name, players.name FROM heroes JOIN players ON players.hero = heroes.id"
    cursor.execute(string)
    result = str(cursor.fetchall())
    print(result)

def create_database(cursor, mydb):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Faild to create database {}".format(err))
        exit(1)
def avgherohealth(cursor):
    string = "SELECT AVG(heroes.health) AS avgHp FROM heroes"
    cursor.execute(string)
    result = str(cursor.fetchall())
    print(result)

def newround(cursor,mydb):
    x = input("input an x coordinate")
    y = input("input a y coordinate")
    rnd = str(randrange(71))
    room = "SELECT * FROM room JOIN roomcard WHERE room.id=?"

    roomcard = "SELECT * FROM roomcard WHERE roomcard.id='"+str(randrange(71))+"'"
    cursor.execute(roomcard)
    event = str(cursor.fetchall()[0][2])
    cursor.execute(room)
    room = str(cursor.fetchall()[0][0])
    newroom = "INSERT INTO room WHERE VALUES (%s)"
    add = (event)
    room = str(cursor.fetchall())
    cursor.execute(newroom, add)
    newroom = str(cursor.fetchall())
    print(newroom)


    print(event)
    print(room)

def menu(cursor,mydb):
    print("_______________DRAKBORGEN_______________")
    print("1. Create new player")
    print("2. List all players and their hero")
    print("3. Check number of players")
    print("4. Average health")

    ans = input()
    if ans == "1":
        new_player(cursor, mydb)
    if ans == "2":
        playerherolist(cursor)
    if ans == "3":
        numberofplayers(cursor, mydb)
    if ans == "4":
        avgherohealth(cursor)


def create_tables(cursor, mydb):

    layout_players = 'INSERT INTO players(name, age, gender, hero)' 'VALUES(%s, %s, %s, %s)'
    layout_heroes = 'INSERT INTO heroes(id, name, strength, agility, armour, luck, health, gold, weapon)' 'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    layout_room = 'INSERT INTO room(id, exits, position, roomcard)' 'VALUES(%s, %s, %s, %s)'
    layout_roomcard = 'INSERT INTO roomcard(id, cardtype, name, effect)' 'VALUES(%s, %s, %s, %s)'

    create_players = "CREATE TABLE `players` (" \
                 "  `name` text," \
                 "  `age` text," \
                 "  `gender` text," \
                 "  `hero` text" \
                     ")ENGINE=InnoDB"

    create_heroes = "CREATE TABLE `heroes` (" \
                 "  `id` text NOT NULL," \
                 "  `name` text NOT NULL," \
                 "  `strength` text NOT NULL," \
                 "  `agility` text NOT NULL," \
                 "  `armour` text NOT NULL," \
                 "  `luck` text NOT NULL," \
                 "  `health` text NOT NULL," \
                 "  `gold` text NOT NULL," \
                 "  `weapon` text NOT NULL" \
                     ")ENGINE=InnoDB"

    create_room = "CREATE TABLE `room` (" \
                 "  `id` text NOT NULL," \
                 "  `exits` text NOT NULL," \
                  "  `position` text NOT NULL," \
                  "  `roomcard` text NOT NULL" \
                     ")ENGINE=InnoDB"

    create_roomcard = "CREATE TABLE `roomcard` (" \
                 "  `id` text NOT NULL," \
                 "  `cardtype` text NOT NULL," \
                 "  `name` text NOT NULL," \
                    "  `effect` text NOT NULL" \
                     ")ENGINE=InnoDB"

    table = [create_players, create_heroes, create_room, create_roomcard]
    datasheets = [layout_players, layout_heroes, layout_room, layout_roomcard]
    for x in table:
        try:
            cursor.execute(x)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print("here")
                print(err.msg)

    files = ['csv/Drakborgen - players.csv', 'csv/Drakborgen - heroes.csv', 'csv/Drakborgen - room.csv', 'csv/Drakborgen - roomcard.csv']
    i = 0
    for x in datasheets:
        file = open(files[i])
        csv_data = csv.reader(file)
        i += 1
        for row in csv_data:
            cursor.execute(x, row)
            mydb.commit()

def main():
    mydb = mysql.connector.connect(**connection_args)
    cursor = mydb.cursor()

    try:
        cursor.execute("USE {}".format(DB_NAME))
        print("The database for Drakborgen already exists")
    except mysql.connector.Error as err:
        print("Database {} does not exist".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor, DB_NAME)
            print("Database {} created succesfully.".format(DB_NAME))
            mydb.database = DB_NAME
            create_tables(cursor, mydb)
    while True:
        menu(cursor,mydb)


if __name__ == '__main__':
    main()