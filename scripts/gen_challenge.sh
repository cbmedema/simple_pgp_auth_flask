#!/bin/bash
num=0
chr=""
dir=/home/bryce/website/encrypted/src/scripts
chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
for i in {1..64}; do 
    # generate a 8 byte unsigned number that is quite random
    num=$(od -vAn -N4 -tu4 < /dev/urandom)
    index=$(($num%62))
    chr+="${chars:$index:1}"
done
echo $chr > "$dir/solution.txt"

gpg --batch --yes --no-tty -o "$dir/encrypted.txt" \
-r admin@localhost -a -e "$dir/solution.txt"


