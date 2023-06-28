"""
Subprocess wrapper file contains all api related to Subprocess module
"""
import subprocess
import logging


def run_cmd_get_output(query):
    """
    This api will run the provided query on command line
    :param query: Query to be run on cmd
    :return: Output of query
    """
    try:
        output = subprocess.getoutput(query)
        return output
    except Exception as e:
        logging.error(f"run_cmd_get_output() - failed to run the query : {query}")
        logging.exception(e)


def run_cmd_call(query):
    """
    This api will run the provided query on command line
    :param query: Query to be executed on cmd
    """
    try:
        subprocess.call(query, shell=True)
    except Exception as e:
        logging.error(f"run_cmd_call() - failed to run the query : {query}")
        logging.exception(e)


def run_cmd_call_runtime(query):
    """
    This api will run the provided query on command line
    :param query: Query to be executed on cmd
    """
    try:
        logging.debug(subprocess.call(query, shell=True))
    except Exception as e:
        logging.error(f"run_cmd_call() - failed to run the query : {query}")
        logging.exception(e)


def cmd_run(query, timeout=None):
    """
    This api will run the provided query on command line
    :param timeout: maximum time to wait before terminating the command
    :param query: Query to be executed on cmd
    """
    try:
        return subprocess.run(query, shell=True, stderr=True, stdout=True, timeout=timeout)
    except Exception as e:
        logging.error(f"cmd_run() - failed to run the query : {query}")
        logging.exception(e)


def cmd_run_display_output(query):
    """
    This api will run the provided query on command line
    :param query: Query to be executed on cmd
    """
    try:
        return subprocess.run(query, capture_output=True, text=True, shell=True)
    except Exception as e:
        logging.error(f"cmd_run_display_output() - failed to run the query : {query}")
        logging.exception(e)

