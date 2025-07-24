#!/bin/bash

FS_INSTALL=/user/kskovpen/analysis/SHiP/FairShip

source /cvmfs/ship.cern.ch/24.10/setUp.sh

export ALIBUILD_WORK_DIR=${FS_INSTALL}/sw
aliBuild build FairShip --always-prefer-system --config-dir $SHIPDIST --defaults release
alienv load FairShip/latest > test_config.sh
