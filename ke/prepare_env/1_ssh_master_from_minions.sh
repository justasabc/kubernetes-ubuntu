#/bin/bash
# minion1
ssh-keygen
ssh-copy-id root@master

# minion2
ssh-keygen
ssh-copy-id root@master

# minion3
ssh-keygen
ssh-copy-id root@master
