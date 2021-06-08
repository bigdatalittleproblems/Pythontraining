import pandas as pd
# ALL files can be found here: https://www.cde.ca.gov/ds/ad/enrolldowndata.asp
enrollFiles = {
    "2020-2021":"https://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=2020-21&cCat=Enrollment&cPage=filesenr.asp",
    '2019-2020': 'http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=2019-20&cCat=Enrollment&cPage=filesenr.asp',
    "2018-2019": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=2018-19&cCat=Enrollment&cPage=filesenr.asp",
    "2017-2018": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=2017-18&cCat=Enrollment&cPage=filesenr.asp",
    "2016-2017": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=2016-17&cCat=Enrollment&cPage=filesenr.asp",
    "2015-2016": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=2015-16&cCat=Enrollment&cPage=filesenr.asp",
    "2014-2015": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=2014-15&cCat=Enrollment&cPage=filesenr.asp",
    "2013-2014": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=2013-14&cCat=Enrollment&cPage=filesenr.asp",
    "2012-2013": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=2012-13&cCat=Enrollment&cPage=filesenr.asp",
    "2011-2012": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=2011-12&cCat=Enrollment&cPage=filesenr.asp",
    "2010-2011": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=2010-11&cCat=Enrollment&cPage=filesenr.asp",
    "2009-2010": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=2009-10&cCat=Enrollment&cPage=filesenr.asp",
    "2008-2009": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=2008-09&cCat=Enrollment&cPage=filesenr.asp",
    "2007-2008": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=2007-08&cCat=Enrollment&cPage=filesenr.asp",
    "2006-2007": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=0607&cCat=Enrollment&cPage=filesenr.asp",
    "2005-2006": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=0506&cCat=Enrollment&cPage=filesenr.asp",
    "2004-2005": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=0405&cCat=Enrollment&cPage=filesenr.asp",
    "2003-2004": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=0304&cCat=Enrollment&cPage=filesenr.asp",
    "2002-2003": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=0203&cCat=Enrollment&cPage=filesenr.asp",
    "2001-2002": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=0102&cCat=Enrollment&cPage=filesenr.asp",
    "2000-2001": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=0001&cCat=Enrollment&cPage=filesenr.asp",
    "1999-2000": "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=9900&cCat=Enrollment&cPage=filesenr.asp"
    }
CDSConversion={19101990136119:'CHA',
               19646341996586:'ING',
               19647091996313:'LEA',
               19647330101675:'DLH',
               19647330102434:'SLA',
               19647330106831:'VEN',
               19647330106849:'BRW',
               19647330111575:'BUN',
               19647330111583:'ROB',
               19647330111617:'LCK',
               19647330111625:'WAT',
               19647330118570:'LCK',
               19647330118588:'LCK',
               19647330118596:'LCK',
               19647330119909:'LCK',
               19647330122481:'JMS',
               19647330122499:'WMS',
               19647330123992:'AEO',
               19647330124008:'JAM',
               19647330124016:'LGC',
               19647330124024:'LGC',
               19647330124883:'CPA',
               19647330129270:'MAE',
               19647330134023:'FLO',
               19647331935154:'LCK',
               19734370137984:'CMP',
               19756711996586:'ING'}
df_list=[]
for i in list(enrollFiles.keys())[0:4]:
    print(f"Pulling data for the {i} SY from: {enrollFiles[i]}")
    df_temp=pd.read_csv(enrollFiles[i],sep='\t')
    # df_temp=df_temp.loc[df_temp['CDS_CODE'].isin( list(CDSConversion.keys()))]
    df_temp['SchoolYear']=i
    df_list.append(df_temp)
df_stack=pd.concat(df_list)
df_stack.to_csv('enrolldatastack.csv',index=False)