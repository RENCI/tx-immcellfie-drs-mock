#!/bin/bash
uvicorn --host $1 --port $2 --reload main:app 
