name=sim_0
pid=$(docker top $name | grep mono | awk '{print $2}' )
echo $pid
