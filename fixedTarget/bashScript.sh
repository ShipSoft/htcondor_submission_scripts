#!/bin/bash

source /vols/lhcb/masmith/SHiP/FairShip/setUp.sh
export ALIBUILD_WORK_DIR=/vols/lhcb/masmith/SHiP/FairShip/sw/
alienv load FairShip/latest > test_config.sh
source test_config.sh

echo 'getting there'
echo $FAIRSHIP

echo 'INFO: Executing: python /vols/lhcb/masmith/SHiP/FairShip/muonShieldOptimization/run_fixedTarget.py' $@

python /vols/lhcb/masmith/SHiP/FairShip/muonShieldOptimization/run_fixedTarget.py $@

ls -lh
