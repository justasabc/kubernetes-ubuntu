#/bin/sh

ssh-keygen
ssh-copy-id root@minion1
ssh-copy-id root@minion2
ssh-copy-id root@minion3

# ssh minion1/minion2/minion3

