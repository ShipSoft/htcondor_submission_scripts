#!/bin/bash

FS_INSTALL=/user/kskovpen/analysis/SHiP/FairShip

source /cvmfs/ship.cern.ch/24.10/setUp.sh

export ALIBUILD_WORK_DIR=${FS_INSTALL}/sw

source ${FS_INSTALL}/../htcondor_submission_scripts/fixedTarget/batch/test_config.sh

echo "INFO: Environment set up for FairShip located at " $FAIRSHIP

echo "INFO: Executing: python ${FAIRSHIP_INSTALL}/muonShieldOptimization/run_fixedTarget.py" $@

python ${FS_INSTALL}/muonShieldOptimization/run_fixedTarget.py $@

echo "INFO: Finished running. These files are on the WN:"
ls -lh
