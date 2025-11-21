#!/bin/bash

FS_INSTALL=/cvmfs/ship.cern.ch/25.11/

export WORK_DIR=${FS_INSTALL}/sw/
source ${FS_INSTALL}/sw/slc9_x86-64/FairShip/latest/etc/profile.d/init.sh

echo "INFO: Environment set up for FairShip located at " $FS_INSTALL

echo "INFO: Executing: python ${FS_INSTALL}/sw/slc9_x86-64/FairShip/latest/muonShieldOptimization/run_fixedTarget.py" $@

python ${FS_INSTALL}/sw/slc9_x86-64/FairShip/latest/muonShieldOptimization/run_fixedTarget.py $@

echo "INFO: Finished running. These files are on the WN:"
ls -lh
