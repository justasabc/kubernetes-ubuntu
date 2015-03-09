# kubernetes-ubuntu
kubernetes on ubuntu

# Steps
## generate conf

	cd ./ubuntu/default_scripts/conf-generator
	./run-me

## copy binary and conf files (master)

	cd ./ubuntu/
	./master.sh

## copy binary and conf files (minion)

	cd ./ubuntu/
	./minion.sh
