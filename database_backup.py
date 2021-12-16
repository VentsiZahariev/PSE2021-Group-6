#!/usr/bin/python

# Import required python libraries

import os
import time
from datetime import datetime
import pipes
import glob
import shutil
import mariadb as mariadb

import log_message

# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databases names one on each line and assigned to DB_NAME variable.

db_host = "127.0.0.1"
db_port = 3306
db_username = "PSEgroup6"
db_password = "battlefield4"
db_database = "weather_log"
backup_path = '/home/centurio/backup/db-backup'
log_filename = "db_log.out"

log_message.info_log(("Start new database sequence for database: " + db_database), log_filename)

# Getting current DateTime to create the separate backup folder like "20180817-123433".
date_time = datetime.now().strftime('%Y%m%d-%H%M%S')
backup_path_today = backup_path + date_time

# Checking if backup folder already exists or not. If not exists will create it.
log_message.info_log("Check for folders 3 days old and delete them.", log_filename)
folders = glob.glob('/backup/dbbackup/*')
today = datetime.now()
for item in folders:
    try:
        foldername = os.path.split(item)
        day = datetime.strftime(foldername, "%Y%m%d")
        diff = today - day
        if diff.days >= 3:
            shutil.rmtree(item)
    except:
        pass


log_message.info_log("Creating new backup folder", log_filename)
if not os.path.exists(backup_path_today):
    os.makedirs(backup_path_today)

# Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
log_message.info_log("Checking for databases names file.", log_filename)
if os.path.exists(db_database):
    file1 = open(db_database)
    multi = 1
    log_message.info_log("Databases file found...", log_filename)
    log_message.info_log("Starting backup of all dbs listed in file ", log_filename)
else:
    log_message.info_log("Databases file not found...", log_filename)
    log_message.info_log("Starting backup of database ", log_filename)
    multi = 0

# Starting actual database backup process.
try:
    if multi:
        in_file = open(db_database,"r")
        flength = len(in_file.readlines())
        in_file.close()
        p = 1
        dbfile = open(db_database,"r")

        while p <= flength:
            db = dbfile.readline() # reading database name from file
            db = db[:-1] # deletes extra line
            dumpcmd = "mysqldump -h " + db_host + " -u " + db_username + " -p" + db_password + " " + db + " > " + pipes.quote(backup_path_today) + "/" + db + ".sql"
            os.system(dumpcmd)
            p = p + 1
            dbfile.close()
    else:
        db = db_database
        dumpcmd = "mysqldump -h " + db_host + " -u " + db_username + " -p" + db_password + " " + db + " > " + pipes.quote(backup_path_today) + "/" + db + ".sql"
        os.system(dumpcmd)
except mariadb.Error as e:
    # logging a critical error to output file to let the user know a database connection has been lost
    log_message.warning_log(("A missing connection to the database: " + db_database), log_filename)


log_message.info_log("Backup script completed...", log_filename)
log_message.info_log(("Your backups have been created in '" + backup_path_today + "' directory"), log_filename)