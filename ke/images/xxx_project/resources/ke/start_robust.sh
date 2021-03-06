#/bin/sh
# manager for robust

function prepare_env() {
	BIN=/home/opensim80/bin
	cd $BIN

	MONO="/usr/bin/mono"
	ROBUST="$BIN/Robust.exe"
	export MONO_THREADS_PER_CPU=125
}

function service_env_setup() {
	# for robust
	export MYSQL_IP=$VGEOMYSQL_PORT_3306_TCP_ADDR
	#export LOCAL_IP=$(/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')
	export ROBUST_IP=$HOST_IP
	echo "=================================================="
	echo $INI_FILE
	echo $LOG_CONFIG
	echo $PID_FILE
	echo $LOG_FILE
	echo $MYSQL_IP
	echo $ROBUST_IP
	echo "=================================================="

}

function service_start() {
	# console basic|local|rest
	$MONO $ROBUST -logconfig="$LOG_CONFIG" -inifile="$INI_FILE" -console="basic"
}

function main() {
	prepare_env
	service_env_setup 
	service_start 
}

# start main function with all arguments
main $@
