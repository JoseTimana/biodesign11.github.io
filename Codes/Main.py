# i = 0
# j = 0
# start = time.time()
# a = time.time() - start
# print(a)
# while a < 1:
# 	i = i+1
# 	a = time.time() - start
# 	time.sleep(0.0002)
# 	# #Wait 1/360 s
# 	# while j < 340:
# 	# 	j = j+1
# 	# 	print(j)
# 	# j=0
# print(time.time()-start)
# print(i) #Number of samples

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

import Storing
import Pan_Tompkings_algorithm

import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Permissions to modify and access google drive
SCOPES = ['https://www.googleapis.com/auth/drive']
# Define an object with the class "googledriveapi" to define drive_service
GoogledriveAPI = Storing.googledriveapi(SCOPES)
# Give the permissions to the API
drive_service = build('drive', 'v3', credentials= GoogledriveAPI.getcredentials())

# Define patient
firstname = "Naomi"
lastname = "Guevara"
DNI = "72684012"
print("Patient:")
print("   Name: "+ lastname+" "+firstname)
print("   DNI: "+ DNI)

# Create patient´s folder to store data
print("-----------------------------------------------------------------------------------------------")
print("Creating patient's folder...\n")
print("Creating on Google drive...")
PatientDrive = Storing.googledriveapi.createFolder(lastname+"_"+firstname+"_"+DNI,drive_service)
print("Creating on the SD...")

PatientSDname, PatientSDpath = Storing.raspberrysd.createFolder(lastname+"_"+firstname+"_"+DNI)

# Create year's folder
currentYear = str(datetime.now().year)
Months = ["",'January','February','March','April','May','June','July','August','September','October','November','December']
Months[1]
# Create a folder to store all ECG data

AllECGname, AllECGpath = Storing.raspberrysd.createFolder("AllECG",PatientSDpath)

# Create Months' folder
print("-----------------------------------------------------------------------------------------------")
print("Creating patient's folder...\n")
print("Creating months' folder...\n")
print("Creating on Google drive...")
# A list to store Folder ID
DriveMonths = ["0","","","","","","","","","","","",""]
for i in range(1,13):
	DriveMonths[i] = Storing.googledriveapi.createFolder(currentYear+"_"+str(i)+"_"+ Months[i],drive_service,PatientDrive)
print("Creating on the SD...")
# A list to store Folder name and patH
SDMonth_name = ["0","","","","","","","","","","","",""]
SDMonth_path = ["0","","","","","","","","","","","",""]
for i in range(1,13):
	SDMonth_name[i],SDMonth_path[i] = Storing.raspberrysd.createFolder(currentYear+"_"+str(i)+"_"+ Months[i], PatientSDpath)

# Creating folder for the panic button and events of Ventricular Tachycardia in Google Drive and SD
print("-----------------------------------------------------------------------------------------------")
print("Creating patient's folder...\n")
print("Creating folder for the panic button and events of Ventricular Tachycardia")

DriveMonthPB = ["0","","","","","","","","","","","",""]
DriveMonthVT = ["0","","","","","","","","","","","",""]
for i in range(1,13):
	DriveMonthPB[i] = Storing.googledriveapi.createFolder("Panic button"+"_"+ Months[i],drive_service,DriveMonths[i])
	DriveMonthVT[i] = Storing.googledriveapi.createFolder("Ventricular Tachycardia"+"_"+ Months[i],drive_service,DriveMonths[i])

SDMonth_namePB = ["","","","","","","","","","","","",""]
SDMonth_pathPB = ["","","","","","","","","","","","",""]
SDMonth_nameVT = ["","","","","","","","","","","","",""]
SDMonth_pathVT = ["","","","","","","","","","","","",""]
for i in range(1,13):
	SDMonth_namePB[i],SDMonth_pathPB[i] = Storing.raspberrysd.createFolder("Panic button"+"_"+ Months[i],SDMonth_path[i])
	SDMonth_nameVT[i],SDMonth_pathVT[i] = Storing.raspberrysd.createFolder("Ventricular Tachycardia"+"_"+ Months[i],SDMonth_path[i])

