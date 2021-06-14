import sqlite3
import threading
from sqlite3 import Error


import colorLayout
from meanColor import *
from video_algorithm import *
from histogram import *

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


def create_video(conn, video):
    """
    Create a new video into the videos table
    :param conn:
    :param video:
    :return: video id
    """
    sql = ''' INSERT INTO videos(path,cbvr)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, video)
    conn.commit()
    return cur.lastrowid


def get_column_from_image(conn, column):
    """
    Query any columnin images table
    :param conn: the Connection object
    :param column: the required column
    :return: 1D or 2D or 3D list
    """
    cur = conn.cursor()
    query = "SELECT " + column + " FROM images"
    cur.execute(query)
    rows = cur.fetchall()
    if column == "mean" or column == "hist" or column == "layout":
        for i in range(len(rows)):
            rows[i] = rows[i][0].split()
            for j in range(len(rows[i])):
                if ',' not in rows[i][j]:
                    rows[i][j] = int(rows[i][j])
                else:
                    rows[i][j] = rows[i][j].split(',')
                    for k in range(len(rows[i][j])): rows[i][j][k] = int(rows[i][j][k])
    else:
        for i in range(len(rows)): rows[i] = rows[i][0]
    return rows


def get_cbvr(conn, column):
    """
        Query any column  in the videos table
        :param conn: the Connection object
        :param column: the required column
        :return: 1D or 2D or 3D list
        """
    cur = conn.cursor()
    query = "SELECT " + column + " FROM videos"
    cur.execute(query)
    rows = cur.fetchall()
    if column == "cbvr":
        for i in range(len(rows)):
            rows[i] = rows[i][0].split()
            for j in range(len(rows[i])):
                rows[i][j] = rows[i][j].split(',')
                for k in range(len(rows[i][j])): rows[i][j][k] = int(rows[i][j][k])

    else:
        for i in range(len(rows)): rows[i] = rows[i][0]
    return rows


sql_create_images_table = """ CREATE TABLE IF NOT EXISTS images (
                                    id integer PRIMARY KEY,
                                    path text NOT NULL,
                                    hist text,
                                    mean text,
                                    layout text
                                ); """

sql_create_videos_table = """ CREATE TABLE IF NOT EXISTS videos (
                                    id integer PRIMARY KEY,
                                    path text NOT NULL,
                                    cbvr text
                                ); """


def start_db():
    # create a database connection
    dbfileexists = os.path.exists("mm.db")
    conn = create_connection(r"mm.db")
    if not dbfileexists:
        # create tables
        if conn is not None:
            # create projects table
            create_table(conn, sql_create_images_table)
            create_table(conn, sql_create_videos_table)
        else:
            print("Error! cannot create the database connection.")
    return conn


def apply_algo(path, algo):
    result = []
    if algo == "mean":
        for i in meanColor(path): result.append(str(i))
    if algo == "hist":
        for i in find_hisogram(path): result.append(str(i))
    if algo == "layout":
        for i in colorLayout.color_layout(path):
            temp = []
            for j in i: temp.append((str(j)))
            result.append(','.join(temp))

    return ' '.join(result)


def apply_cbvr(path):
    result = []
    for i in keyFrames_meanColor(path):
        temp = []
        for j in i: temp.append((str(j)))
        result.append(','.join(temp))
    return ' '.join(result)


def insert_image(conn, path):

    with conn:
        mean = apply_algo(path, "mean")

        layout = apply_algo(path, "layout")
        print(threading.current_thread())

        hist = apply_algo(path, "hist")
        print("end")
        image = (path, mean, layout, hist)

        create_image(conn, image)



def inser_video(conn, path):
    with conn:
        cbvr = apply_cbvr(path)
        vid = (path, cbvr)
        create_video(conn, vid)


def search_image(conn, path, algo):
    result = []
    if algo == "mean":
        searchimage = meanColor(path)
        fromdb = get_column_from_image(conn, "mean")
        for i in range(len(fromdb)):
            if isSimilar(searchimage, fromdb[i]):
                result.append(get_column_from_image(conn, "path")[i])
    if algo == "hist":
        searchimage = find_hisogram(path)
        fromdb = get_column_from_image(conn, "hist")
        for i in range(len(fromdb)):
            if isSimilarr(searchimage, fromdb[i]):
                result.append(get_column_from_image(conn, "path")[i])
    if algo == "layout":
        searchimage = colorLayout.color_layout(path)
        fromdb = get_column_from_image(conn, "layout")
        for i in range(len(fromdb)):
            if colorLayout.is_similar_color_layout(searchimage, fromdb[i]):
                result.append(get_column_from_image(conn, "path")[i])
    return result


def search_video(conn, path):
    result = []

    if(path[-4:]=='.mp4'):
        search_video = keyFrames_meanColor(path)
        fromdb = get_cbvr(conn, "cbvr")
        for i in range(len(fromdb)):
            if is_videos_similar(search_video, fromdb[i]):
                result.append(get_cbvr(conn, "path")[i])
    else:
        search_video = meanColor(path)
        fromdb = get_cbvr(conn, "cbvr")
        for i in range(len(fromdb)):
            if is_frame_in_video(search_video, fromdb[i]):
                result.append(get_cbvr(conn, "path")[i])
    return result


############# test ######################
'''
conn = start_db()  # call at the start of gui



path = "G:\\4th cse\\sec term\\multimedia\\proj\\1.png"
insert_image(conn, path)
result = search_image(conn, path, "hist")
print(result)

conn = start_db()  # call at the start of gui
vid_path = "E:\\forth year\\image\PROJECT\\videos\\0.mp4"
vid_path1 = "E:\\forth year\\image\PROJECT\\videos\\1.mp4"
inser_video(conn,vid_path)
inser_video(conn,vid_path1)
vidresult = search_video(conn,vid_path)
print(vidresult)
'''