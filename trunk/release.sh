#!/bin/bash

TARGETDIR=/incoming

release="$1" ; shift
if [ -e "$release" ] ; then
    echo "Fehler: Erstes Argument muss Release sein!"
    exit 10
fi

function upload () {
    test="$1" ; shift
    for name in "$@" ; do
	ext=${name/*./.}
	basename=$(basename $name $ext)
	target="$TARGETDIR/$basename-$release$ext"

	if [ -z "$test" ] ; then
	    ncftpput -C ftp.berlios.de $name $target
	else
	    echo "Uploading $name as $target"
	fi
    done
}

echo
upload "test" "$@"
echo
read -p "Okay? (y/n) " -n 1 okay
echo

if [ "$okay" == "y" -o "$okay" == "Y" ] ; then
    upload "" "$@"
else
    echo "Abbruch ..."
    exit 0
fi
