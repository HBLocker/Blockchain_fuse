use blockchainlib::*;
extern crate fuse;
use std::path::Path; 
use fuse::Filesystem;
use std::env::args;
struct NullFS;
impl Filesystem for NullFS { //calls fuse file system type 
}




fn main () {
    
    let mountpoint = match env::args().as_slice() //debugging creates a mount point for the part of the file system
    {
        [,ref path] => Path::new(path), //pushes to path 
        => {
            println!("Usage:{} <Mount_Point>"env::args()[0]); //prints mountd system (DOES NOT WORK YET)
            return; 
        }
    }

    
//block functions beiing called

    let mut i = 0;
    while i < 3{
    let mut block = Block::new(i, 0, vec![0; 32], 0, "Genesis block!".to_owned());

    println!("{:?}", &block);

    let h = block.hash();

    println!("{:?}", &h);

    block.hash = h;

    println!("{:?}", &block);
    i = i+1;
}


}
