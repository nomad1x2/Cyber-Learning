#!/bin/bash

#no input validation (yet), only last nn### digits are calculated

if [[ $# -eq 1 ]] # if arg provided, use it, otherwise use system umask
then
	input="000$1"
else
	input=$(umask)
fi

mask=$(printf '%d' "0$input") # parse octal string as dec int

# calculate mask for directory/file perms (default dir = 777, file = 666):
# ~mask flips the bits, AND with the default clears only the bits set in the mask

dir=$(printf '%03o' $((0777 & ~mask))) # formatted as 3 digits octal
file=$(printf '%03o' $((0666 & ~mask))) # same

# display octal perms as symbolic
to_symbolic() {
        local oct="$1" # first arg
        local sym="" # placeholder
        for d in "${oct:0:1}" "${oct:1:1}" "${oct:2:1}"; do # loop through each digit
		[[ $((d & 4)) -ne 0 ]] && sym+="r" || sym+="-" # read bit  (100)
		[[ $((d & 2)) -ne 0 ]] && sym+="w" || sym+="-" # write bit (010)
		[[ $((d & 1)) -ne 0 ]] && sym+="x" || sym+="-" # exec bit  (001)
        done
        echo "$sym"
}

echo "Umask: ${input: -3}"
echo "Directory permissions: $dir ($(to_symbolic $dir))"
echo "File permissions:      $file ($(to_symbolic $file))"
