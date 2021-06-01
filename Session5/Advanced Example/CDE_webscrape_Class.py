# -*- coding: utf-8 -*-
"""
Required Python packages are:  selenium pandas xlrd numpy openpyxl xlrd lxml "pip install pandas xlrd numpy openpyxl xlrd lxml"

Created on Tue Mar 17 16:22:57 2020

@author: christian.ramirez
This is refrenced by the Webscrape final script to import classes, and this works as a single source to edit and add future pulls from.
"""
import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import cowsay
from pathlib import Path

projwd = Path.cwd()
pathToDriver = projwd.joinpath('ChromeDriver', 'chromedriver.exe')
projectWD = os.getcwd()
compSchools = pd.read_csv(os.path.join(projectWD, 'Resources', 'CompSchoolAltSchoolID.txt'), sep='\t')




class ReportNames():
    def __init__(self):
        self.availableReports = {
            'suspensionReports': ['ALL', 'OSS', 'ISS'],
            'reclassRate': [],
            'ChronAbs': []
        }
        self.availableBreakdown = {
            'report': ['ethnicity', 'programSubgroup', 'academicYear']
        }
        self.availableSubgroups = ['All Students', 'Male', 'Female', 'EL', 'Non-EL', 'SWD', 'Non-SWD']
        self.SchoolYear_CDE = ['2019-20', '2018-19', '2017-18', '2016-17', '2015-16', '2014-15', '2013-14']
        self.compSchools = pd.read_csv(os.path.join(projectWD, 'Resources', 'CompSchoolAltSchoolID.txt'), sep='\t')
        self.dataTypeOptions = ['ethnicity', 'programSubgroup', 'academicYear']
        self.districts = ['Los Angeles Unified', 'Los Angeles', 'Statewide', 'Los Angeles County Office of Education',
                          'Inglewood Unified', 'Lennox', 'Compton Unified']
        self.reportFilterOpt = {"All Students": ["ContentPlaceHolder1_rdoListGender_0", "ContentPlaceHolder1_rdoEL_0",
                                                 "ContentPlaceHolder1_rdoSpecEd_0"],
                                "Male": ["ContentPlaceHolder1_rdoListGender_1", "ContentPlaceHolder1_rdoEL_0",
                                         "ContentPlaceHolder1_rdoSpecEd_0"],
                                "Female": ["ContentPlaceHolder1_rdoListGender_2", "ContentPlaceHolder1_rdoEL_0",
                                           "ContentPlaceHolder1_rdoSpecEd_0"],
                                "EL": ["ContentPlaceHolder1_rdoListGender_0", "ContentPlaceHolder1_rdoEL_1",
                                       "ContentPlaceHolder1_rdoSpecEd_0"],
                                "Non-EL": ["ContentPlaceHolder1_rdoListGender_0", "ContentPlaceHolder1_rdoEL_2",
                                           "ContentPlaceHolder1_rdoSpecEd_0"],
                                "SWD": ["ContentPlaceHolder1_rdoListGender_0", "ContentPlaceHolder1_rdoEL_0",
                                        "ContentPlaceHolder1_rdoSpecEd_1"],
                                "Non-SWD": ["ContentPlaceHolder1_rdoListGender_0", "ContentPlaceHolder1_rdoEL_0",
                                            "ContentPlaceHolder1_rdoSpecEd_2"]}

class CDE_WebScrapeStatic():
    def __init__(self):
        # self.schoolListTest_class=schoolListTest_class
        self.link_suspension = 'https://data1.cde.ca.gov/dataquest/dqCensus/DisSuspRate.aspx?year={SchoolYear_CDE}&agglevel=School&cds={SchoolCDS}'
        self.link_chronAbs = 'https://data1.cde.ca.gov/dataquest/DQCensus/AttChrAbsRate.aspx?agglevel=School&cds={SchoolCDS}&year={SchoolYear_CDE}'
        self.link_reclassRate = 'https://data1.cde.ca.gov/dataquest/Cbeds4.asp?Enroll=on&PctEL=on&PctFEP=on&PctRe=on&cSelect={SchoolYear_CDE}&cChoice=SchProf1&cYear={SchoolCDS}'
        self.link_EthnicitybyGrade = 'https://data1.cde.ca.gov/dataquest/dqcensus/EnrEthGrd.aspx?cds={SchoolCDS}&agglevel=school&year={SchoolYear_CDE}'
        self.link_EthnicitybyGradePercent = 'https://dq.cde.ca.gov/dataquest/dqcensus/EnrEthLevels.aspx?cds={SchoolCDS}&agglevel=school&year={SchoolYear_CDE}'

    def staticScrapeReclass(self, SchoolCDS, SchoolYear_CDE):
        htmlLink = self.link_reclassRate.format(SchoolCDS=SchoolCDS, SchoolYear_CDE=SchoolYear_CDE)
        htmlTable = pd.read_html(htmlLink)
        for tableIndex in range(0, len(htmlTable)):
            htmlTable[tableIndex]['HTML_Link'] = htmlLink
        return htmlTable

    def staticScrapeEth(self, SchoolCDS, SchoolYear_CDE, SchoolName):
        DataID = f'Eth_{SchoolCDS}_{SchoolYear_CDE}'
        htmlLink = self.link_EthnicitybyGrade.format(SchoolCDS=SchoolCDS, SchoolYear_CDE=SchoolYear_CDE)
        print(f'Running report for: {htmlLink}')
        htmlTable = pd.read_html(htmlLink)
        for tableIndex in range(0, len(htmlTable)):
            htmlTable[tableIndex]['HTML_Link'] = htmlLink
            htmlTable[tableIndex]['DataID'] = DataID
            htmlTable[tableIndex]['CDS_Code'] = SchoolCDS
            htmlTable[tableIndex]['SchoolYear'] = SchoolYear_CDE
            htmlTable[tableIndex]['SchoolName'] = SchoolName
        return htmlTable, DataID

    def staticScrapeEthPercent(self, SchoolCDS, SchoolYear_CDE, SchoolName):
        DataID = f'Eth_{SchoolCDS}_{SchoolYear_CDE}'
        htmlLink = self.link_EthnicitybyGradePercent.format(SchoolCDS=SchoolCDS, SchoolYear_CDE=SchoolYear_CDE)
        print(f'Running report for: {htmlLink}')
        htmlTable = pd.read_html(htmlLink)
        for tableIndex in range(0, len(htmlTable)):
            htmlTable[tableIndex]['HTML_Link'] = htmlLink
            htmlTable[tableIndex]['DataID'] = DataID
            htmlTable[tableIndex]['CDS_Code'] = SchoolCDS
            htmlTable[tableIndex]['SchoolYear'] = SchoolYear_CDE
            htmlTable[tableIndex]['SchoolName'] = SchoolName
        return htmlTable, DataID

    def StackTables(self, DataDictionary):
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


