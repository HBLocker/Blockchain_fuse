use blockchainlib::*;
extern crate fuse;
use std::path::Path; 
use fuse::Filesystem;
use std::env::args;
struct NullFS;
impl Filesystem for NullFS {
}




fn main () {
    
    let mountpoint = match env::args().as_slice()
    {
        [,ref path] => Path::new(path),
        => {
            println!("Usage:{} <Mount_Point>"env::args()[0]);
            return; 
        }
    }

    


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
