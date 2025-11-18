import logging
import pandas as pd

di_ratios=pd.DataFrame(
    data=[
        ['Germany', 1.0, 1.0, 1.0],
       ['UK', 1.0922707164144592, 1.1372549019607845, 1.2076641574615246],
       ['Turkey', 0.7789346740000642, 0.67116002968093,0.5024711365464143],
       ['Albania', 0.660296005251697, 0.49468216670789017,0.23546335612209424],
       ['South Africa', 0.7318782713991, 0.6011625030917636,0.39656615846641063],
       ['Czechia', 0.8924357222705253, 0.8609458189790166,0.753099173553719],
       ['Ireland', 0.9207551856912184, 0.9364234262449107,1.1590909090909092],
       ['Greece', 0.6713451745124829, 0.5111180707798308,0.3274793388429752],
       ['Netherlands', 1.0117997764252886, 1.057626056999687,1.2530991735537191],
       ['Portugal', 0.9289529251024717, 0.9470717193861572,0.8109504132231404],
       ['Romania', 0.8680909203825611, 0.6414030692139054,0.2603305785123967]
    ],
    columns=["Country","Mature product","Growing product","Emerging product"]
)

class Eurostat:
    def __init__(self):
        """
        All the Aurostat related data processing methods.
        """
        pass

    def sheet_finder(sheet:str,filepath:str,n=8)->bool:
        """
        Flag sheets that contain relevant information.

        Parameters:
        - sheet, str of the sheet name
        - filepath, str of the excel file downloaded from Eurostat
        - n, int the number of rows to skip as these sheets usually contain unnecessary rows

        Returns:
        - boolean flag whether a particular sheet is necessary or NOT
        """
        df=pd.read_excel(
            io=filepath,
            sheet_name=sheet,
            nrows=n
        )
        try:
            if ("Sheet" in sheet) and ("Enterprises - number" in df["Unnamed: 2"].values) and ("Total" not in df["Unnamed: 2"].values):
                return True
            else:
                return False
        except:
            return False
        
    def sheet_reader(sheet:str,filepath:str)->pd.DataFrame:
        """
        Read the sheets that were flagged by the sheet_finder method.

        Parameters:
        - sheet, str of the sheet name
        - filepath, str of the excel file downloaded from Eurostat

        Returns:
        - DataFrame of the sheet
        """
        df=pd.read_excel(
            io=filepath,
            sheet_name=sheet
        )
        segment=df.iloc[6]["Unnamed: 2"]
        columns=df.iloc[8].dropna()
        columns=["country"]+list(columns[columns!="TIME"].values)
        
        df=df.iloc[11:46].dropna(axis=1)
        df.columns=columns
        df["segment"]=segment
        df=df.apply(lambda col: col.replace(":",np.nan),axis=1)
        return df

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

def segment_mapper(segment:str,transform_table:pd.DataFrame)->str:
    """
    Simple function to get segment mapping.

    Paramter(s):
    - segment, str
    - transform_table, pd.DataFrame

    Returns:
    - mapped_segment, str
    """
    subdf=transform_table[transform_table["From"]==segment]
    mapped_segments=subdf["To"].values
    exact_match=segment in mapped_segments
    if len(mapped_segments)==0:
        return [exact_match,segment]
    elif len(mapped_segments)==1:
        return [exact_match,mapped_segments[0]]
    else:
        return [exact_match,';'.join(mapped_segments)]

"""
Important key value pairs for:
- s level segment mapping
- segment proportions
"""
dictionaries={
    "s_level_mapper":{
        'SoHo (0-9)': 's1-s3',
        'Small SME (10-49)': 's4',
        'Small Corporate (100-249)': 's6',
        'Large SME (50-99)': 's5',
        'Large Corporate (500-999)': 's8',
        'Large Corporate (250-499)': 's7',
        'Large Corporate (1000+)': 's9-s11',
        'Small corporate (100-249)': 's6',
        'Large corporate (500-999)': 's8',
        'Large corporate (250-499)': 's7',
        'Large corporate (1000+)': 's9-s11'
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
        'From 0 to 1 person employed':"s1-s3",
        'From 0 to 9 persons employed':"s1-s3",
        'From 2 to 9 persons employed':"s1-s3",
        'From 10 to 19 persons employed':"s4",
        'From 20 to 49 persons employed':"s4",
        'From 50 to 249 persons employed':"s5-s6",
        '250 persons employed or more':"s7+"
    }
}