class CDE_WebScrapeSelenium():
    '''
    this is the main class that will be called in the main.py script.
    each method in this class
    
    '''
    def __init__(self):
        self.link_suspension = 'https://data1.cde.ca.gov/dataquest/dqCensus/DisSuspRate.aspx?year={SchoolYear_CDE}&agglevel=School&cds={SchoolCDS}'
        self.link_chronAbs = 'https://data1.cde.ca.gov/dataquest/DQCensus/AttChrAbsRate.aspx?agglevel=School&cds={SchoolCDS}&year={SchoolYear_CDE}'
        self.link_gradRate = 'https://data1.cde.ca.gov/dataquest/dqcensus/CohRate.aspx?agglevel=school&year={SchoolYear_CDE}&cds={SchoolCDS}'
        self.link_AGGradePercentPreview = 'https://preview.cde.ca.gov/DataQuest/DQCensus/CohRate.aspx?year={SchoolYear_CDE}&agglevel=school&cds={SchoolCDS}'
        self.link_AGGradePercent = 'https://data1.cde.ca.gov/dataquest/dqcensus/CohRate.aspx?year={SchoolYear_CDE}&agglevel=school&cds={SchoolCDS}'
        self.link_AdjCohortOutcome ='https://dq.cde.ca.gov/dataquest/dqcensus/CohOutcome.aspx?agglevel=school&year={SchoolYear_CDE}&cds={SchoolCDS}'
        self.link_enrollSubgroup='https://data1.cde.ca.gov/dataquest/dqcensus/EnrCharterSub.aspx?cds={SchoolCDS}&agglevel=school&year={SchoolYear_CDE}'
        self.link_enrollEth='https://data1.cde.ca.gov/dataquest/dqcensus/EnrEthGrd.aspx?cds={SchoolCDS}&agglevel=school&year={SchoolYear_CDE}'
        self.reportFilterOpt = {"All Students": ["ContentPlaceHolder1_rdoListGender_0", "ContentPlaceHolder1_rdoEL_0",
                                                 "ContentPlaceHolder1_rdoSpecEd_0"],
                                "Male": ["ContentPlaceHolder1_rdoListGender_1", "ContentPlaceHolder1_rdoEL_0",
                                         "ContentPlaceHolder1_rdoSpecEd_0"],
                                "Female": ["ContentPlaceHolder1_rdoListGender_2", "ContentPlaceHolder1_rdoEL_0",
                                           "ContentPlaceHolder1_rdoSpecEd_0"],
                                "EL": ["ContentPlaceHolder1_rdoListGender_0", "ContentPlaceHolder1_rdoEL_1",
                                       "ContentPlaceHolder1_rdoSpecEd_0"],
                                "Non-EL": ["ContentPlaceHolder1_rdoListGender_0", "ContentPlaceHolder1_rdoEL_2",
                                           "ContentPlaceHolder1_rdoSpecEd_0"],
                                "SWD": ["ContentPlaceHolder1_rdoListGender_0", "ContentPlaceHolder1_rdoEL_0",
                                        "ContentPlaceHolder1_rdoSpecEd_1"],
                                "Non-SWD": ["ContentPlaceHolder1_rdoListGender_0", "ContentPlaceHolder1_rdoEL_0",
                                            "ContentPlaceHolder1_rdoSpecEd_2"]}
        self.messagepresent = {"All Students": "All Students",
                               "Male": 'GenderMale',
                               "Female": 'GenderFemale',
                               "EL": 'EnglishLearnersYes',
                               "Non-EL": 'EnglishLearnersNo',
                               "SWD": 'StudentsWithDisabilitiesYes',
                               "Non-SWD": 'StudentsWithDisabilitiesNo'}
        self.susErrorlog = []
        self.chronAbsErrorlog = []

    def getFailList(self, failLogname='Fail_log.txt'):
        if os.path.isfile(failLogname):
            faillist = []
            with open(failLogname, 'r') as fl:
                tempfail = fl.read().splitlines()
            for i in tempfail:
                faillist.append(i.strip(" "))
            return faillist
        else:
            return [None]
    def setup_method(self, dockerIP='localhost:4444'):
        if sys.platform == 'linux':
            dockerIP = 'CDEwebscrape:4444'
            capabilities = DesiredCapabilities.CHROME.copy()
            selenium_grid_url = f"http://{dockerIP}/wd/hub"
            print(f'using selenium grid: {selenium_grid_url}')
            self.driver = webdriver.Remote(desired_capabilities=capabilities, command_executor=selenium_grid_url)
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(30)
            self.vars = {}
            return self.driver
        else:
            options_dic = {
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True}
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_experimental_option("prefs", options_dic)
            self.driver = webdriver.Chrome(str(pathToDriver), options=chromeOptions)
            self.driver.set_page_load_timeout(60)
            self.driver.implicitly_wait(60)
            self.vars = {}
            return self.driver

    def teardown_method(self):
        print('Now Closing Window in 15 seconds')
        time.sleep(5)
        print('Closing Window in 10 seconds')
        time.sleep(5)
        print('Closing Window in 5 seconds')
        time.sleep(5)
        print('Window Closed')
        self.driver.quit()

    # This method is meant to take the htmlSource and return a list of tables.
    def tablesHTML(self, cdeReport, dataID, htmlSource, htmlLink, SchoolYear_CDE, SchoolCDS, dataTypeOptions,
                   reportFilter, enabledFilter=None, susRep=None):
        try:
            htmlTable = pd.read_html(htmlSource)
            print(f'length of htmlTable is {len(htmlTable)}')
            # in the for loop it cycles through all the tables in the list and adds a column to help identify later on what table it is.
            for tableIndex in range(0, len(htmlTable)):
                htmlTable[tableIndex]['HTML_Link'] = htmlLink
                htmlTable[tableIndex]['SchoolCDS'] = SchoolCDS
                htmlTable[tableIndex]['SchoolYear_CDE'] = SchoolYear_CDE
                htmlTable[tableIndex]['dataTypeOptions'] = dataTypeOptions
                htmlTable[tableIndex]['reportFilter'] = reportFilter
                htmlTable[tableIndex]['dataID'] = dataID
                htmlTable[tableIndex]['enabledFilter'] = enabledFilter
                if susRep is not None:
                    htmlTable[tableIndex]['susRep'] = susRep
                fileDir = os.path.join(projectWD, 'ReportOutput')
                reportFolder = os.path.join(projectWD, 'ReportOutput',
                                            f'CDE_{cdeReport}_{dataTypeOptions}_Table{tableIndex + 1}')
                if not os.path.exists(fileDir):
                    os.makedirs(fileDir)
                if not os.path.exists(reportFolder):
                    os.makedirs(reportFolder)
                DropFile = os.path.join(reportFolder, f'{dataID}.csv')
                htmlTable[tableIndex].to_csv(DropFile, index=False)
            return htmlTable, dataID
        except Exception as ex:
            cowsay.cow('Error!!!')
            print(f'***GOT THE FOLLOWING ERROR in tablesHTML: {ex}***')
            return None

    def getDisaggregated(self):
        try:
            temp = self.driver.find_element(By.ID, 'ContentPlaceHolder1_pnlReport').text
            filtermsg = temp.replace('\n', '').replace(' ', '').replace(':', '')
            # print(f'Received following For Subgroup: {filtermsg}')
            # print(f'the data type of this string is: {type(filtermsg)}')
            return filtermsg
        except Exception as ex:
            cowsay.cow(f'in getEnabledFilters Function, the Message was not available. ')
            print(f'***GOT THE FOLLOWING ERROR: {ex}***')
            return ""

    def getEnabledFilters(self):
        try:
            temp = self.driver.find_element(By.ID, "filter-msg").text
            filtermsg = temp.replace('\n', '_').replace(' ', '').replace(':', '')
            filtermsgList = temp.replace(' ', '').replace('\n', ' ').replace(':', '')
            filtermsgList = filtermsgList.split()
            cowsay.tux(f'Received following filtermsg: {filtermsg}')
            cowsay.cheese(f'Received following filtermsg: {filtermsgList}')
            # print(f'the data type of this string is: {type(filtermsg)}')
            return filtermsg, filtermsgList
        except Exception as ex:
            cowsay.cow(f'in getEnabledFilters Function, the Message was not available. ')
            print(f'***GOT THE FOLLOWING ERROR: {ex}***')
            return ['NoFilter', 'NoFilter']

    def dataTypeOptions(self, reportInput):
        counter = 0
        if reportInput == 'ethnicity':
            while True:
                if counter < 20:
                    self.driver.find_element(By.ID, "ContentPlaceHolder1_rdoListReportRows_0").click()
                    temp = self.getDisaggregated()
                    if "DisaggregatedbyEthnicity" in temp:
                        print('Selected Ethnicity Report')
                        break
                    else:
                        counter += 1
                        time.sleep(1)
                else:
                    break
        if reportInput == 'programSubgroup':
            while True:
                if counter < 20:
                    self.driver.find_element(By.ID, "ContentPlaceHolder1_rdoListReportRows_1").click()
                    temp = self.getDisaggregated()
                    if "DisaggregatedbyProgramSubgroup" in temp:
                        print('Selected Subgroup Report')
                        break
                    else:
                        counter += 1
                        time.sleep(1)
                else:
                    break
        if reportInput == 'academicYear':
            while True:
                if counter < 20:
                    self.driver.find_element(By.ID, "ContentPlaceHolder1_rdoListReportRows_2").click()
                    temp = self.getDisaggregated()
                    if "DisaggregatedbyAcademicYear" in temp:
                        print('Selected Academic Year Report')
                        break
                    else:
                        counter += 1
                        time.sleep(1)
                else:
                    break

    def agGradRates(self, SchoolYear_CDE, SchoolCDS, dataTypeOptions='ethnicity',
                    reportFilter='All Students', reRunScrape: bool = False):
        """
        This will scrape the AG Graduation Rates.
        Since this method creates a CSV file to create a resilient application, the return values will be None for
        success, and dataID  to create a log of failed scrapes and skip later.

        """
        if dataTypeOptions != 'ethnicity':
            reportFilter = 'All Students'
        dataID = f'GradRate_{SchoolYear_CDE}_{SchoolCDS}_{dataTypeOptions}_Subgroup{reportFilter}'
        reportList = self.reportList()
        failList = self.getFailList()

        # This will skip anything that has failed in the past, or that we already have on record.
        if not reRunScrape:
            if dataID in failList:
                cowsay.beavis(f'Record in Fail_log.txt, so skipping for now')
                return None
            elif dataID in reportList:
                cowsay.beavis('Report already avaiable no need to scrape')
                return None
        else:
            print(f'Starting Scrape for: {dataID}')
        enabledFilter = None
        htmlLink = self.link_AGGradePercent.format(SchoolCDS=SchoolCDS, SchoolYear_CDE=SchoolYear_CDE)
        print(
            f'Running scrapeSuspension Function for link:{htmlLink}\nreportFilter:{reportFilter}\ndataTypeOptions:{dataTypeOptions}')
        # CurrentUrl=self.driver.getCurrentUrl()
        print(f'CurrentUrl is: {htmlLink}')
        try:
            self.driver.get(htmlLink)
            self.driver.find_element(By.LINK_TEXT, "Report Options and Filters").click()
            self.dataTypeOptions(dataTypeOptions)
            if dataTypeOptions == 'ethnicity':
                # This selects the subgroups
                filetersuccess = self.selectReportFilter(self.reportFilterOpt[reportFilter])
                if filetersuccess == 0:
                    cowsay.daemon(f'Failed to select Subgroups for {dataID}')
                    return dataID
            else:
                pass
            enabledFilterlist = self.getEnabledFilters()
            enabledFilter = enabledFilterlist[0]
            # This only needs to run if the report is not Ethnicity to Select Subgroups
            # this ensures that the options were selected by running a loop until it is satisfied
            if dataTypeOptions == 'ethnicity':
                self.selectReportFilter(self.reportFilterOpt[reportFilter])
            htmlSource = self.driver.page_source
            dataOutput = self.tablesHTML(cdeReport='AgGradRates', dataID=dataID, htmlSource=htmlSource,
                                         htmlLink=htmlLink, SchoolYear_CDE=SchoolYear_CDE, SchoolCDS=SchoolCDS,
                                         dataTypeOptions=dataTypeOptions, reportFilter=reportFilter,
                                         enabledFilter=enabledFilter)
            print(
                f'Ran Suspension report for {SchoolCDS} for School Year: {SchoolYear_CDE}, for the following breakdown: {dataTypeOptions}, subgroup: {reportFilter} enabledFilter: {enabledFilter}')
            return None
        except Exception as ex:
            cowsay.cow('Error!!!')
            print(f'***GOT THE FOLLOWING ERROR in scrapeSuspension: {ex}***')
            print(f'Skipping {SchoolCDS} for school year {SchoolYear_CDE}')
            return dataID

    def adjCohortOutcomes(self, SchoolYear_CDE, SchoolCDS, dataTypeOptions='ethnicity',
                    reportFilter='All Students', reRunScrape: bool = False):
        """
        Since this method creates a CSV file to create a resilient application, the return values will be None for
        success, and dataID  to create a log of failed scrapes and skip later.

        """
        if dataTypeOptions != 'ethnicity':
            reportFilter = 'All Students'
        dataID = f'adjCohort_{SchoolYear_CDE}_{SchoolCDS}_{dataTypeOptions}_Subgroup{reportFilter}'
        reportList = self.reportList()
        failList = self.getFailList()
        # This will skip anything that has failed in the past, or that we already have on record.
        if not reRunScrape:
            if dataID in failList:
                cowsay.beavis(f'Record in Fail_log.txt, so skipping for now')
                return None
            elif dataID in reportList:
                cowsay.beavis('Report already avaiable no need to scrape')
                return None
        else:
            print(f'Starting Scrape for: {dataID}')
        enabledFilter = None
        htmlLink = self.link_AdjCohortOutcome.format(SchoolCDS=SchoolCDS, SchoolYear_CDE=SchoolYear_CDE)
        print(
            f'Running scrapeSuspension Function for link:{htmlLink}\nreportFilter:{reportFilter}\ndataTypeOptions:{dataTypeOptions}')
        print(f'CurrentUrl is: {htmlLink}')
        try:
            self.driver.get(htmlLink)
            self.driver.find_element(By.LINK_TEXT, "Report Options and Filters").click()
            self.dataTypeOptions(dataTypeOptions)
            if dataTypeOptions == 'ethnicity':
                # This selects the subgroups
                filetersuccess = self.selectReportFilter(self.reportFilterOpt[reportFilter])
                if filetersuccess == 0:
                    cowsay.daemon(f'Failed to select Subgroups for {dataID}')
                    return dataID
            else:
                pass
            enabledFilterlist = self.getEnabledFilters()
            enabledFilter = enabledFilterlist[0]

            # This only needs to run if the report is not Ethnicity to Select Subgroups
            # this ensures that the options were selected by running a loop until it is satisfied

            if dataTypeOptions == 'ethnicity':
                self.selectReportFilter(self.reportFilterOpt[reportFilter])
            htmlSource = self.driver.page_source
            dataOutput = self.tablesHTML(cdeReport='adjCohort', dataID=dataID, htmlSource=htmlSource,
                                         htmlLink=htmlLink, SchoolYear_CDE=SchoolYear_CDE, SchoolCDS=SchoolCDS,
                                         dataTypeOptions=dataTypeOptions, reportFilter=reportFilter,
                                         enabledFilter=enabledFilter)
            print(
                f'Ran Suspension report for {SchoolCDS} for School Year: {SchoolYear_CDE}, for the following breakdown: {dataTypeOptions}, subgroup: {reportFilter} enabledFilter: {enabledFilter}')
            return None
        except Exception as ex:
            cowsay.cow('Error!!!')
            print(f'***GOT THE FOLLOWING ERROR in scrapeSuspension: {ex}***')
            print(f'Skipping {SchoolCDS} for school year {SchoolYear_CDE}')
            return dataID

    def selectReportFilter(self, urlid):
        '''Returns 0 if there was an error or returns 1 if it was a success'''
        for i in urlid:
            # time.sleep(10)
            print('Running: selectReportFilter')
            print(f'Option: {i}')
            count = 0
            while self.driver.find_element(By.ID, i).is_selected() == False:
                try:
                    print(f'Run count: {count + 1}')
                    count += 1
                    self.driver.find_element(By.ID, i).click()
                    time.sleep(10)
                    if count > 3:
                        return 0
                except:
                    if count > 3:
                        return 0
        return 1
    def reportGenderSelect(self, reportInput):
        if reportInput == 'Male':
            self.driver.find_element(By.ID, "ContentPlaceHolder1_rdoListGender_1").click()
        if reportInput == 'Female':
            self.driver.find_element(By.ID, "ContentPlaceHolder1_rdoListGender_2").click()
        else:
            self.driver.find_element(By.ID, "ContentPlaceHolder1_rdoListGender_0").click()

    def reportELSelect(self, reportInput):
        if reportInput == 'EL':
            self.driver.find_element(By.ID, "ContentPlaceHolder1_rdoEL_1").click()
        if reportInput == 'Non-EL':
            self.driver.find_element(By.ID, "ContentPlaceHolder1_rdoEL_2").click()
        else:
            self.driver.find_element(By.ID, "ContentPlaceHolder1_rdoEL_0").click()

    def reportSWDSelect(self, reportInput):
        if reportInput == 'SWD':
            self.driver.find_element(By.ID, "ContentPlaceHolder1_rdoSpecEd_1").click()
        if reportInput == 'Non-SWD':
            self.driver.find_element(By.ID, "ContentPlaceHolder1_rdoSpecEd_2").click()
        else:
            self.driver.find_element(By.ID, "ContentPlaceHolder1_rdoSpecEd_0").click()

    # this is specific to suspension
    def susReportselect(self, reportInput):
        counter = 0
        if reportInput == 'ISS':
            while True:
                self.driver.find_element(By.ID, "ContentPlaceHolder1_rdoListSuspType_1").click()
                time.sleep(10)
                _ = self.getEnabledFilters()
                if "Out-of-School" in _[0]:
                    print('Selected ISS')
                    break
                else:
                    counter += 1
                if counter >= 4:
                    break
                else:
                    pass
        elif reportInput == 'OSS':
            while True:
                self.driver.find_element(By.ID, "ContentPlaceHolder1_rdoListSuspType_2").click()
                time.sleep(10)
                _ = self.getEnabledFilters()
                if "Out-of-School" in _[0]:
                    print('Selected OSS')
                    break
                else:
                    counter += 1
                if counter >= 4:
                    break
                else:
                    pass

        elif reportInput == 'ALL':
            self.driver.find_element(By.ID, "ContentPlaceHolder1_rdoListSuspType_0").click()
            print('Selected All Suspensions')
        else:
            print('No SuspensionReport Selected')

    def reportList(self):
        try:
            ReportDir = os.path.join(projectWD, 'ReportOutput')
            ReportList = os.listdir(ReportDir)
            temp = []
            for i in ReportList:
                j = os.path.join(ReportDir, i)
                if os.path.isdir(j):
                    CDE_SuspensionReports = os.listdir(j)
                    for k in CDE_SuspensionReports:
                        k = str(k)
                        temp.append(k.replace('.csv', ''))
            temp = list(dict.fromkeys(temp))
            return temp
        except:
            return [None]

    def scrapeSuspension(self, SchoolYear_CDE, SchoolCDS, susRep, dataTypeOptions='ethnicity',
                         reportFilter='All Students', reRunScrape: bool = False):
        """
        Since this method creates a CSV file to create a resilient application, the return values will be None for
        success, and dataID  to create a log of failed scrapes and skip later.

        """
        if dataTypeOptions != 'ethnicity':
            reportFilter = 'All Students'
        dataID = f'Suspension_{SchoolYear_CDE}_{SchoolCDS}_{susRep}_{dataTypeOptions}_Subgroup{reportFilter}'
        reportList = self.reportList()
        failList = self.getFailList()
        # This will skip anything that has failed in the past, or that we already have on record.
        if not reRunScrape:
            if dataID in failList:
                cowsay.beavis(f'Record in Fail_log.txt, so skipping for now')
                return None
            elif dataID in reportList:
                cowsay.beavis('Report already avaiable no need to scrape')
                return None
        else:
            print(f'Starting Scrape for: {dataID}')
        enabledFilter = None
        htmlLink = self.link_suspension.format(SchoolCDS=SchoolCDS, SchoolYear_CDE=SchoolYear_CDE)
        print(
            f'Running scrapeSuspension Function for link:{htmlLink}\nsusRep:{susRep}\nreportFilter:{reportFilter}\ndataTypeOptions:{dataTypeOptions}')
        # CurrentUrl=self.driver.getCurrentUrl()
        print(f'CurrentUrl is: {htmlLink}')
        try:
            self.driver.get(htmlLink)
            self.driver.find_element(By.LINK_TEXT, "Report Options and Filters").click()
            # This selects Eth, or Program Subgroup
            self.dataTypeOptions(dataTypeOptions)
            ##This selects OSS ISS ALL suspenision types
            self.susReportselect(susRep)
            # self.dataTypeOptions(dataTypeOptions)
            if dataTypeOptions == 'ethnicity':
                # This selects the subgroups
                filetersuccess = self.selectReportFilter(self.reportFilterOpt[reportFilter])
                if filetersuccess == 0:
                    cowsay.daemon(f'Failed to select Subgroups for {dataID}')
                    return dataID
                # see if I can create a way to loop to see if the message is present before committing to extract data.
            else:
                pass
            enabledFilterlist = self.getEnabledFilters()
            enabledFilter = enabledFilterlist[0]

            # This only needs to run if the report is not Ethnicity to Select Subgroups
            # this ensures that the options were selected by running a loop until it is satisfied

            if dataTypeOptions == 'ethnicity':
                self.selectReportFilter(self.reportFilterOpt[reportFilter])
            htmlSource = self.driver.page_source
            dataOutput = self.tablesHTML(cdeReport='Suspension', dataID=dataID, htmlSource=htmlSource,
                                         htmlLink=htmlLink, SchoolYear_CDE=SchoolYear_CDE, SchoolCDS=SchoolCDS,
                                         dataTypeOptions=dataTypeOptions, reportFilter=reportFilter,
                                         enabledFilter=enabledFilter, susRep=susRep)
            print(
                f'Ran Suspension report for {SchoolCDS} for School Year: {SchoolYear_CDE}, for the following breakdown: {dataTypeOptions}, subgroup: {reportFilter} enabledFilter: {enabledFilter}')
            return None
        except Exception as ex:
            cowsay.cow('Error!!!')
            print(f'***GOT THE FOLLOWING ERROR in scrapeSuspension: {ex}***')
            print(f'Skipping {SchoolCDS} for school year {SchoolYear_CDE}')
            # add to class log to review Later.
            return dataID

    # this is specific to Chronically Absent
    def scrapeChronAbs(self, SchoolYear_CDE, SchoolCDS, dataTypeOptions='ethnicity', reportFilter='All Students'):
        # Catch an error when it wants to
        if dataTypeOptions != 'ethnicity':
            reportFilter = 'All Students'
        dataID = f'Absenteeism_{SchoolYear_CDE}_{SchoolCDS}_{dataTypeOptions}_Subgroup{reportFilter}'
        reportList = self.reportList()
        failList = self.getFailList()
        if dataID in failList:
            cowsay.beavis(f'Record in Fail_log.txt, so skipping for now')
            return None
        if dataID in reportList:
            cowsay.beavis('Report already avaiable no need to scrape')
            return None
        else:
            enabledFilter = None
            htmlLink = self.link_chronAbs.format(SchoolCDS=SchoolCDS, SchoolYear_CDE=SchoolYear_CDE)
            print(
                f'Running scrapeSuspension Funtion for link:{htmlLink} \n reportFilter:{reportFilter}\n dataTypeOptions:{dataTypeOptions}')
            print(f'CurrentUrl is: {htmlLink}')
            try:
                self.driver.get(htmlLink)
                self.driver.find_element(By.LINK_TEXT, "Report Options and Filters").click()
                if dataTypeOptions == 'ethnicity':
                    self.selectReportFilter(self.reportFilterOpt[reportFilter])
                else:
                    self.dataTypeOptions(dataTypeOptions)
                enabledFilterlist = self.getEnabledFilters()
                enabledFilter = enabledFilterlist[0]
                #
                if dataTypeOptions == 'ethnicity':
                    filetersuccess = self.selectReportFilter(self.reportFilterOpt[reportFilter])
                    if filetersuccess == 0:
                        cowsay.daemon(f'Failed to select Subgroups for {dataID}')
                        return dataID
                else:
                    cowsay.stegosaurus('3')
                    self.dataTypeOptions(dataTypeOptions)
                enabledFilterlist = self.getEnabledFilters()
                enabledFilter = enabledFilterlist[0]
                if dataTypeOptions == 'ethnicity':
                    cowsay.stegosaurus('4')
                    self.selectReportFilter(self.reportFilterOpt[reportFilter])
                cowsay.stegosaurus('5')
                htmlSource = self.driver.page_source
                dataOutput = self.tablesHTML(cdeReport='Absenteeism', dataID=dataID, htmlSource=htmlSource,
                                             htmlLink=htmlLink, SchoolYear_CDE=SchoolYear_CDE, SchoolCDS=SchoolCDS,
                                             dataTypeOptions=dataTypeOptions, reportFilter=reportFilter,
                                             enabledFilter=enabledFilter, susRep=None)
                print(
                    f'Ran Suspension report for {SchoolCDS} for School Year: {SchoolYear_CDE}, for the following breakdown: {dataTypeOptions}, subgroup: {reportFilter} enabledFilter: {enabledFilter}')
                return None
            except Exception as ex:
                cowsay.cow('Error!!!')
                print(f'***GOT THE FOLLOWING ERROR in scrapeSuspension: {ex}***')
                print(f'Skipping {SchoolCDS} for school year {SchoolYear_CDE}')
                return dataID
                htmlSource = self.driver.page_source
                dataOutput = self.tablesHTML(cdeReport='Absenteeism', dataID=dataID, htmlSource=htmlSource,
                                             htmlLink=htmlLink, SchoolYear_CDE=SchoolYear_CDE, SchoolCDS=SchoolCDS,
                                             dataTypeOptions=dataTypeOptions, reportFilter=reportFilter,
                                             enabledFilter=enabledFilter, susRep=susRep)
                print(
                    f'Ran Suspension report for {SchoolCDS} for School Year: {SchoolYear_CDE}, for the following breakdown: {dataTypeOptions}, subgroup: {reportFilter} enabledFilter: {enabledFilter}')
                return None
            except Exception as ex:
                cowsay.cow('Error!!!')
                print(f'***GOT THE FOLLOWING ERROR in scrapeSuspension: {ex}***')
                print(f'Skipping {SchoolCDS} for school year {SchoolYear_CDE}')
                # add to class log to review Later.
                return dataID

    def scrapeGradRates(self, SchoolYear_CDE, SchoolCDS, dataTypeOptions='ethnicity', reportFilter='All Students'):
        # Catch an error when it wants to
        if dataTypeOptions != 'ethnicity':
            reportFilter = 'All Students'
        dataID = f'GradRate_{SchoolYear_CDE}_{SchoolCDS}_{dataTypeOptions}_Subgroup{reportFilter}'
        reportList = self.reportList()
        failList = self.getFailList()
        if dataID in failList:
            cowsay.beavis(f'Record in Fail_log.txt, so skipping for now')
            return None
        elif dataID in reportList:
            cowsay.beavis('Report already avaiable no need to scrape')
            return None
        else:
            enabledFilter = None
            htmlLink = self.link_gradRate.format(SchoolCDS=SchoolCDS, SchoolYear_CDE=SchoolYear_CDE)
            print(
                f'Running scrapeSuspension Funtion for link:{htmlLink} \n reportFilter:{reportFilter}\n dataTypeOptions:{dataTypeOptions}')
            print(f'CurrentUrl is: {htmlLink}')
            try:
                self.driver.get(htmlLink)
                self.driver.find_element(By.LINK_TEXT, "Report Options and Filters").click()
                if dataTypeOptions == 'ethnicity':
                    self.selectReportFilter(self.reportFilterOpt[reportFilter])
                else:
                    self.dataTypeOptions(dataTypeOptions)
                enabledFilterlist = self.getEnabledFilters()
                enabledFilter = enabledFilterlist[0]
                if dataTypeOptions == 'ethnicity':
                    filetersuccess = self.selectReportFilter(self.reportFilterOpt[reportFilter])
                    if filetersuccess == 0:
                        cowsay.daemon(f'Failed to select Subgroups for {dataID}')
                        return dataID
                else:
                    cowsay.stegosaurus('3')
                    self.dataTypeOptions(dataTypeOptions)
                enabledFilterlist = self.getEnabledFilters()
                enabledFilter = enabledFilterlist[0]
                if dataTypeOptions == 'ethnicity':
                    cowsay.stegosaurus('4')
                    self.selectReportFilter(self.reportFilterOpt[reportFilter])
                cowsay.stegosaurus('5')
                htmlSource = self.driver.page_source
                dataOutput = self.tablesHTML(cdeReport='GradRate', dataID=dataID, htmlSource=htmlSource,
                                             htmlLink=htmlLink, SchoolYear_CDE=SchoolYear_CDE, SchoolCDS=SchoolCDS,
                                             dataTypeOptions=dataTypeOptions, reportFilter=reportFilter,
                                             enabledFilter=enabledFilter, susRep=None)
                print(
                    f'Ran Suspension report for {SchoolCDS} for School Year: {SchoolYear_CDE}, for the following breakdown: {dataTypeOptions}, subgroup: {reportFilter} enabledFilter: {enabledFilter}')
                return None
            except Exception as ex:
                cowsay.cow('Error!!!')
                print(f'***GOT THE FOLLOWING ERROR in scrapeSuspension: {ex}***')
                print(f'Skipping {SchoolCDS} for school year {SchoolYear_CDE}')
                return dataID

                htmlSource = self.driver.page_source
                dataOutput = self.tablesHTML(cdeReport='Absenteeism', dataID=dataID, htmlSource=htmlSource,
                                             htmlLink=htmlLink, SchoolYear_CDE=SchoolYear_CDE, SchoolCDS=SchoolCDS,
                                             dataTypeOptions=dataTypeOptions, reportFilter=reportFilter,
                                             enabledFilter=enabledFilter, susRep=susRep)
                print(
                    f'Ran Suspension report for {SchoolCDS} for School Year: {SchoolYear_CDE}, for the following breakdown: {dataTypeOptions}, subgroup: {reportFilter} enabledFilter: {enabledFilter}')
                return None
            except Exception as ex:
                cowsay.cow('Error!!!')
                print(f'***GOT THE FOLLOWING ERROR in scrapeGradRates: {ex}***')
                print(f'Skipping {SchoolCDS} for school year {SchoolYear_CDE}')
                return dataID


    def scrapeEnroll(self, SchoolYear_CDE, SchoolCDS, dataTypeOptions='ethnicity', reportFilter='All Students'):
        if dataTypeOptions != 'ethnicity':
            reportFilter = 'All Students'
            scrapeLink = self.link_enrollSubgroup
        else:
            scrapeLink=self.link_enrollEth

        dataID = f'Enrollment_{SchoolYear_CDE}_{SchoolCDS}_{dataTypeOptions}_Subgroup{reportFilter}'
        reportList = self.reportList()
        failList = self.getFailList()
        if dataID in failList:
            cowsay.beavis(f'Record in Fail_log.txt, so skipping for now')
            return None
        elif dataID in reportList:
            cowsay.beavis('Report already avaiable no need to scrape')
            return None
        else:
            enabledFilter = None
            htmlLink = scrapeLink.format(SchoolCDS=SchoolCDS, SchoolYear_CDE=SchoolYear_CDE)
            print(
                f'Running scrapeSuspension Funtion for link:{htmlLink} \n reportFilter:{reportFilter}\n dataTypeOptions:{dataTypeOptions}')
            print(f'CurrentUrl is: {htmlLink}')
            try:
                self.driver.get(htmlLink)
                self.driver.find_element(By.LINK_TEXT, "Report Options and Filters").click()
                if dataTypeOptions == 'ethnicity':
                    self.selectReportFilter(self.reportFilterOpt[reportFilter])
                else:
                    self.dataTypeOptions(dataTypeOptions)
                enabledFilterlist = self.getEnabledFilters()
                enabledFilter = enabledFilterlist[0]
                #
                if dataTypeOptions == 'ethnicity':
                    filetersuccess = self.selectReportFilter(self.reportFilterOpt[reportFilter])
                    if filetersuccess == 0:
                        cowsay.daemon(f'Failed to select Subgroups for {dataID}')
                        return dataID
                else:
                    cowsay.stegosaurus('3')
                    self.dataTypeOptions(dataTypeOptions)
                enabledFilterlist = self.getEnabledFilters()
                enabledFilter = enabledFilterlist[0]
                if dataTypeOptions == 'ethnicity':
                    cowsay.stegosaurus('4')
                    self.selectReportFilter(self.reportFilterOpt[reportFilter])
                cowsay.stegosaurus('5')
                htmlSource = self.driver.page_source
                dataOutput = self.tablesHTML(cdeReport='Enroll', dataID=dataID, htmlSource=htmlSource,
                                             htmlLink=htmlLink, SchoolYear_CDE=SchoolYear_CDE, SchoolCDS=SchoolCDS,
                                             dataTypeOptions=dataTypeOptions, reportFilter=reportFilter,
                                             enabledFilter=enabledFilter, susRep=None)
                print(
                    f'Ran Suspension report for {SchoolCDS} for School Year: {SchoolYear_CDE}, for the following breakdown: {dataTypeOptions}, subgroup: {reportFilter} enabledFilter: {enabledFilter}')
                return None
            except Exception as ex:
                cowsay.cow('Error!!!')
                print(f'***GOT THE FOLLOWING ERROR in scrapeSuspension: {ex}***')
                print(f'Skipping {SchoolCDS} for school year {SchoolYear_CDE}')
                return dataID

                htmlSource = self.driver.page_source
                dataOutput = self.tablesHTML(cdeReport='Absenteeism', dataID=dataID, htmlSource=htmlSource,
                                             htmlLink=htmlLink, SchoolYear_CDE=SchoolYear_CDE, SchoolCDS=SchoolCDS,
                                             dataTypeOptions=dataTypeOptions, reportFilter=reportFilter,
                                             enabledFilter=enabledFilter, susRep=susRep)
                print(
                    f'Ran Suspension report for {SchoolCDS} for School Year: {SchoolYear_CDE}, for the following breakdown: {dataTypeOptions}, subgroup: {reportFilter} enabledFilter: {enabledFilter}')
                return None
            except Exception as ex:
                cowsay.cow('Error!!!')
                print(f'***GOT THE FOLLOWING ERROR in scrapeGradRates: {ex}***')
                print(f'Skipping {SchoolCDS} for school year {SchoolYear_CDE}')
                return dataID