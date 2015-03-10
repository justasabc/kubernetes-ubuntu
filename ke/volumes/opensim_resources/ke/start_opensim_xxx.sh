#/bin/sh
# manager for opensim

function prepare_env() {
	BIN=/home/opensim80/bin
	cd $BIN

	MONO="/usr/bin/mono"
	OPENSIM="$BIN/OpenSim.exe"
	export MONO_THREADS_PER_CPU=125
}

function sim_env_setup() {
	# for opensim
	# add 2 robust ips for opensim:  8002 ROBUST_PUBLIC_IP, 8003 ROBUST_INTERNAL_IP
	export MYSQL_IP=$MYSQL_SERVICE_SERVICE_HOST 
	export ROBUST_PUBLIC_IP=$ROBUST_PUBLIC_SERVICE_SERVICE_HOST 
	export ROBUST_INTERNAL_IP=$ROBUST_INTERNAL_SERVICE_SERVICE_HOST 
	export REGIONLOAD_WEB_URL="http://$APACHE_SERVICE_SERVICE_HOST:880/region_load/$SIM_NAME.xml"
	echo "=================================================="
	echo $SIM_NAME
	echo $SIM_PORT
	echo $INI_MASTER
	echo $INI_FILE
	echo $LOG_CONFIG
	echo $PID_FILE
	echo $LOG_FILE
	echo "mysql ip: $MYSQL_IP"
	echo "robust public ip: $ROBUST_PUBLIC_IP"
	echo "robust internal ip: $ROBUST_INTERNAL_IP"
	echo "regionload url: $REGIONLOAD_WEB_URL"
	echo "=================================================="

}

function sim_start() {
	# console basic|rest|empty
	# http://opensimulator.org/wiki/OpenSim.exe_Command_Line_Options
	# basic will lead to cursor error
	#$MONO $OPENSIM -logconfig="$LOG_CONFIG" -inimaster="$INI_MASTER" -inifile="$INI_FILE" -console="basic"
	$MONO $OPENSIM -logconfig="$LOG_CONFIG" -inimaster="$INI_MASTER" -inifile="$INI_FILE" 
}

function main() {
	prepare_env
	sim_env_setup 
	sim_start 
}

# start main function with all arguments
main $@
