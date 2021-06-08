from pathlib import Path
from Session6.custom_modules.dwpull import dwsqlpull


# Exercise, I want to see the average RI growth for students at Locke for all School Years and Tested Grade Levels.
# I need you to provide me with a final document that includes all this data :)

# NOTES: we need to filter to only include scores where student took two tests at least 6 months apart.

projwd = Path.cwd()
df=dwsqlpull(sqlFile_path=projwd.joinpath("Session6/sqlQueries/RI.sql"),outputname="RIData20202021")