#!/usr/bin/env/ python

#FusePy Dependancies
from __future__ import print_function, absolute_import, division
from fusepy import FUSE, FuseOSError, Operations, LoggingMixIn
from collections import defaultdict
from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
import argparse

#Python Logger Library
import logging
#Python DateTime Library
import datetime
#Path Library
from pathlib import Path
#Python Time Library
from time import time

#Custom Class Import
from pybc import PyBlockChain
from pyLogger import BlockChainLogger

#Class Block File System()
class BLOCK_FS(LoggingMixIn, Operations):

    #Initialise Python Blockchain
    n_chain = PyBlockChain()
    #Initialise Python Logger for Blockchain
    bcl = BlockChainLogger()
    #Set Working Directory (Where do the log files go)
    bcl.setWorkingDirectory("logs/")
    #Set User Mode (0 = Normal User, 1 = Super Admin)
    n_chain.setUserMode(0)
    #Creates Genesis Block (Will show as Initial Block)
    n_chain.createInitialBlock("Initial Block")
    

    # Sets default working directory when FUSE starts
    def __init__(self):
       self.files = {}
       self.data = defaultdict(bytes)
       self.fd = 0
       now = time()
       self.files['/'] = dict(
           st_mode=(S_IFDIR | 0o755),
           st_ctime=now,
           st_mtime=now,
           st_atime=now,
           st_nlink=2)

    # Create File (Path of file, file permissions mode e.g. 755)
    def create(self,path, mode):
        # Set File as Directory object
        self.files[path] = dict(
            st_mode=(S_IFREG | mode),
            st_nlink=1,
            st_size=0,
            st_ctime=time(),
            st_mtime=time(),
            st_atime=time())
        self.addChainLink("File Created",path,mode,None,time())
        self.fd += 1
        return self.fd
    #Get File attributes
    def getattr(self, path, fh=None):
        if path not in self.files:
            raise FuseOSError(ENOENT)

        return self.files[path]
    #Rename a File (Doesn't work)
    def rename(self, old, new):
        self.data[new] = self.data.pop(old)
        self.files[new] = self.files.pop(old)
    #Create a new Directory
    def mkdir(self, path, mode):
        self.files[path] = dict(
            st_mode=(S_IFDIR | mode),
            st_nlink=2,
            st_size=0,
            st_ctime=time(),
            st_mtime=time(),
            st_atime=time())
        self.addChainLink("Make Directory",path,mode,None,time())
        self.files['/']['st_nlink'] += 1
    #Create a File
    def touch(self, path, flags):
        self.fd += 1
        self.addChainLink("File Created",path,flags,None,time())
        return self.fd
    #Open a File
    def open(self, path, flags):
        self.fd += 1
        self.addChainLink("Open",path,flags,None,time())
        return self.fd
    #Read from a File 
    def read(self, path, size, offset, fh):
        return self.data[path][offset:offset + size]
    #Read a Directory(Check which Directory the user is in)
    def readdir(self, path, fh):
        #self.addChainLink("Read Directory",path,None,fh,time())
        return ['.', '..'] + [x[1:] for x in self.files if x != '/']
    #Delete a Directory
    def rmdir(self, path):
        self.files.pop(path)
        self.addChainLink("Remove Directory",path,None,None,time())
        self.files['/']['st_nlink'] -= 1
    #Status of the File System
    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

    

    # Add Block to Chain, Append Block to Logfile.
    def addChainLink(self,action,path,mode,data,timeStamp):
        # Get Block Data that is going to be stored
        blockData = ('\n\t\tAction Performed: %s\n\t\tPath: %s\n\t\tData: %s\n\t\tMode: %s\n\t\tTimeStamp: %s' %(action,path,data,mode,datetime.datetime.fromtimestamp(timeStamp).strftime('%c')))
        # Add Block data to Chain
        self.n_chain.addNewBlock(blockData)
        
        #Change Block Data
        if(len(self.n_chain.chain) > 4):
          #Changes data in a block at a specified index (index,data)
          self.n_chain.changeBlockData(2,"Up to no Good!")
          #Removes block at a specified index
          self.n_chain.removeBlock(2)

        #Check chain is still valid (Must be in user mode 1)
        result = self.n_chain.checkChainIntegrity()
        status="OK"
        if result == True:
           print('STATUS: OK')
           status="OK"
        else:
           print('STATUS: ERROR')
           for block in range(1,len(self.n_chain.chain)):
               curBlock = self.n_chain.chain[block]
               logBlock = ("Block Index: " + str(curBlock.index) + "\n\nHash: " + curBlock.nHash + "\n\n" + curBlock.data + "\n\nPHash: " + curBlock.pHash + "\n\n" + "Status: " + status + "\n\n" +"\n\nChain is Invaild, Error Log")
               # Write Data to Log File
               self.bcl.writeToLogFile(self.bcl.DIR,logBlock)
               status="ERROR"

        print(status)
        # Get length of chain
        chainlength = (len(self.n_chain.chain)-1)
        # Get Newest Block block[chain-length]
        getCurrentBlock = self.n_chain.chain[chainlength]
        # Create Log Data
        logBlock = ("Block Index: " + str(getCurrentBlock.index) + "\n\nHash: " + getCurrentBlock.nHash + "\n\n" + getCurrentBlock.data + "\n\nPHash: " + getCurrentBlock.pHash + "\n\n" + "Status: " + status + "\n\n")
        # Write Data to Log File
        self.bcl.writeToLogFile(self.bcl.DIR,logBlock)
        
#Initial Start Method
if __name__ == '__main__':
    #Initialise Parser
    parser = argparse.ArgumentParser()
    #Pass Mount Argument to Mout Virtual Disk
    parser.add_argument('mount')
    #Execute Parser Command
    args = parser.parse_args()
    #Create FusePy Instanace
    #logging.basicConfig(level=logging.DEBUG)
    fuse = FUSE(BLOCK_FS(), args.mount, foreground=True, nonempty=False, allow_other=True)
