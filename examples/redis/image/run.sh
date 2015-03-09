#!/bin/bash

function launchmaster() {
  if [[ ! -e /redis-master-data ]]; then
    echo "Redis master data doesn't exist, data won't be persistent!"
    mkdir /redis-master-data
  fi
  redis-server /redis-master/redis.conf
}

function launchsentinel() {
  master=$(redis-cli -h ${REDIS_SENTINEL_SERVICE_HOST} -p ${REDIS_SENTINEL_SERVICE_PORT} --csv SENTINEL get-master-addr-by-name mymaster | tr ',' ' ' | cut -d' ' -f1)
  if [[ -n ${master} ]]; then
    master="${master//\"}"
  else
    master=$(hostname -i)
  fi

  sentinel_conf=sentinel.conf
#  curl http://${KUBERNETES_RO_SERVICE_HOST}:${KUBERNETES_RO_SERVICE_PORT}/api/v1beta1/endpoints/redis-master | python /sentinel.py > ${sentinel_conf}

  echo "sentinel monitor mymaster ${master} 6379 2" > ${sentinel_conf}
  echo "sentinel down-after-milliseconds mymaster 60000" >> ${sentinel_conf}
  echo "sentinel failover-timeout mymaster 180000" >> ${sentinel_conf}
  echo "sentinel parallel-syncs mymaster 1" >> ${sentinel_conf}

  redis-sentinel ${sentinel_conf}
}

function launchslave() {
  if [[ -x ${REDIS_MASTER_SERVICE_HOST} ]]; then
    echo "Redis master service can't be found."
    exit 1
  fi

  perl -pi -e "s/%master-ip%/${REDIS_MASTER_SERVICE_HOST}/" /redis-slave/redis.conf
  perl -pi -e "s/%master-port%/${REDIS_MASTER_SERVICE_PORT}/" /redis-slave/redis.conf
  redis-server /redis-slave/redis.conf
}

if [[ "${MASTER}" == "true" ]]; then
  launchmaster
  exit 0
fi

if [[ "${SENTINEL}" == "true" ]]; then
  launchsentinel
  exit 0
fi

launchslave
