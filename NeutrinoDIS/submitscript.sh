#!/bin/bash

EOSDIR=$1 # output directory 
nEvents=$2
ProcId=$3
ClusterId=$4

source /cvmfs/ship.cern.ch/24.10/setUp.sh 
source /afs/cern.ch/user/a/anupamar/HTCondor/configfiles/config_ECN3_2024.sh #alienv load FairShip/latest-master-release > config_<version>.sh

echo 'config sourced'

mkdir -p "$EOSDIR/$ClusterId/job_$ProcId"

OUTPUTDIR="$EOSDIR/$ClusterId/job_$ProcId"


output_files=(
    "$OUTPUTDIR/ship.conical.Genie-TGeant4.root"
    "$OUTPUTDIR/ship.params.conical.Genie-TGeant4.root"
    "$OUTPUTDIR/simulation_output.txt"
    "$OUTPUTDIR/geofile_full.conical.Genie-TGeant4.root"
    "$OUTPUTDIR/ship.conical.Genie-TGeant4_rec.root"
)


step1() {
    echo 
    echo " Step 1: Neutrino DIS simulation using run_simScript.py"
    echo "=============================================================="
    
    python "$FAIRSHIP/macro/run_simScript.py" --helium --Genie -f /eos/experiment/ship/user/Iaroslava/NeutrinoSample2024/genie_3.2/genie-nu_mu_full.root -n $nEvents | tee simulation_output.txt
   
    xrdcp "ship.conical.Genie-TGeant4.root" root://eospublic.cern.ch/"$OUTPUTDIR"/ &
    xrdcp "geofile_full.conical.Genie-TGeant4.root" root://eospublic.cern.ch/"$OUTPUTDIR"/ &
    xrdcp "ship.params.conical.Genie-TGeant4.root" root://eospublic.cern.ch/"$OUTPUTDIR"/ &
    xrdcp simulation_output.txt root://eospublic.cern.ch/"$OUTPUTDIR"/ &
    wait
}

step2() {
    echo 
    echo " Step 2: Reconstruction using ShipReco.py"
    echo "=============================================================="
    
    python "$FAIRSHIP/macro/ShipReco.py" -f "ship.conical.Genie-TGeant4.root" -g "geofile_full.conical.Genie-TGeant4.root"
    
    xrdcp "ship.conical.Genie-TGeant4_rec.root" root://eospublic.cern.ch/"$OUTPUTDIR"/
}


nothing_to_do=true  

for i in {0..3}; do # Check if any files from Step 1 (files 1-3) are missing
    if [ ! -f "${output_files[$i]}" ]; then
        
        nothing_to_do=false
        
        echo "${output_files[$i]} is missing, removing subsequent files and rerunning steps."
        
        for file in "${output_files[@]}"; do # Remove all subsequent files from Step 1 and Step 2, but only if they exist
            if [ -f "$file" ]; then
                echo "Removing $file"
                rm "$file"
            fi
        done
        
        step1  # Rerun Step 1
        break  # Stop checking further once a missing file from Step 2 is found
    fi
done

if [ ! -f "${output_files[4]}" ]; then # Check if any file from Step 2 is missing ( just the final file)
    
    nothing_to_do=false
    echo "${output_files[4]} is missing, rerunning Step 2."
    step2  # Rerun Step 2
fi


if [ "$nothing_to_do" = true ]; then
    echo 'Nothing to do. All necessary files are present.'
fi
