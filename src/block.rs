use std::fmt::{ self, Debug, Formatter };
use super::*;
extern crate fuse; 
use fuse::Filesystem; 
use std::os; 
use libc::{ENOENT, ENOSYS}; 
use fuse::{FileAttr, FileType,Request,ReplyAttr,ReplyData,ReplyEntry,ReplyDirectory}; //passes to the gen block here ^^
// calls each file being read 

pub struct Block {
    pub index: u32,
    pub timestamp: u128,
    pub hash: BlockHash,
    pub prev_block_hash: BlockHash,
    pub nonce: u64,
    pub payload: String,
}

impl Debug for Block {
    fn fmt (&self, f: &mut Formatter) -> fmt::Result {
        write!(f, "Block[{}]: {} at: {} with: {}",
            &self.index,
            &hex::encode(&self.hash),
            &self.timestamp,
            &self.payload,
        )
    }
}

impl Block {
    pub fn new (index: u32, timestamp: u128, prev_block_hash: BlockHash, nonce: u64, payload: String) -> Self {
        Block {
            index,
            timestamp,
            hash: vec![0; 32],
            prev_block_hash,
            nonce,
            payload,
            
        }
    }
}

impl Hashable for Block {
    fn bytes (&self) -> Vec<u8> {
        let mut bytes = vec![];

        bytes.extend(&u32_bytes(&self.index));
        bytes.extend(&u128_bytes(&self.timestamp));
        bytes.extend(&self.prev_block_hash);
        bytes.extend(&u64_bytes(&self.nonce));
        bytes.extend(self.payload.as_bytes());

        bytes
    }
}
