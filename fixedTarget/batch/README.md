# Production submission

1. Make sure the FairShip installation in `bashScript.sh` points to the version you want

2. Make sure the MassStorageFile location in `gangaScript.py` points to wherever you want the data to go

3. Make sure you have created a voms proxy for the file registration

4. Use the gangaSubmit.sh script to submit the job. This is important - you need to use the ship version of ganga on CVMFS (not latest)



# Batch submission

1. Download the FairShip software:
    ```bash
    git clone https://github.com/ShipSoft/FairShip.git
    git clone https://github.com/ShipSoft/htcondor_submission_scripts.git
    ```
2. Modify FS_INSTALL variable to point to your installation in the relevant htcondor_submission_scripts scripts
3. Build the code:
   ```bash
   cd htcondor_submission_scripts/fixedTarget/batch
   ./build.sh
   ```
4. Submit jobs (in clean environment):
   ```
   ./gangaSubmit.sh
   ```

