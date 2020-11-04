#!bin/bash
"""
Python Block Chain Lib


//////////////////////////////////////////////////
/// Block Python Class  Data Structure Visual ///
/////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////
/// Genisis Block  ///  Link ///    Block 1  /// Link ///   Block 2  ///
////////////////////////////////////////////////////////////////////////
///        Hash ---------v   ///     Hash --------v   ///            ///
///       (Data)   ///   v   ///    (Data)  ///   v   ///            ///
Null<-- Prev Hash  ///   v---> <- Prev Hash ///   v--> next block... ///
///                ///       ///            ///       ///            ///
////////////////////////////////////////////////////////////////////////

"""
""" Import Libs """
import string
import random
import hashlib

""" Block Class """

class Block():

    """ Block Data Variables """

    """  Block Hash  """
    nHash = None
    """  Block Data  """
    nData = None
    """  Prev  Hash  """
    pHash = None
    """  Block Index """
    index = None

    """ Generate Hash Function """

    def genHash(self,phash,nData):
        """Set Hashable String"""
        hashData = bytes("%s %s" % (phash,nData),encoding='utf8')
        """ Generate a sha256 Hash """
        newHash = hashlib.sha256(b"%b" % hashData).hexdigest()
        """ Return Hash """
        return newHash
