# Phase 2 CDE Data Scrape #

This is the repository for the Phase2 project where it will pull data directly from CDE and place it in the following file```./ReportOutputFinal/FinalStaged.csv```
* This can be run on Windows and Linux, but it is optimized to run on a Linux Server using Docker.

## Linux Requirements ##
* Have Docker installed on linux machine, and have docker-compose enabled.
* From root of project, run  ```docker-compose up --exit-code-from pythonscript``` to run it completely in the background, or ```docker-compose up -d ``` to run it and see the log outputs to monitor progress.
  - either one will build the image and run the container in the background.
    
* to stop and terminate the containers, in the root of the project, use the command: ```docker-compose down```

### Windows Requirements ###

* Have Python (3.7 or higher), and Chrome WebDriver downloaded and in your Environement Variables.
* Here is the link to dowload [Chromium](https://chromedriver.chromium.org/downloads) that will work as the Chrome Driver. the ChromeDriver directory is where you should store the driver so the program can find it.

### Install Packages ###
* All Python Packages are found in the ```requirements.txt``` file at the root of this directory.
* to install, you can run ```pip install -r requirements.txt```


### Running an Update ###

* **Update School Years**
  - In ```main.py```, you will find the list variable ```SchoolYear_CDE``` on line 20. Here, you can add new schools years, or additional prior school years. Each list entry must be formatted like ```'2019-20'```
* **Update Schools to scrape** 
  - Schools to scrape are stored in this file: ```./Resources/CDE_SchoolScrapeList.txt```. You will need to add schools here to pull their information.  
  - _**note**, i decided to use the txt file vs a csv file because there are instances where the csv file will convert the SSID into scientific notation. By storing it as txt, it will not round these values._
  - To find CDE Codes of other schools, you can use this link to search CDE Codes:  [CDE School Directory](https://www.cde.ca.gov/schooldirectory/)
### Re-Running Reports ###
* To increase efficiency when re-running, the ```Fail_log.txt``` is a storing a list of reports that failed. Usually, reports fail because there is no data present for the specific report. By default, when re-running the script, it sees if a specific report is here and skips them if they are. 
  * if you want to re-run all the reports that failed, either because the data has been recently published, or you just want to make sure that all data was collected, then you can just delete the ```Fail_log.txt``` file. This will not affect anything, and it will just reproduced from scratch.  

### Install Docker on Linux Server ###
* For Linux, it is best to use a docker container to run the process since it will be predictable and reliable.
* Have Docker installed by running this command: ```curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh```
* Have docker-compose installed by running ```sudo apt install docker-compose -y```
* Once these two packages are installed, you can run the docker container automatically by entering the following command while in this working directory: "docker-compose up". 
* To run it as a daemon in the background, run ```docker-compose up -d```
once it is finished, the Selenium Container will still be running, so you can take it down with "docker-compose down"
### Who do I talk to? ###

* With errors regarding the Chrome Driver, Tarah knows how to troubleshoot many errors, or how to download the most recent Chrome Driver.
* Errors with the Chrome Driver usually look like this: ![Error_Example](Error_Example.png)
