#!/bin/bash

EOSDIR=$1
muonTupleFile=$2
ProcId=$3
MuonsPerJob=$4 
DISPerMuon=$5 
     
firstEvent=$((ProcId*MuonsPerJob))

source /cvmfs/ship.cern.ch/24.10/setUp.sh 
source /afs/cern.ch/user/a/anupamar/HTCondor/configfiles/config_ECN3_2024.sh #alienv load FairShip/latest-master-release > config_<version>.sh

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
    echo "Generating DIS for muons hitting SBT / Tracking Station 1"
    echo "============================================================================================================================"
    echo

    python "$FAIRSHIP/muonDIS/makeMuonDIS.py" --inputFile "$muonTupleFile" -i "$firstEvent" --nDIS "$DISPerMuon" --nEvents "$MuonsPerJob"

    if [ $? -ne 0 ]; then
        echo "ERROR: Step 1 failed. Exiting script."
        exit 1
    fi
    echo "Copying files..."
    xrdcp muonDis.root root://eospublic.cern.ch/"$OUTPUTDIR"/ 

}

step2() {

    echo
    echo "MuonDIS simulation using run_simScript.py"
    echo "============================================================================================================================"
    echo

    python "$FAIRSHIP/macro/run_simScript.py" --MuDIS -f root://eospublic.cern.ch/"$OUTPUTDIR/muonDis.root" --firstEvent 0 --nEvents $((MuonsPerJob*DISPerMuon)) --helium | tee simulation_output.txt

    echo
    echo "MuDIS simulation done. Adding the original muon's SBT response to the simulation."
    echo

    python "$FAIRSHIP/muonDIS/add_muonresponse.py" -m root://eospublic.cern.ch/"$OUTPUTDIR/muonDis.root" -f "ship.conical.muonDIS-TGeant4.root"
    
    if [ $? -ne 0 ]; then
        echo "ERROR: Step 2 failed. Exiting script."
        exit 1
    fi

    echo "Copying files..."

    xrdcp "ship.conical.muonDIS-TGeant4.root" root://eospublic.cern.ch/"$OUTPUTDIR"/
    xrdcp "geofile_full.conical.muonDIS-TGeant4.root" root://eospublic.cern.ch/"$OUTPUTDIR"/
    xrdcp "ship.params.conical.muonDIS-TGeant4.root" root://eospublic.cern.ch/"$OUTPUTDIR"/
    xrdcp simulation_output.txt root://eospublic.cern.ch/"$OUTPUTDIR"/

}

step3() {

    echo
    echo "Reconstruction of the MuonDIS files"
    echo "============================================================================================================================"
    echo 

    python "$FAIRSHIP/macro/ShipReco.py" -f root://eospublic.cern.ch/"$OUTPUTDIR/ship.conical.muonDIS-TGeant4.root" -g root://eospublic.cern.ch/"$OUTPUTDIR/geofile_full.conical.muonDIS-TGeant4.root"

    if [ $? -ne 0 ]; then
        echo "ERROR: Step 3 failed. Exiting script."
        exit 1
    fi

    echo "Copying files..."
    xrdcp "ship.conical.muonDIS-TGeant4_rec.root" root://eospublic.cern.ch/"$OUTPUTDIR"/ 

}

nothing_to_do=true
SECONDS=0  # Reset timer

echo
if [ ! -f "${output_files[0]}" ]; then # Check if files for Step 1 are missing

    nothing_to_do=false

    echo "${output_files[0]} is missing, removing subsequent files if they exist and rerunning steps."
    
    for file in "${output_files[@]}"; do # Remove all subsequent files (from Step 1 to 3) if they exist
        if [ -f "$file" ]; then
            echo "Removing $file"
            rm "$file"
        fi
    done
    echo
    echo "STEP 1/3:"
    step1  # Run Step 1
    echo "STEP 1/3: Completed"

fi

if [ "$nothing_to_do" = true ]; then
    echo 'Skipping STEP 1/3; output files exist.'
fi

echo "-----------------------------------------------------------------------------------------------Time taken $(echo "scale=2; $SECONDS / 60" | bc) minutes"
SECONDS=0  # Reset timer
echo
for i in {1..4}; do # Check if any files from Step 2 files 2-4) are missing

    if [ ! -f "${output_files[$i]}" ]; then

        nothing_to_do=false

        echo "${output_files[$i]} is missing, removing subsequent files if they exist and rerunning steps."
        
        for file in "${output_files[@]:1}"; do # Remove all subsequent files from Step 2 and Step 3, but only if they exist
            if [ -f "$file" ]; then
                echo "Removing $file"
                rm "$file"
            fi
        done

        echo
        echo "STEP 2/3:"
        step2  # Run Step 2
        echo "STEP 2/3: Completed"

        break  # Stop checking further once a missing file from Step 2 is found
    fi
done

if [ "$nothing_to_do" = true ]; then
    echo 'Skipping STEP 2/3; output files exist.'
fi
echo "-----------------------------------------------------------------------------------------------Time taken $(echo "scale=2; $SECONDS / 60" | bc) minutes"
SECONDS=0  # Reset timer

echo
if [ ! -f "${output_files[5]}" ]; then # Check if any file from Step 3 is missing ( just the final file)
    
    nothing_to_do=false
    echo "${output_files[5]} is missing, rerunning Step 3."
    
    if [ -f "${output_files[5]}" ]; then # Remove only the Step 3 file if it exists
        echo "Removing ${output_files[5]}"
        rm  "${output_files[5]}"
    fi
    echo
    echo "STEP 3/3:"
    step3  # Rerun Step 3
    echo "STEP 3/3: Completed"
fi

if [ "$nothing_to_do" = true ]; then
    echo 'Skipping STEP 3/3; output files exist.'
fi

echo "-----------------------------------------------------------------------------------------------Time taken $(echo "scale=2; $SECONDS / 60" | bc) minutes"
SECONDS=0  # Reset timer
