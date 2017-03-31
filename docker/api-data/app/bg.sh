#!/bin/bash
echo "Bash version ${BASH_VERSION}..."
for i in $(seq 1 10)
  do
     echo "Welcome $i times"
     sleep 1
  done
