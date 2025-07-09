#!/bin/bash

source /vols/lhcb/masmith/SHiP/FairShip/setUp.sh
export ALIBUILD_WORK_DIR=/vols/lhcb/masmith/SHiP/FairShip/sw/
alienv load FairShip/latest > test_config.sh
source test_config.sh

echo 'INFO: Environment set up for FairShip located at ' $FAIRSHIP

echo 'INFO: Executing: python /vols/lhcb/masmith/SHiP/FairShip/muonShieldOptimization/run_fixedTarget.py' $@

python /vols/lhcb/masmith/SHiP/FairShip/muonShieldOptimization/run_fixedTarget.py $@

echo 'INFO: Finished running. These files are on the WN:'
ls -lh
