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

