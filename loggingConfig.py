import logging

def configure_logging():
    logging.basicConfig(filename = "Logger.log", format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
