# Project Setup Guide

## **Setting Up a New VM**
Follow these steps to configure your virtual machine, install necessary dependencies, and run your scripts!

### **Prerequisite: Manually Update Package Lists**
Before running any of the scripts, ensure package list is up-to-date by running...
```bash
sudo apt update
```

### **1. Install Chrome Headless Browser**
We require **Google Chrome Headless Browser** in order to web scrape. To install it, use this script in the repo...
```bash
./install_chrome.sh
```

### **2. Verify Chrome Headless Browser Installation**
After running the script, verify that Chrome was installed correctly by running...
```bash
google-chrome-stable --version
google-chrome-stable --headless --disable-gpu --dump-dom https://example.com/
```

### **3. Install Python Dependencies**
To ensure all necessary packages are installed, run the following command...
```bash
pip install -r requirements.txt
```
The script installs pandas and lxml.

### **4. Set Up Virtual Machine Using Makefile**
Use make for automation (rather than manually setting up the virtual environment) by running...
```bash
make update
```
This command will create a Python environment inside env/, install the dependencies in requirements.txt, and activate the environment.

### **5. Running a Job Using Makefile**
To check the project repo's structure, we'll use the command...
```bash
make ygainers.csv
```
This command starts a web scraping job, fetches data, and saves it to ygainers.csv

### **6. Project Directory Structure**
To see our repo's structure, we'll use the command...
```bash
tree SP25_DS5111_cbv6gd -I env
```
The output should look like this...
```
/home/ubuntu/SP25_DS5111_cbv6gd
├── README.md
├── data
├── init.sh
├── makefile
├── requirements.txt
└── scripts
    ├── global_creds.sh
    └── install_chrome_headless.sh
```
