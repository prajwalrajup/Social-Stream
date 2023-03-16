import os
import logging


def configure_logging():
    logging.basicConfig(filename=os.path.dirname(os.path.abspath(__file__)) + "/Logger.log",
                        format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
