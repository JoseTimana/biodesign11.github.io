from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
import send2trash
import numpy as np
import pandas as pd

# If modifying these scopes, delete the file token.pickle.
class googledriveapi:
	def __init__(self,SCOPES):
		self.SCOPES = SCOPES

	def getcredentials(self):
	    """Shows basic usage of the Drive v3 API."""
	    creds = None
	    # The file token.pickle stores the user's access and refresh tokens, and is
	    # created automatically when the authorization flow completes for the first
	    # time.
	    if os.path.exists('token.pickle'):
	        with open('token.pickle', 'rb') as token:
	            creds = pickle.load(token)
	    # If there are no (valid) credentials available, let the user log in.
	    if not creds or not creds.valid:
	        if creds and creds.expired and creds.refresh_token:
	            creds.refresh(Request())
	        else:
	            flow = InstalledAppFlow.from_client_secrets_file(
	                'credentials.json', self.SCOPES)
	            creds = flow.run_local_server(port=0)
	        # Save the credentials for the next run
	        with open('token.pickle', 'wb') as token:
	            pickle.dump(creds, token)
	    return creds

	#Drive v3 API
	def uploadFile(filename,drive_service,filepath,mimetype,folder_id = 'root'):
	    file_metadata = {'name': filename,'parents': [folder_id]}
	    media = MediaFileUpload(filepath, mimetype=mimetype)
	    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
	    #print('File ID: %s' % file.get('id'))
	    print( filename +" Successfully uploaded")
	    return file.get('id')

	def createFolder(name,drive_service,folder_id = 'root'):
	    file_metadata = {'name': name, 'mimeType': 'application/vnd.google-apps.folder','parents': [folder_id]}
	    file = drive_service.files().create(body=file_metadata, fields='id').execute()
	    #print ('Folder ID: %s' % file.get('id'))
	    print( name +" Successfully created")
	    return file.get('id')

	def downloadFile(file_id,drive_service,filepath):
	    request = drive_service.files().get_media(fileId=file_id)
	    fh = io.BytesIO()
	    downloader = MediaIoBaseDownload(fh, request)
	    done = False
	    while done is False:
	        status, done = downloader.next_chunk()
	        print("Download %d%%." % int(status.progress() * 100))
	    with io.open(filepath,'wb') as f:
	        fh.seek(0)
	        f.write(fh.read())
	    print("Successfully downloaded")

	def searchFile(size,drive_service,query):
	    results = drive_service.files().list( pageSize=size, fields="nextPageToken, files(id, name, kind, mimeType)", q=query).execute()
	    items = results.get('files', [])
	    if not items:
	        print('No files found.')
	    else:
	        print('Files:')
	        for item in items:
	            print('{0} ({1})'.format(item['name'], item['id']))


class raspberrysd:
	def __init__(self):
		pass

	def createFolder(name,folderpath = os.getcwd()):
		#define the name of the directory to be created
		path = folderpath + '/' + name
		try:
			os.mkdir(path)
		except OSError:
			print ("Creation of the directory %s failed" % path)
		else:
			print ( name + " Successfully created on %s " % path)
		return name, path

	def createcsvFile(samples,measurements,csvname,csvpath):
		pd.DataFrame({'Samples': samples,'Measurements': measurements}).to_csv(csvpath + '/' + csvname +'.csv',index = False)
		return csvname, csvpath

	def trashFile(filename):
		if os.path.exists(filename):
			send2trash.send2trash(filename)
			if os.path.exists(filename):
				print("Moved to trash failed")
			else:
				print("Successfully moved to trash")
		else:
			print("File doesn't exist")

if __name__ == "__main__":
	
	SCOPES = ['https://www.googleapis.com/auth/drive']
	GoogledriveAPI = googledriveapi(SCOPES)
	drive_service = build('drive', 'v3', credentials= GoogledriveAPI.getcredentials())

	# Create a folder and save Folder ID
	# Ventriculartachycardia = googledriveapi.createFolder('Ventricular tachycardia', drive_service)

	# Upload a File and save File ID
	# ecg = googledriveapi.uploadFile('ecg.jpg',drive_service,"C:\Laptop\Biodesign\Database python\ECG\ecg.png",'image/jpeg', Ventriculartachycardia)

	# Download a file
	# googledriveapi.downloadFile(ecg,drive_service,'C:\Laptop\Biodesign/attempt.jpg')

	# Search for a File
	# googledriveapi.searchFile(10,drive_service,"name contains 'Ventricular'")
	# googledriveapi.searchFile(10,drive_service,"parents in '1vXZWI5kVuwzOyePH65wbZyvtO-wPmh64'")

	# Create a folder and save Folder name and path
	# VTname, VTpath = raspberrysd.createFolder('Ventriculartachycardia','C:\Laptop\Biodesign\Final project')
	# ECGname, ECGpath = raspberrysd.createFolder('ECG', VTpath)

	# Trash folder in another folder
	# raspberrysd.trashFile(VTname + '/' + ECGname)
	
	# Simulating ADS1115
	# Measurements = [1,3,5,7,9]
	# Samples = []
	# for i in range(0,len(Measurements)):
	# 	Samples.append(i)

	# # Create a CSV file
	# CSVname, CSVpath = raspberrysd.createcsvFile(Samples,Measurements,'trying',VTname)
	# df1 = pd.read_csv(VTpath + '/' + CSVname + '.csv', delimiter=',')
	# print(df1) 