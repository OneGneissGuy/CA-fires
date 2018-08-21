# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 12:15:59 2018
Scrape a CAL FIRE pdf for historical fire incidents data
@author: JFSARACENO@GMAIL.COM
"""


import pandas as pd
import tabula #tabula requires Java to be installed on Win10

def clean_fire_df(df):
    """func to clean up a dataframe returned by tabula read of CALFire pdf """
    if isinstance(df, pd.DataFrame):
        df.columns = df.iloc[0, :].tolist()
        index_name = 'YEAR'  
        if index_name in df.columns.tolist():
            df.index = df[index_name] # set index 
        cols = ['NUMBER OF FIRES','ACRES BURNED','DOLLAR DAMAGE',]
        if set(cols).issubset(df.columns):
            df2 = df[cols].copy()#drop useless cols
            df2.drop(df.index[0], inplace=True)#cut header
            df2.drop(df.index[-1], inplace=True)#cut footer
            #drop any null values
            df2.drop(df.index[df.index.isna()], inplace=True)
            # remove the asterisks from years and convert strings to an integer
            df2.index = [int(s.replace("*", "")) for s in df2.index.tolist()]
            # convert the index to a datetimeindex
            df2.index = pd.to_datetime(df2.index, format='%Y')
            df2.index.name = index_name
            # remove commas to convert text values to floats, column wise
            for column in df2.columns:
                df2[column] = df2[column].apply(lambda x: float(
                                                x.split()[0].replace(',', '')))        
            return df2
    else:
        raise TypeError("Only valid with pandas Dataframe "
                        "but got an instance of %r" % type(df).__name__)


if __name__ == '__main__':
    #path to input file
    fire_stats_url = 'http://cdfdata.fire.ca.gov/pub/cdf/images/incidentstatsevents_270.pdf'
    # OR if no web connection use:    data/incidentstatsevents_270.pdf
    #path to output data file
    fire_stats_csv = 'data/ca-fire-incidents.csv'
    #join both  dataframes that represent each page
    df_fires = pd.concat([clean_fire_df(tabula.read_pdf(fire_stats_url,
                                                        pages=[1])),    
                          clean_fire_df(tabula.read_pdf(fire_stats_url,
                                                        pages=[2]))])
    # sort the joined dataframe by increasing year
    df_fires.sort_index(ascending=True, inplace=True)
    # write the cleaned up dataframe to a csv file
    df_fires.to_csv(fire_stats_csv, date_format="%Y")
