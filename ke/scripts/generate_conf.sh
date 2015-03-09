#!/bin/sh
cd ./default_scripts/conf-generator
for i in $(ls .);do
	/bin/sh $i
done
