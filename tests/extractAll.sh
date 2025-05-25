#!/bin/bash

cd build

for i in *.mod
do
    gunzip < "$i" > $i.txt
done