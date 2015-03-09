#/bin/sh

# add minion here
minions=(minion1 minion2 minion3)
env_root=/root/prepare_env

for m in "${minions[@]}" ;do
	ssh $m rm -rf $env_root

	echo "copying files to $m..."
	ssh $m mkdir -p $env_root/

	scp -r pre/* $m:$env_root/
	echo "=============================="
done
