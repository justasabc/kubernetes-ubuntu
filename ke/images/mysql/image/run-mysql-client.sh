CONTAINER='mysql'
IP=$(docker inspect -f '{{ .NetworkSettings.IPAddress }}' $CONTAINER) 
echo $IP
#mysql -u opensim_user -popensim_pass -P 3306 -h $IP
mysql -u adminuser -padminpass -P 3306 -h $IP
