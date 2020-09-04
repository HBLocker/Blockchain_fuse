use blockchainlib::*;
extern crate fuse;
use std::path::Path;

use fuse::Filesystem;
struct NullFS;

impl Filesystem for NullFS {
}



fn main () {

    let mountpoint = std::path::Path::new(std::os::args()[1].as_slice());
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
