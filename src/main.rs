use blockchainlib::*;

fn main () {
    let mut i = 0;
    while i < 100{
    let mut block = Block::new(i, 0, vec![0; 32], 0, "Genesis block!".to_owned());

    println!("{:?}", &block);

    let h = block.hash();

    println!("{:?}", &h);

    block.hash = h;

    println!("{:?}", &block);
    i = i+1;
}
}
