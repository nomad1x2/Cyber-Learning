#!/bin/bash

DIR=/home/nomad/dir_test
FILE=specific_file

############

echo -e "Checking if $DIR exists:\n"
if [[ ! -d $DIR ]]
then
	echo -e "$DIR does not exist. Creating $DIR:\n"
	mkdir $DIR
else
	echo -e "$DIR exists.\n"
fi

############

if [[ ! -f $DIR/$FILE ]]
then
	echo -e "$FILE does not exist. Creating $FILE:\n"
	touch $DIR/$FILE
else
	echo -e "$FILE exists, listing:\n"
fi

############

ls -lsR $DIR


