""" Block Chain Logger Class """

# Imports
import os
import time

# Class
class BlockChainLogger(object):

 # Directory Path where logs are being written to.
 DIR = "/"
 # Set Working Directory
 def setWorkingDirectory(self,dir):
     self.DIR = dir
 # Count number of log files in the directory
 def countLogFiles(self):
     list = os.listdir(self.DIR)
     numFiles = len(list)
     return numFiles
     
 # Write Data to log file
 def writeToLogFile(self,directory,data):
     x = time.strftime("%d-%m-%Y")
     filename = ("%s.log") % x
     f = open(directory +"/"+ filename, "a")
     dataToWrite = ("%s") % data
     f.write(dataToWrite)
     f.close()

 # Read Log file data.
 def readLogFile(self,directory,fileName):
     f = open(directory+"/"+fileName, "r")
     print(f.read())
