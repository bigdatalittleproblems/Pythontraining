import os
import pyodbc
import pandas as pd
from pathlib import Path
projwd = Path.cwd()

def dwsqlpull(sqlFile_path: str, outputname: str, rerunquery: bool = False, exportcsv: bool = True,
             odbc_name: str = 'GD_DW_90',output_path=projwd.joinpath("sqlOutput")):
    """:arg sqlFile is a dir to a sql file that you want to run, odbc_name is the name of the ODBC Connection that is
    established on the machine that is running the query. by default it is GD_DW_90
    """
    outputDir=projwd.joinpath('sqlOutput')
    Path.mkdir(outputDir,exist_ok=True)
    outputfile = output_path.joinpath(f'{outputname}.csv')
    print(f"SQL Output will be stored: {outputfile}")
    if outputfile.exists() and not (rerunquery):
        print(f'Skipping the SQL Query\nPulling in Data from: {outputfile}')
        return pd.read_csv(outputfile)
    else:
        # _ = sqlFile_path
        print(f'Application is Running query: {sqlFile_path}')

    try:
        conn = pyodbc.connect(f'DSN={odbc_name};')
        file = open(sqlFile_path, "r")
        sql = file.read()
        file.close()
        # with open ("AttendancePull.sql","r") as file:
        #     AttendanceSQL =file.read()
        df_temp = pd.read_sql_query(sql, con=conn)
        # make a backup
        if exportcsv:
            df_temp.to_csv(outputfile, index=False)
        else:
            pass
        return df_temp
    except Exception as ex:
        print(f'***GOT THE FOLLOWING ERROR in running a SQL Pull: {ex}***')
        return -1
if __name__ == '__main__':
    df=dwsqlpull(sqlFile_path=projwd.joinpath("Session6/sqlQueries/RI.sql"),outputname="RIData20202021",rerunquery=True)