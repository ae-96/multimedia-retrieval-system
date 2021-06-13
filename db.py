import sqlite3
from sqlite3 import Error
import os

import colorLayout
from meanColor import *
from colorLayout import is_similar_color_layout
from colorLayout import color_layout

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_image(conn, image):
    """
    Create a new image into the images table
    :param conn:
    :param image:
    :return: image id
    """
    sql = ''' INSERT INTO images(path,mean,layout,hist)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, image)
    conn.commit()
    return cur.lastrowid

def get_column(conn,column):
    """
    Query any column for any id in the images table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    query = "SELECT " + column + " FROM images"
    cur.execute(query)

    rows = cur.fetchall()
    if column == "mean" or column == "hist" or column == "layout" :

        for i in range(len(rows)):
            rows[i] = rows[i][0].split()

            for j in range(len(rows[i])):
                if ',' not in rows[i][j]:
                    rows[i][j] = int(rows[i][j])
                else:
                    rows[i][j] = rows[i][j].split(',')
                    for k in range(len(rows[i][j])): rows[i][j][k] = int(rows[i][j][k])


    else :
        for i in range(len(rows)): rows[i] = rows[i][0]

    return rows

sql_create_images_table = """ CREATE TABLE IF NOT EXISTS images (
                                    id integer PRIMARY KEY,
                                    path text NOT NULL,
                                    hist text,
                                    mean text,
                                    layout text
                                ); """

def start_db() :
    # create a database connection
    dbfileexists = os.path.exists("mm.db")
    conn = create_connection(r"mm.db")
    if not dbfileexists:
        # create tables
        if conn is not None:
            # create projects table
            create_table(conn, sql_create_images_table)
        else:
            print("Error! cannot create the database connection.")
    return conn


def apply_algo(path,algo):
    result = []
    if algo == "mean" :
        for i in meanColor(path): result.append(str(i))
    if algo == "hist": pass
    if algo == "layout":
        for i in colorLayout.color_layout(path):
            temp=[]
            for j in i :temp.append((str(j)))
            result.append(','.join(temp))

    return ' '.join(result)

def insert_image(conn ,path):
    with conn :
        mean = apply_algo(path, "mean")
        layout = apply_algo(path, "layout")
        hist = apply_algo(path, "hist")
        image = (path, mean, layout, hist)
        create_image(conn, image)

def search(conn,path,algo):
    result=[]
    if algo == "mean" :
        searchimage = meanColor(path)
        fromdb = get_column(conn,"mean")
        for i in range(len(fromdb)) :
            if isSimilar(searchimage,fromdb[i]) :
                result.append(get_column(conn,"path")[i])

    if algo == "hist": pass
    if algo == "layout":
        searchimage = colorLayout.color_layout(path)
        fromdb = get_column(conn, "layout")
        '''
        print(fromdb)
        print(searchimage)'''
        for i in range(len(fromdb)) :

            if colorLayout.is_similar_color_layout(searchimage,fromdb[i]) :
                result.append(get_column(conn,"path")[i])

    return result

############# test ######################

conn = start_db()   # call at the start of gui

path = "G:\\4th cse\sec term\multimedia\proj\\1.png"
insert_image(conn,path)
result = search(conn,path,"layout")
print(result)





