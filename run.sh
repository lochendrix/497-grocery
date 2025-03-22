#!/bin/bash
source ./env/bin/activate
cd server
python init_db.py
python app.py