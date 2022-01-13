#!/usr/bin/python3

# logger.py
# Last edit made: 13-01-2022
# Version: 0.2
# Description: Logs error messages to a output file to catch crashes and failures
# Author: Tim ter Steege
# python version used: 3.9

# Import required python libraries
import logging

# global variable to hold the name of the output file
filename = "mqtt_log.out"

def info_log(message):
    """
    logs a message to an output file with info tag
    form of message:  INFO: [datetime] - message
    """
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


def warning_log(message):
    """
    logs a message to an output file with warning tag
    form of message:  WARNING: [datetime] - message
    """
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


def error_log(message):
    """
    logs a message to an output file with error tag
    form of message:  ERROR: [datetime] - message
    """
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


def critical_log(message):
    """
    logs a message to an output file with critical tag
    form of message:  CRITICAL: [datetime] - message
    """
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