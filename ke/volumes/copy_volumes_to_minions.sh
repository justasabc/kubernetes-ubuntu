#/bin/sh
filename=$(basename $0)

# add minion here
minions=(minion1 minion2 minion3)
master_path=../volumes
minion_path=/volumes

for m in "${minions[@]}" ;do
	echo "copying volumes to $m..."
	ssh $m rm -rf $minion_path

	scp -r $master_path $m:$minion_path
	ssh $m rm $minion_path/$filename
	echo "=============================="
done
