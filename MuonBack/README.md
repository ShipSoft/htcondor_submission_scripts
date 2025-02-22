
# Condor Scripts to generate MuonBackground using Fairship

Thesse scripts have been used to produce the MuonBackground Files(weighted to a spill) available in `/eos/experiment/ship/simulation/bkg/MuonBack_2024helium`. 

If you do not already have FairShip, please follow the [Fairship README](https://github.com/ShipSoft/FairShip?tab=readme-ov-file#build-instructions-using-cvmfs) to build the software (Steps 1-4) to use within lxplus.

To reuse the scripts, follow the step by step guide:

## 0. Clone the Repository

```bash
cd /afs/cern.ch/user/<path>/<to_your_folder>
git clone https://github.com/anupama-reghunath/HTCondor_scripts.git
```

## 1. Load the Environment for use within HTCondor

Source the setup script (replace \$SHIP_RELEASE with the release you want to use):
```bash
source /cvmfs/ship.cern.ch/$SHIP_RELEASE/setUp.sh
```
To load the FairShip environment for use within HTCondor, execute:
```bash
alienv load FairShip/latest-<version>-release > /afs/cern.ch/user/<path>/<to_your_folder>/HTCondor_scripts/config_<version>.sh
```
Alternatively, you can also use `eval` as described in [Fairship README](https://github.com/ShipSoft/FairShip?tab=readme-ov-file#build-instructions-using-cvmfs) (Step 5).

## 2. Modifying the Submission Scripts

### 2.1  Submission File (`submitscript.sub`)

#### Email Configuration
Change the `notify_user` field to your respective email address if you would like to be notified of the status. 
(Warning: Enabling this option will result in 8256 notification emails being sent!)

#### Modify Folder Paths:

Replace the Output folder path in **line 6** with your own EOS folder path (this is where the outputs will be saved):
```bash
arguments = /eos/user/<path>/<to_your_output_folder> $(inputFile) $(startEvent) $(nEvents) $(Process) $(ClusterId) 
```
and the Input folder path in **line 21**:
```bash
queue inputFile,startEvent,nEvents from /afs/cern.ch/user/<path>/<to_your_folder>/HTCondor_scripts/MuonBack/inputfile_list_1spill.txt
```

#### Ensure Error/Output/Log Folders Exist

Confirm that the necessary directories exist for HTCondor logs, outputs, and errors (and create them if otherwise).
```bash
error   = /afs/cern.ch/work/<path>/<to_your_Condor_folder>/error/muonBack_$(Process).err
log     = /afs/cern.ch/work/<path>/<to_your_Condor_folder>/log/muonBack_$(Process).log
output  = /afs/cern.ch/work/<path>/<to_your_Condor_folder>/muonBack_$(Process).out
```
It is advised to use the afs work space (`/afs/cern.ch/work/`) for these files since the [quota is much larger](https://resources.web.cern.ch/resources/Manage/ListServices.aspx).
### 2.2 Executable (`submitscript.sh`)

Change the \$SHiP_RELEASE version on **line 10** with the release you want to use):
```bash
source /cvmfs/ship.cern.ch/$SHIP_RELEASE/setUp.sh
```
Change the path to the `config_<version>.sh file on **line 11** with the one produced in [Step 1](https://github.com/anupama-reghunath/HTCondor_scripts/new/main/MuonBack#1-load-the-environment-for-use-within-htcondor):
```bash
source /afs/cern.ch/user/<path>/<to_your_folder>/HTCondor_scripts/config_<version>.sh
```
Replace all mentions of  `root://eospublic.cern.ch` with `root://eosuser.cern.ch` to save the files to your personal EOS space.

---



