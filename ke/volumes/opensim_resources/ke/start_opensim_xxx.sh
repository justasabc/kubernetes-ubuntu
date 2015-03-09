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
	#export MYSQL_IP=$VGEOMYSQL_PORT_3306_TCP_ADDR 
	#export ROBUST_IP=$VGEOROBUST_PORT_8003_TCP_ADDR
	export MYSQL_IP=$MYSQL_SERVICE_SERVICE_HOST 
	export ROBUST_IP=$ROBUST_SERVICE_SERVICE_HOST 
	echo "=================================================="
	echo $SIM_NAME
	echo $SIM_PORT
	echo $INI_MASTER
	echo $INI_FILE
	echo $LOG_CONFIG
	echo $PID_FILE
	echo $LOG_FILE
	echo $REGIONLOAD_WEB_URL
	echo $MYSQL_IP
	echo $ROBUST_IP
	echo "=================================================="

}

function sim_start() {
	# console basic|rest|empty
	# http://opensimulator.org/wiki/OpenSim.exe_Command_Line_Options
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
