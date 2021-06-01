# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 09:48:58 2020

@author: christian.ramirez
Script requires that CDE_webscrape_Class project is in the same DIR
"""
import os
import pandas as pd
from CDE_webscrape_Class import CDE_WebScrapeSelenium, ReportNames
from TableStack import tableStack, unstagedReportsDic, loadCsvData, overallStack
from StageTableProcessing import prestagetable, StageTable, stagetablemelt, updatedStackingFunction
import cowsay
from datetime import timedelta
import time
projectWD = os.getcwd()

# UPDATES
# You can update the school year below
SchoolYear_CDE = ['2020-21','2019-20', '2018-19', '2017-18', '2016-17', '2015-16', '2014-15', '2013-14']
# this is the file that reads in the School Data to scrape. If you want to change the schools, you can open this document and add rows of data.
# Note. the file is a txt file because if you open and save it as a csv, Exel can change CDS codes to scientific notation.
CDE_School_List = pd.read_csv(os.path.join(projectWD, 'Resources', 'CDE_SchoolScrapeList.txt'), sep='\t')

projectWD = os.getcwd()
path_Output = os.path.join(projectWD, 'ReportOutput')
if os.path.exists(path_Output):
    print(f'path {path_Output} exists')
else:
    print(f'Creating Path: {path_Output}')
    os.mkdir(path_Output)
raceMapping_raw = pd.read_csv(os.path.join(projectWD, 'Resources', 'RaceMapping.txt'), sep='\t')
raceMappingCA = raceMapping_raw[raceMapping_raw.Region == 'CA']
raceMappingCA.reset_index(drop=True, inplace=True)

# importing Report variables from the class
reports = ReportNames()
susReport = reports.availableReports['suspensionReports']
dataReportTypes = reports.dataTypeOptions

#############################################
# locally defined method to Scrape data.
# CDSList must be a list,
# SchoolYear_CDE can be a string or a  list. there is a test to convert it back into a list.
# susReport must be a list
# repType must be a text string

ReportSubgroupsFilters = reports.availableSubgroups
def dirCreate(dir):
    try:
        if os.path.isdir(dir):
            print(f'Dir Exists: {dir}')
            pass
        else:
            os.mkdir(dir)
    except:
        cowsay.ghostbusters(f'{dir} is not an acceptable directory')


def suspensionDataLoop(CDSList=CDE_School_List['CDS'], SchoolYear_CDE=SchoolYear_CDE, susReport=susReport,
                       repType=dataReportTypes[0]):
    suspension = CDE_WebScrapeSelenium()
    suspension.setup_method()
    if type(SchoolYear_CDE) != list:
        SchoolYear_CDE = [SchoolYear_CDE]
    Stack = {}
    try:
        for sy in SchoolYear_CDE:
            for cds in CDSList:
                for rep in susReport:
                    for subGroup in ReportSubgroupsFilters:
                        if repType == 'programSubgroup':
                            temp = suspension.scrapeSuspension(SchoolYear_CDE=sy, SchoolCDS=cds, susRep=rep,
                                                               dataTypeOptions=repType, reportFilter=subGroup)
                            if temp != None:
                                cowsay.daemon(f'Creating Error Log record for {temp}')
                                with open('Fail_log.txt', 'a') as fl:
                                    fl.write(f'{temp} \n')
                            # break subgroup loop to only run once
                            break
                        else:
                            temp = suspension.scrapeSuspension(SchoolYear_CDE=sy, SchoolCDS=cds, susRep=rep,
                                                               dataTypeOptions=repType, reportFilter=subGroup)
                            if temp != None:
                                cowsay.daemon(f'Creating Error Log record for {temp}')
                                with open('Fail_log.txt', 'a') as fl:
                                    fl.write(f'{temp} \n')
        suspension.teardown_method()
        return Stack
    except Exception as ex:
        cowsay.tux('Error!!!!')
        print(f'***GOT THE FOLLOWING ERROR: {ex}***')
        print('Error in suspensionDataLoop function')


def chronAbsDataLoop(CDSList=CDE_School_List['CDS'], SchoolYear_CDE=SchoolYear_CDE, repType=dataReportTypes[0]):
    chronAbs = CDE_WebScrapeSelenium()
    chronAbs.setup_method()
    if type(SchoolYear_CDE) != list:
        SchoolYear_CDE = [SchoolYear_CDE]
    Stack = {}
    try:
        for sy in SchoolYear_CDE:
            for cds in CDSList:
                for subGroup in ReportSubgroupsFilters:
                    if repType == 'programSubgroup':
                        temp = chronAbs.scrapeChronAbs(SchoolYear_CDE=sy, SchoolCDS=cds, dataTypeOptions=repType,
                                                       reportFilter='All Students')
                        if temp != None:
                            cowsay.daemon(f'Creating Error Log record for {temp}')
                            with open('Fail_log.txt', 'a') as fl:
                                fl.write(f'{temp} \n')
                        # break subgroup loop to only run once
                        break
                    else:
                        temp = chronAbs.scrapeChronAbs(SchoolYear_CDE=sy, SchoolCDS=cds, dataTypeOptions=repType,
                                                       reportFilter=subGroup)
                        if temp != None:
                            cowsay.daemon(f'Creating Error Log record for {temp}')
                            with open('Fail_log.txt', 'a') as fl:
                                fl.write(f'{temp} \n')
        chronAbs.teardown_method()
    except Exception as ex:
        cowsay.tux("Error!!!")
        print(f'***GOT THE FOLLOWING ERROR When running chronAbsDataLoop: {ex}***')
        print('Error in chronAbsDataLoop function Returnin None ')

def gradRatesDataLoop(CDSList=CDE_School_List['CDS'], SchoolYear_CDE=SchoolYear_CDE, repType=dataReportTypes[0]):
    chronAbs = CDE_WebScrapeSelenium()
    chronAbs.setup_method()
    if type(SchoolYear_CDE) != list:
        SchoolYear_CDE = [SchoolYear_CDE]
    Stack = {}
    try:
        for sy in SchoolYear_CDE:
            for cds in CDSList:
                for subGroup in ReportSubgroupsFilters:
                    if repType == 'programSubgroup':
                        temp = chronAbs.scrapeGradRates(SchoolYear_CDE=sy, SchoolCDS=cds, dataTypeOptions=repType,
                                                       reportFilter='All Students')
                        if temp != None:
                            cowsay.daemon(f'Creating Error Log record for {temp}')
                            with open('Fail_log.txt', 'a') as fl:
                                fl.write(f'{temp} \n')
                        # break subgroup loop to only run once
                        break
                    else:
                        temp = chronAbs.scrapeGradRates(SchoolYear_CDE=sy, SchoolCDS=cds, dataTypeOptions=repType,
                                                       reportFilter=subGroup)
                        if temp != None:
                            cowsay.daemon(f'Creating Error Log record for {temp}')
                            with open('Fail_log.txt', 'a') as fl:
                                fl.write(f'{temp} \n')
        chronAbs.teardown_method()
    except Exception as ex:
        cowsay.tux("Error!!!")
        print(f'***GOT THE FOLLOWING ERROR When running chronAbsDataLoop: {ex}***')
        print('Error in gradRatesDataLoop function Returnin None ')


def enrollDataLoop(CDSList=CDE_School_List['CDS'], SchoolYear_CDE=SchoolYear_CDE, repType=dataReportTypes[0]):
    chronAbs = CDE_WebScrapeSelenium()
    chronAbs.setup_method()
    if type(SchoolYear_CDE) != list:
        SchoolYear_CDE = [SchoolYear_CDE]
    Stack = {}
    try:
        for sy in SchoolYear_CDE:
            for cds in CDSList:
                for subGroup in ReportSubgroupsFilters:
                    if repType == 'programSubgroup':
                        temp = chronAbs.scrapeEnroll(SchoolYear_CDE=sy, SchoolCDS=cds, dataTypeOptions=repType,
                                                       reportFilter='All Students')
                        if temp != None:
                            cowsay.daemon(f'Creating Error Log record for {temp}')
                            with open('Fail_log.txt', 'a') as fl:
                                fl.write(f'{temp} \n')
                        # break subgroup loop to only run once
                        break
                    else:
                        temp = chronAbs.scrapeEnroll(SchoolYear_CDE=sy, SchoolCDS=cds, dataTypeOptions=repType,
                                                       reportFilter=subGroup)
                        if temp != None:
                            cowsay.daemon(f'Creating Error Log record for {temp}')
                            with open('Fail_log.txt', 'a') as fl:
                                fl.write(f'{temp} \n')
        chronAbs.teardown_method()
    except Exception as ex:
        cowsay.tux("Error!!!")
        print(f'***GOT THE FOLLOWING ERROR When running chronAbsDataLoop: {ex}***')
        print('Error in gradRatesDataLoop function Returnin None ')


def adjCohortOutcomesDataLoop(CDSList=CDE_School_List['CDS'], SchoolYear_CDE=SchoolYear_CDE, repType=dataReportTypes[0]):
    obj = CDE_WebScrapeSelenium()
    obj.setup_method()
    if type(SchoolYear_CDE) != list:
        SchoolYear_CDE = [SchoolYear_CDE]
    Stack = {}
    try:
        for sy in SchoolYear_CDE:
            for cds in CDSList:
                for subGroup in ReportSubgroupsFilters:
                    if repType == 'programSubgroup':
                        temp = obj.adjCohortOutcomes(SchoolYear_CDE=sy, SchoolCDS=cds, dataTypeOptions=repType,
                                                       reportFilter='All Students')
                        if temp != None:
                            cowsay.daemon(f'Creating Error Log record for {temp}')
                            with open('Fail_log.txt', 'a') as fl:
                                fl.write(f'{temp} \n')
                        # break subgroup loop to only run once
                        break
                    else:
                        temp = obj.adjCohortOutcomes(SchoolYear_CDE=sy, SchoolCDS=cds, dataTypeOptions=repType,
                                                       reportFilter=subGroup)
                        if temp != None:
                            cowsay.daemon(f'Creating Error Log record for {temp}')
                            with open('Fail_log.txt', 'a') as fl:
                                fl.write(f'{temp} \n')
        obj.teardown_method()
    except Exception as ex:
        cowsay.tux("Error!!!")
        print(f'***GOT THE FOLLOWING ERROR When running chronAbsDataLoop: {ex}***')
        print('Error in gradRatesDataLoop function Returnin None ')

# locally defined method to stack data. It takes in a data dictionary that is the output of the suspensionDataLoop method
def StackTables(DataDictionary):
    FinalDataTables = []
    for j in range(0, len(DataDictionary[list(DataDictionary.keys())[0]])):
        stackDoc = []
        for d in DataDictionary:
            DataDictionary[d][j]['DataID'] = d
            stackDoc.append(DataDictionary[d][j])
        FinalDataTables.append(pd.concat(stackDoc))
    for i in range(0, len(FinalDataTables)):
        FinalDataTables[i].reset_index(drop=True, inplace=True)
    return FinalDataTables


def startSusProcess():
    # Start of Suspension Scrape process
    print('Starting first Suspension Scrape')
    suspensionDataLoop(CDSList=CDE_School_List['CDS'], SchoolYear_CDE=SchoolYear_CDE[:4],susReport=susReport, repType=dataReportTypes[0])
    print('Starting Second Suspension Scrape')
    suspensionDataLoop(CDSList=CDE_School_List['CDS'], SchoolYear_CDE=SchoolYear_CDE[:4],
                       susReport=susReport, repType=dataReportTypes[1])
    print('Starting Suspension teardown_method()')
    # suspension.teardown_method()
    # return CompSusDataEthnicity, CompSusDatasubGroup
def scrapeDataLoop(CDSList=CDE_School_List['CDS'], SchoolYear_CDE=SchoolYear_CDE,repType=dataReportTypes[0],funcClass=CDE_WebScrapeSelenium()):
    # suspension = CDE_WebScrapeSelenium()
    funcClass.setup_method()
    if type(SchoolYear_CDE) != list:
        SchoolYear_CDE = [SchoolYear_CDE]
    Stack = {}
    try:
        for sy in SchoolYear_CDE:
            for cds in CDSList:
                for subGroup in ReportSubgroupsFilters:
                    if repType == 'programSubgroup':
                        temp = funcClass.agGradRates(SchoolYear_CDE=sy, SchoolCDS=cds,dataTypeOptions=repType, reportFilter=subGroup)
                        if temp != None:
                            cowsay.daemon(f'Creating Error Log record for {temp}')
                            with open('Fail_log.txt', 'a') as fl:
                                fl.write(f'{temp} \n')
                        # break subgroup loop to only run once
                        break
                    else:
                        temp = funcClass.agGradRates(SchoolYear_CDE=sy, SchoolCDS=cds,dataTypeOptions=repType, reportFilter=subGroup)
                        if temp != None:
                            cowsay.daemon(f'Creating Error Log record for {temp}')
                            with open('Fail_log.txt', 'a') as fl:
                                fl.write(f'{temp} \n')
        funcClass.teardown_method()
        return Stack
    except Exception as ex:
        cowsay.tux('Error!!!!')
        print(f'***GOT THE FOLLOWING ERROR: {ex}***')
        print('Error in suspensionDataLoop function')

def startadjCohortOutcomes():
    # Start of Suspension Scrape process
    print('Starting Graduation Scrape')
    adjCohortOutcomesDataLoop(CDSList=CDE_School_List['CDS'], SchoolYear_CDE=SchoolYear_CDE[:4], repType=dataReportTypes[0])
    adjCohortOutcomesDataLoop(CDSList=CDE_School_List['CDS'], SchoolYear_CDE=SchoolYear_CDE[:4], repType=dataReportTypes[1])

def startEnrollment():
    # Start of Suspension Scrape process
    print('Starting Graduation Scrape')
    enrollDataLoop(CDSList=CDE_School_List['CDS'], SchoolYear_CDE=SchoolYear_CDE[:4], repType=dataReportTypes[0])
    enrollDataLoop(CDSList=CDE_School_List['CDS'], SchoolYear_CDE=SchoolYear_CDE[:4], repType=dataReportTypes[1])

def startChronAbsProcess():
    print('Starting Chron Abs')
    print('Starting Chron Abs by Ethnicity')
    chronAbsDataLoop(CDSList=CDE_School_List['CDS'], SchoolYear_CDE=SchoolYear_CDE[:4],repType=dataReportTypes[0])
    print('Starting Chron Abs by SubGroup')
    chronAbsDataLoop(CDSList=CDE_School_List['CDS'], SchoolYear_CDE=SchoolYear_CDE[:4],repType=dataReportTypes[1])

def startGradRatesProcess():
    print('Starting GradRates')
    print('Starting GradRates by Ethnicity')
    gradRatesDataLoop(CDSList=CDE_School_List['CDS'], SchoolYear_CDE=SchoolYear_CDE[:4], repType=dataReportTypes[0])
    print('Starting GradRates by SubGroup')
    gradRatesDataLoop(CDSList=CDE_School_List['CDS'], SchoolYear_CDE=SchoolYear_CDE[:4], repType=dataReportTypes[1])


if __name__ == '__main__':
    startTime = time.perf_counter()
    # Start of ChronAbs Scrape process
    startEnrollment()
    startadjCohortOutcomes()
    startGradRatesProcess()
    startSusProcess()
    startChronAbsProcess()
    # this takes all of the files in the ./ReportOutput Dir and stacks them based on Folder names. The value returns a Dic with the name of the table and the path to the file as the Key value pair.
    unstagedReports = tableStack()
    # this takes the data dic that was generated above, and reads the files into the Dic.
    ReportsDic = unstagedReportsDic(unstagedReports)

    # preData = loadCsvData()
    finalData = prestagetable(ReportsDic)
    stagedData = StageTable(finalData)
    OutputFinalDir = os.path.join(projectWD, 'ReportOutputFinal')
    dirCreate(OutputFinalDir)
    tempStack=overallStack(stagedData)
    tempStack.to_csv(os.path.join(OutputFinalDir, 'FinalStaged.csv'),index=False)
    updatedStackingFunction()
    for i in stagedData:
        filename = os.path.join(OutputFinalDir, f'{i}_Staged.csv')
        stagedData[i].to_csv(filename,index=False)
    endTime = time.perf_counter()
    totalTime=(endTime-startTime)
    totalTimeSec=str(timedelta(seconds=totalTime))
    print(f'Total time to run script is: {totalTimeSec}')