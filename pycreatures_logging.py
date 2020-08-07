
from logging import *
import sys, os
import traceback

def setupLogging(log_file, level):

    basicConfig(filename=log_file, level=level, format='%(asctime)s %(message)s')



def logException(msg):
    # Log full exception information

    def indent(str):
        result = ""
        lines = str.split("\n")
        for line in lines:
            result += "\t\t" + line + "\n"
        return result

    # Log exception
    err = msg + "\n" + indent(traceback.format_exc())

    error(err)

    '''
    # Grab Python information and log that too
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    error("--> Python Exception type {} at line {} in file {} ".format(exc_type, exc_tb.tb_lineno, fname))    
    '''

