#!/usr/bin/python3

# logger.py
# Last edit made: 10-12-2021
# Version: 0.1
# Subject: Logs error messages to a output file to catch crashes and failures
# Author: Tim ter Steege
# python version used: 3.9

import logging


def info_log(message, filename):
    try:
        log_format = "%(levelname)s: [%(asctime)s] - %(message)s"
        logging.basicConfig(filename=filename,
                            filemode="a",
                            format=log_format,
                            level=logging.INFO)
        logger = logging.getLogger()
        logger.info(message)

    except AttributeError as e:
        print("Error: ", e)


def warning_log(message, filename):
    try:
        log_format = "%(levelname)s: [%(asctime)s] - %(message)s"
        logging.basicConfig(filename=filename,
                            filemode="a",
                            format=log_format,
                            level=logging.WARNING)
        logger = logging.getLogger()
        logger.warning(message)

    except AttributeError as e:
        print("Error: ", e)


def error_log(message, filename):
    try:
        log_format = "%(levelname)s: [%(asctime)s] - %(message)s"
        logging.basicConfig(filename=filename,
                            filemode="a",
                            format=log_format,
                            level=logging.ERROR)
        logger = logging.getLogger()
        logger.error(message)

    except AttributeError as e:
        print("Error: ", e)


def critical_log(message, filename):
    try:
        log_format = "%(levelname)s: [%(asctime)s] - %(message)s"
        logging.basicConfig(filename=filename,
                            filemode="a",
                            format=log_format,
                            level=logging.CRITICAL)
        logger = logging.getLogger()
        logger.critical(message)

    except AttributeError as e:
        print("Error: ", e)