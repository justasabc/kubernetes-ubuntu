import json
import sys

data = json.load(sys.stdin)

if data and "endpoints" in data and len(data["endpoints"]) > 0:
  host = data["endpoints"][0].split(":")[0]
else:
  host = "localhost"

print "sentinel monitor mymaster %s 6379 2" % host
print "sentinel down-after-milliseconds mymaster 60000"
print "sentinel failover-timeout mymaster 180000"
print "sentinel parallel-syncs mymaster 1"

