
# Condor Scripts to generate MuonDIS simulations using Fairship

These scripts have been used to produce the MuonDIS simulation available within `/eos/experiment/ship/simulation/bkg/MuonDIS_2024helium/8070735`. 

> **Note:**  
> To generate MuonDIS, MuonBackground files must already be generated.  
> You can either use one of the clusters in `/eos/experiment/ship/simulation/bkg/MuonBack_2024helium/` (produced with default master release) or generate your own MuonBack using the [MuonBack scripts](https://github.com/anupama-reghunath/HTCondor_scripts/tree/main/MuonBack).

To reuse the MuonDIS scripts, follow the step by step guide:

## 1. Load the Environment for use within HTCondor

- Source the setup script (replace \$SHIP_RELEASE with the release you want to use):
  ```bash
  source /cvmfs/ship.cern.ch/$SHIP_RELEASE/setUp.sh
  ```
- To load the FairShip environment for use within HTCondor, execute:
  ```bash
  alienv load FairShip/latest-<version>-release > /afs/cern.ch/user/<path>/<to_your_folder>/HTCondor_scripts/config_<version>.sh
  ```
---
## 2. Modifying the Submission Scripts

### Step 0: Collecting muons hitting the SBT / Tracking Station 1 

#### 2.0.0 Submission File (`condor.sub`)

- Change the `notify_user` field to your respective email address if you would like to be notified of the status.
  (Warning: Enabling this option may result in an email spam!)

- Confirm that the necessary directories exist for HTCondor logs, outputs, and errors (and create them if otherwise).
  ```bash
  error   = /afs/cern.ch/work/<path>/<to_your_Condor_folder>/error/makentuple.err
  log     = /afs/cern.ch/work/<path>/<to_your_Condor_folder>/log/makentuple.log
  output  = /afs/cern.ch/work/<path>/<to_your_Condor_folder>/makentuple.out
  ```
  It is advised to use the afs work space (`/afs/cern.ch/work/`) for these files since the [quota is much larger](https://resources.web.cern.ch/resources/Manage/ListServices.aspx).
#### 2.0.1 Executable (`condor.sh`)

- Change the \$SHiP_RELEASE version on **line 10** with the release you want to use):
  ```bash
  source /cvmfs/ship.cern.ch/$SHIP_RELEASE/setUp.sh
  ```
- Change the path to the `config_<version>.sh` file on **line 6** with the one produced in [Step 1](to be added):
  ```bash
  source /afs/cern.ch/user/<path>/<to_your_folder>/HTCondor_scripts/config_<version>.sh
  ```
- Add the path to muon background files. (default is "/eos/experiment/ship/simulation/bkg/MuonBack_2024helium/8070735 )
  ```bash
  python $FAIRSHIP/muonDIS/make_nTuple_SBT.py --path <path to muon background files> &
  python $FAIRSHIP/muonDIS/make_nTuple_Tr.py --path <path to muon background files>
  ```
- Change the paths to where the output is to be stored:
  ```bash
  xrdcp muonsProduction_wsoft_SBT.root /eos/<path>/<to_your_output_folder>/muonsProduction_wsoft_SBT.root
  xrdcp SelectedMuonsSBT.txt /eos/<path>/<to_your_output_folder>/SelectedMuonsSBT.txt
  
  xrdcp muonsProduction_wsoft_Tr.root /eos/<path>/<to_your_output_folder>/muonsProduction_wsoft_Tr.root
  xrdcp SelectedMuonsTr.txt /eos/<path>/<to_your_output_folder>/SelectedMuonsTr.txt
  ```
`muonsProduction_wsoft_SBT.root`, `SelectedMuonsSBT.txt` contains the information about the muons which hit the SBT.
`muonsProduction_wsoft_Tr.root`, `SelectedMuonsTr.txt` contains the information about the muons which hit the Tracking Station (and no hit in the SBT).

Once these files are produced, proceed further.

### Step 1: Producing DIS simulations for the muons hitting the SBT/Tr

There are two submission_scripts (for the SBT case and the Tr Case), both using the same executable.

#### 2.1.0 Executable (`submitscript.sh`)

- Change the \$SHiP_RELEASE version on **line 10** with the release you want to use):
  ```bash
  source /cvmfs/ship.cern.ch/$SHIP_RELEASE/setUp.sh
  ```
- Change the path to the `config_<version>.sh file on **line 6** with the one produced in [Step 1](to be added):
  ```bash
  source /afs/cern.ch/user/<path>/<to_your_folder>/HTCondor_scripts/config_<version>.sh
  ```
- Replace all mentions of  `root://eospublic.cern.ch` with `root://eosuser.cern.ch` to save the files to your personal EOS space.

#### 2.1.1 Submit Files (`submitscript.sub`)

- Ensure error/output/log folders exist and the notify_user is updated like in  [Step 2.0.1](https://github.com/anupama-reghunath/HTCondor_scripts/new/main/MuonDIS#201-submission-file-condorsub)

- Change the arguments in **line 6** with your own EOS folder path (this is where the outputs will be saved). 
  Make sure to create a subFolder "SBT"(or Tr) folders to save the simulations separately.

  ```bash
  arguments = /eos/user/<path>/<to_your_output_folder>/SBT <path>/<to_your_output_folder>/muonsProduction_wsoft_<type>.root $(Process) <number of muons per job> <number of DIS per muon> 
  ```
  for eg., in submitscript_SBT.sub, number of muons per job = 10 and number of DIS per muon = 100.
- Adjust number of jobs to execute with ```queue njobs```, such that njobs*number of muons per job >= number of muons in muonsProduction_wsoft_<type>.root

---
## 3. Submitting to HTCondor
To submit the jobs to HTCondor, run
```bash
condor_submit submitscript_<type>.sub
```
To monitor the job queue, use `condor_q`. 

For more useful commands and adavnced usage, please refer to the [official HTCondor documentation](https://htcondor.readthedocs.io/en/latest/)

