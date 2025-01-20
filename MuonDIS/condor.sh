#!/bin/bash

#######################################################################################
source /cvmfs/ship.cern.ch/24.10/setUp.sh 

source /afs/cern.ch/user/a/anupamar/HTCondor/configfiles/config_ECN3_2024.sh #alienv load FairShip/latest-master-release > config_<version>.sh
echo 'config sourced'

#######################################################################################

python $FAIRSHIP/muonDIS/make_nTuple_SBT.py &
python $FAIRSHIP/muonDIS/make_nTuple_Tr.py 
wait

xrdcp muonsProduction_wsoft_SBT.root /eos/experiment/ship/simulation/bkg/MuonDIS_2024helium/8070735/muonsProduction_wsoft_SBT_1spill_8070735.root
xrdcp SelectedMuonsSBT.txt /eos/experiment/ship/simulation/bkg/MuonDIS_2024helium/8070735/SelectedMuonsSBT_1spill_8070735.txt

xrdcp muonsProduction_wsoft_Tr.root /eos/experiment/ship/simulation/bkg/MuonDIS_2024helium/8070735/muonsProduction_wsoft_Tr_1spill_8070735.root
xrdcp SelectedMuonsTr.txt /eos/experiment/ship/simulation/bkg/MuonDIS_2024helium/8070735/SelectedMuonsTr_1spill_8070735.txt