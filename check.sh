#!/bin/bash 

find . -name 'checker.py' | while read line; do
    echo "Processing checker '$line'"
    "$line" check 127.0.0.1
    A=$?
    if [ $A != 101 ]
    then 
    	echo "Check failed! Got code $A from CHECK"
    	false
    else
    	echo "Check passed!"
    	true
    fi

    OUT=`"$line" put 127.0.0.1 123 AAAAAAAACAAAAAAAAAAAAABAAAAAAAA= 1`
    A=$?
    if [ $A != 101 ]
    then 
    	echo "Check failed! Got code $A from PUT"
    	false
    else
    	echo "Check passed!"
    	true
    fi

    "$line" get 127.0.0.1 $OUT AAAAAAAACAAAAAAAAAAAAABAAAAAAAA= 1
    A=$?
    if [ $A != 101 ]
    then 
    	echo "Check failed! Got code $A from PUT"
    	false
    else
    	echo "Check passed!"
    	true
    fi
done