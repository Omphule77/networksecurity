import sys
from networksecurity.logging.logger import logging

class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_detail:sys):
        self.error_message=error_message
        _,_,exc_tb=error_detail.exc_info()
        self.lineno=exc_tb.tb_lineno
        self.filename=exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occurred in python script name [{self.filename}] line number [{self.lineno}] error message[{str(self.error_message)}]"
        
if __name__ == "__main__":
    try:
        logging.info("Starting the Try block")
        a=1/0
    except Exception as e:
        logging.info(e)
        raise NetworkSecurityException(e,sys)