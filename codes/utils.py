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

"""
Important key value pairs for:
- s level segment mapping
- segment proportions
"""
dictionaries={
    "s_level_mapper":{
        'SoHo (0-9)': 'S1-S3',
        'Small SME (10-49)': 'S4',
        'Small Corporate (100-249)': 'S6',
        'Large SME (50-99)': 'S5',
        'Large Corporate (500-999)': 'S8',
        'Large Corporate (250-499)': 'S7',
        'Large Corporate (1000+)': 'S9-S11',
        'Small corporate (100-249)': 'S6',
        'Large corporate (500-999)': 'S8',
        'Large corporate (250-499)': 'S7',
        'Large corporate (1000+)': 'S9-S11'
    },
    "segment_ratios":{
        "s5":0.368999838,# S5-S6
        "s6":0.631000162,# S5-S6
        "s7":0.397751443,# S7+
        "s8":0.265876633,# S7+
        "s9":0.215739897,# S7+
        "s10":0.120632027# S7+
    },
    "eurostat_segments":{
        'From 0 to 1 person employed':"S1-S3",
        'From 0 to 9 persons employed':"S1-S3",
        'From 2 to 9 persons employed':"S1-S3",
        'From 10 to 19 persons employed':"S4",
        'From 20 to 49 persons employed':"S4",
        'From 50 to 249 persons employed':"S5-S6",
        '250 persons employed or more':"S7+"
    }
}