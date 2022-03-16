import csv
from mysql.connector import errorcode
import mysql.connector

connection_args = {
    "host": "localhost",
    "user": "root",
    "password": "root"
}
DB_NAME = "drakborgen"

def new_player(cursor):
    name = input("Enter the players name")
    age = input("Enter the player age")
    while True:
        hero = input("Enter a number 1-4 to pik a hero")
        string = "SELECT name FROM players WHERE name ='" + hero + "'"
        print(string)
        cursor.execute(string)
        result = str(cursor.fetchall())
        print(result)




def create_database(cursor, mydb):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Faild to create database {}".format(err))
        exit(1)

def menu(cursor):
    print("DRAKBORGEN_______________")
    print("1. Create new player")
    print("2. List all players and their hero")
    print("3 Do a round")
    ans = input()
    if ans == "1":
        new_player(cursor)


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
        else:
            print("OK")

    files = ['csv/Drakborgen - players.csv', 'csv/Drakborgen - heroes.csv', 'csv/Drakborgen - room.csv', 'csv/Drakborgen - roomcard.csv']
    i = 0
    for x in datasheets:
        print(x)
        file = open(files[i])
        csv_data = csv.reader(file)
        i += 1
        for row in csv_data:
            print(row)
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
    menu(cursor)


if __name__ == '__main__':
    main()