#################################################################################################################################################
# As folders have already been created is time to start with daily monitoring
print("-----------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------")
print("As folders have already been created is time to start with daily monitoring")
# Get current day
currentday = currentday = str(datetime.now().year)+"-"+str(datetime.now().month)+"-"+str(datetime.now().day)
now = datetime.now()
# Run until year finishes
# year = datetime.now().year
for i in range(0,1): #Just to make some 
# while  year ~= "2020":
# 	year = datetime.now().year
	currentday = str(datetime.now().year)+"-"+str(datetime.now().month)+"-"+str(datetime.now().day)
	print(currentday)
	# Create a folder for this day
	print("Creating daily ECG folder the SD...")
	daySDname, daySDpath = Storing.raspberrysd.createFolder(currentday,AllECGpath)
	for i in range(0,5):
# 	while currentday == str(datetime.now().year)+"-"+str(datetime.now().month)+"-"+str(datetime.now().day)):
		# Simulating ADS1115
		print("Starting data sampling...")
		w = 0 # Number of samples
		Samples = []
		Measurements = []
		start = time.time()
		end = time.time() - start
		samptime = 10
		while end < samptime:
			dir(datetime)
			dir(np)
			dir(plt)
			dir(MediaFileUpload)
			dir(pd)
			dir(pickle)
			dir(datetime)
			dir(np)
			dir(plt)
			dir(MediaFileUpload)
			dir(pd)
			dir(pickle)

			print(str(int(float(end)*100/samptime))+"%") # To reduce the quantity of data
			Samples.append(w)
			Measurements.append(w**2)
			w = w+1
			end = time.time() - start
		print("100%")
		print("Data sampling completed")
		print(str(w)+ " samples colected")
		print("-----------------------------------------------------------------------------------------------")
		print("Storing samples in a csv file...")
		currenttime = str(datetime.now().hour)+"h-"+str(datetime.now().minute)+"m-"+str(datetime.now().second)+"s" #now.strftime("%Hh-%Mm-%Ss")
		CSVdayname, CSVdaypath = Storing.raspberrysd.createcsvFile(Samples,Measurements,"rawdata_"+currenttime,daySDpath)
		print("Successfully stored")
		print("-----------------------------------------------------------------------------------------------")
		print("Reading data sampled")
		csvecg = pd.read_csv(daySDpath + "/" + CSVdayname + ".csv", delimiter=',')
		#Convert to numpy array
		rawecg = csvecg.to_numpy()
		#Define axis for plotting
		sample = rawecg[:,0]
		xsample = np.divide(sample,w/samptime)
		LII = rawecg[:,1]
		zero = np.mean(LII) #Define zero voltage
		yLII = np.divide(np.subtract(LII,zero),204.8)
		print("Successfully readed")
		print("-----------------------------------------------------------------------------------------------")
		print("Starting QRS detection with Pan Tompkings algorithm")
		#qrs_detector = Pan_Tompkings_algorithm.Peakdetection(ecg_data_path="C:\Laptop\Biodesign\Database python\input\mitbih_database/100.csv")

		print("QRS complex and peaks Successfully detected")
		print("   Heartbeat: ")
		print("   Width QRS Complex: ")
		print("   RWPT Q-R: ")
		print("-----------------------------------------------------------------------------------------------")

		print("Diagnosing Ventricular Tachycardia...")
		print("   According to Fernando Pava's criteria:")
		print("   Diagnosis is positive when:")
		print("   Width QRS Complex is >= 120ms ")
		print("   R wave peak time(RWPT) is >= 50ms")
		print("-----------------------------------------------------------------------------------------------")
		print("Saving ECG plot including data, diagnosis and peaks on SD")

		print("Saving ECG plot including data, diagnosis and peaks on Google drive")
		print("-----------------------------------------------------------------------------------------------")
		print("Panic button pressed")

		print("Saving ECG plot including data, diagnosis and peaks on Google drive")
		print("----------------------------------------------------------------------------------------------")
# 	Update current day
# 		currentday = str(datetime.now().year)+"-"+str(datetime.now().month)+"-"+str(datetime.now().day)