from pathlib import Path
from Session6.custom_modules.dwpull import dwsqlpull


# Exercise, I want to see the average RI growth for students at Locke for all School Years and Tested Grade Levels.
# I need you to provide me with a final document that includes all this data :)

# NOTES: we need to filter to only include scores where student took two tests at least 6 months apart.

projwd = Path.cwd()
df=dwsqlpull(sqlFile_path=projwd.joinpath("Session6/sqlQueries/RI.sql"),outputname="RIData20202021")

df['FirstTestSchool'].unique()
df.columns
# iloc vs loc

df_iloc=df[df['FirstTestSchool']=='Locke Academy'].index
df.iloc[df_iloc]

df_drf=df.loc[(df['FirstTestSchool']=='Locke Academy')&(df['MonthsBetweenFirstLast']>5)]
df_drf=df_drf[['schoolyear', 'FirstTestSchool', 'TestGradeLevel', 'FirstRIDate',
       'FirstRIScore', 'MidRIDate', 'MidRIScore', 'LastRIDate', 'LastRIScore',
       'HighestDate', 'HighestScore', 'TwoTests', 'MonthsBetweenFirstLast',
       'HasMidYearTest', 'Growth_FirstLast', 'AdjustedGrowth_FirstLast',
       'Growth_FirstHighest', 'AdjustedGrowth_FirstHighest']]

df_summary=df_drf.groupby(['schoolyear','TestGradeLevel']).mean().reset_index()