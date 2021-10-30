#!/bin/bash

rm -r results.txt

time python3 qc.py -test dev.txt -train trainWithoutDev.txt > results.txt
python3 acc.py
