#!/bin/bash


ruby /lich/lich.rb -s --game=DR -g dr.simutronics.net:4901 &

cd /pylanthia && pipenv install && pipenv run python3 pylanthia.py
