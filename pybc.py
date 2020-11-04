#!bin/bash
"""
Python Block Chain Lib


/////////////////////////
/BlockChain Python Class/
/////////////////////////
/// Create Function   ///
/// Add Function      ///
/// Remove Function   ///
/// Print Function    ///
/// WriteLog Function ///
/////////////////////////

"""

""" Imported Libs"""

from block import Block

""" BlockChain Class """

class PyBlockChain():

    """ Store List Validity """
    isValid = False
    """ Check if user is Root (Enable Chain Repair Method)"""
    isRoot = False
    """ Declare Chain """
    chain = []
    """ SET SALT """
    superSecretSalt = ""

    """ Define User Mode """
    def setUserMode(self,flag):
        print(flag)
        if flag == 0:
            self.isRoot = False
        elif flag == 1:
            self.isRoot = True

    """ Create Genisis Block """
    def createInitialBlock(self,data):
        """ Set Instance of Block """
        initalBlock = Block()
        """ Set Hash Salt """
        initalBlock.superSecretSalt = self.superSecretSalt

        """ Add Data to Block """
        initalBlock.data = data
        """ Set Null for Prevoius Hash as None Exist Yet """
        initalBlock.pHash = initalBlock.genHash(None,data)
        """ Set Block Index to 0 """
        initalBlock.index = 0
        """ Set Initial Block Hash """
        initalBlock.nHash = initalBlock.genHash("0",data)
        """ Add Block to the Chain """
        self.chain.append(initalBlock)

    """ Add New Block """
    def addNewBlock(self,data):
        """ Set Instance of Block """
        newBlock = Block()
        """ Add Data to Block """
        newBlock.data = data
        """ Set Previous Hash Equal to the Hash of the First Block """
        newBlock.pHash = self.chain[len(self.chain) - 1].nHash
        getPHASH = self.chain[len(self.chain) - 1].nHash
        """ Set Block Index to Number of Blocks on the Chain """
        newBlock.index = len(self.chain)
        """ Set New Block Hash """
        newBlock.nHash = newBlock.genHash(getPHASH,newBlock.data)
        """ Add Block to the Chain """
        self.chain.append(newBlock)

    """ Remove Block """
    def removeBlock(self,sel_index):
        """ Remove Block From Chain """
        self.chain.remove(self.chain[sel_index])
        """ Update Block Indices after block removed """
        while sel_index < len(self.chain):
            """ Index -=1 """
            self.chain[sel_index].index -= 1
            """ is Root User Enabled? """
            if self.isRoot == True:
                """ Repair Chain Continuity """
                self.chain[sel_index-1].nHash = self.chain[sel_index].pHash
            """ Interate selected index by 1 """
            sel_index+=1

    def changeBlockData(self,sel_index,data):

        self.chain[sel_index].data = data

    def checkChainIntegrity(self):

        tweight = 0
        fweight = 0

        if (len(self.chain)) > 1:

            for index in range(1,len(self.chain)):
                # Check the hash of the current block
                # Get Current Block Data & Previous Hash and Hash these values
                data = self.chain[index].data
                print(data)
                pHash = self.chain[index-1].nHash
                # Instance of Block to get access to Gen Hash Function
                x = Block()
                # Check Hash = genHash (Previous Hash and Current Block Data)
                checkHash = x.genHash(pHash,data)

                # Does the current block = check hash value
                if (self.chain[index].nHash == checkHash):
                    # Yes +1 to truth Weight
                    tweight +=1
                else:
                    # No +1 to false weight
                    fweight +=1

        """ if fweight is greater than 0, chain has a problem """
        if fweight > 0:
            """ Return false on Integrity Check """
            return False
        else:
            """ Return True on Integrity Check if fweight = 0 """
            return True

    """ Print Chain """
    def printChain(self):
        """ Iterate over Chain """
        for i in self.chain:
            """ if the block is @ index 0, Add 'Printing BLocks' """
            if i.index == 0:
                print("\nPrinting Blocks\n")
                print("Block Index: %x" % i.index)
                print("Block Hash:  %s\n" % i.nHash)
                print("\t Block Data:  %s\n" % i.data)
                print("Block PHash: %s" % i.pHash)
                print("\n")
            else:
                """ Print the rest of the chain """
                print("\n")
                print("Block Index: %x" % i.index)
                print("Block Hash:  %s\n" % i.nHash)
                print("\t Block Data:  %s\n" % i.data)
                print("Block PHash: %s" % i.pHash)
                print("\n")
