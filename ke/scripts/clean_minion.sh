#/bin/sh
rm -rf /var/log/upstart/*
rm -rf /volumes/opensim_resources/ke/grid/services/*
rm -rf /volumes/opensim_resources/ke/grid/instances/*
rm -rf /volumes/opensim_resources/ke/.*.swp

containers=$(docker ps -a -q)
for c in $containers ;do
	#test $c && docker rm $c
	docker rm $c
done
