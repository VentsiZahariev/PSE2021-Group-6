#!/usr/bin/python3

# logger.py
# Last edit made: 10-12-2021
# Version: 0.1
# Subject: Code to retrieve data from the things network and store it to the database
# Author: Tim ter Steege
# python version used: 3.9

import logging

class log:
    try:
        def error_log(message):
            log_format = "%(levelname)s %(asctime)s - %(message)s"

            logging.basicConfig(filename="logfile.out",
                                filemode="a",
                                format= log_format,
                                level = logging.ERROR)

            logger = logging.getLogger()

            logger.error(message)
    except AttributeError as e:
        print(f"Error: {e}")


    def debug_log(message):
        try:
            log_format = "%(levelname)s %(asctime)s - %(message)s"

            logging.basicConfig(filename="logfile.out",
                                filemode="a",
                                format=log_format,
                                level=logging.DEBUG)

            logger = logging.getLogger()

            logger.error(message)
        except AttributeError as e:
            print(f"Error: {e}")