#!/bin/bash

EOSDIR=$1 
muonTupleFile=$2 
ProcId=$3 
MuonsPerJob=$4 
DISPerMuon=$5 

firstEvent=$((ProcID*MuonsPerJob)) 

source /cvmfs/ship.cern.ch/24.10/setUp.sh 
source /afs/cern.ch/user/a/anupamar/alt_sw/config_muonDIS.sh #HTCondor/configfiles/config_ECN3_2024.sh #alienv load FairShip/latest-master-release > config_<version>.sh

echo 'config sourced'

mkdir -p "$EOSDIR/job_$ProcId"

OUTPUTDIR="$EOSDIR/job_$ProcId"


output_files=(
    "$OUTPUTDIR/muonDis.root"
    "$OUTPUTDIR/ship.conical.muonDIS-TGeant4.root"
    "$OUTPUTDIR/ship.params.conical.muonDIS-TGeant4.root"
    "$OUTPUTDIR/simulation_output.txt"
    "$OUTPUTDIR/geofile_full.conical.muonDIS-TGeant4.root"
    "$OUTPUTDIR/ship.conical.muonDIS-TGeant4_rec.root"
)

step1() {
    echo 
    echo "Running Step 1: making MuonDIS from the muons hitting SBT / Tracking Station 1"
    echo "=============================================================="
    python "$FAIRSHIP/muonDIS/makeMuonDIS.py" -f "$muonTupleFile" -i "$firstEvent" --nDIS "$DISPerMuon" -n "$MuonsPerJob"
    xrdcp muonDis.root root://eospublic.cern.ch/"$OUTPUTDIR"/
}

step2() {
    echo 
    echo "Running Step 2: running the muonDIS simulation"
    echo "=============================================================="
    python "$FAIRSHIP/macro/run_simScript.py" --MuDIS -f "muonDis.root" --firstEvent 0 --nEvents $((MuonsPerJob*DISPerMuon)) | tee simulation_output.txt
    echo "MuDIS simulation done. Adding the original muon's SBT response to the simulation."
    python "$FAIRSHIP/muonDIS/add_muonresponse.py" -m "muonDis.root" -f "ship.conical.muonDIS-TGeant4.root"
    
    xrdcp "ship.conical.muonDIS-TGeant4.root" root://eospublic.cern.ch/"$OUTPUTDIR"/ &
    xrdcp "geofile_full.conical.muonDIS-TGeant4.root" root://eospublic.cern.ch/"$OUTPUTDIR"/ &
    xrdcp "ship.params.conical.muonDIS-TGeant4.root" root://eospublic.cern.ch/"$OUTPUTDIR"/ &
    xrdcp simulation_output.txt root://eospublic.cern.ch/"$OUTPUTDIR"/ &
    wait
        
}

step3() {
    echo 
    echo "Running Step 3: Running Reconstruction"
    echo "=============================================================="
    python "$FAIRSHIP/macro/ShipReco.py" -f "ship.conical.muonDIS-TGeant4.root" -g "geofile_full.conical.muonDIS-TGeant4.root"
    xrdcp "ship.conical.muonDIS-TGeant4_rec.root" root://eospublic.cern.ch/"$OUTPUTDIR"/
}

nothing_to_do=true  # Flag to track if any file is missing


if [ ! -f "${output_files[0]}" ]; then # Check if files for Step 1 are missing
    nothing_to_do=false
    echo "${output_files[0]} is missing, removing subsequent files and rerunning steps."
    
    for file in "${output_files[@]}"; do # Remove all subsequent files (from Step 1 to 3) if they exist
        if [ -f "$file" ]; then
            echo "Removing $file"
            rm "$file"
        fi
    done
    step1  # Rerun Step 1
fi


for i in {1..4}; do # Check if any files from Step 2 files 2-4) are missing
    if [ ! -f "${output_files[$i]}" ]; then
        nothing_to_do=false
        echo "${output_files[$i]} is missing, removing subsequent files and rerunning steps."
        
        for file in "${output_files[@]:1}"; do # Remove all subsequent files from Step 2 and Step 3, but only if they exist
            if [ -f "$file" ]; then
                echo "Removing $file"
                rm "$file"
            fi
        done
        step2  # Rerun Step 2
        break  # Stop checking further once a missing file from Step 2 is found
    fi
done


if [ ! -f "${output_files[5]}" ]; then # Check if any file from Step 3 is missing ( just the final file)
    
    nothing_to_do=false
    echo "${output_files[5]} is missing, rerunning Step 3."
    
    if [ -f "${output_files[5]}" ]; then # Remove only the Step 3 file if it exists
        echo "Removing ${output_files[5]}"
        rm  "${output_files[5]}"
    fi
    step3  # Rerun Step 3
fi


if [ "$nothing_to_do" = true ]; then
    echo 'Nothing to do. All necessary files are present.'
fi