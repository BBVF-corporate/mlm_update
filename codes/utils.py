import logging

def loggerConfig(logfile:str)->None:
    """
    Setting up the logging structure.

    Parameters:
    - logfile:str, filepath of the logfile

    Returns:
    - None
    """
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        filemode='a',
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )