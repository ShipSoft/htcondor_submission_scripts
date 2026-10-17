# HTCondor submission scripts

Scripts for running common SHiP simulation workflows with FairShip on HTCondor
at CERN. General documentation on running FairShip on HTCondor is in the
[SHiP software documentation](https://shipsoft.github.io/Documentation/htcondor/).

## Workflows

| Directory | What it produces | CVMFS release | Status |
| --- | --- | --- | --- |
| [`fixedTarget/batch/`](fixedTarget/batch/README.md) | Fixed-target (minimum bias) production with ganga, EOS output and Rucio registration | 26.03 | Used for the 2026 production |
| [`MuonBack/`](MuonBack/README.md) | Muon background weighted to a spill | 24.10 | Unmaintained |
| [`MuonDIS/`](MuonDIS/README.md) | Muon DIS from existing muon background files | 24.10 | Unmaintained |
| [`NeutrinoDIS/`](NeutrinoDIS/) | Neutrino DIS from a GENIE sample | 24.10 | Unmaintained |
| [`SignalEventCalc/`](SignalEventCalc/README.md) | HNL signal samples from EventCalc | 24.10 | Unmaintained |

The four 24.10 workflows are unmaintained. They have not been tested with later
FairShip releases, and FairShip's command-line options have changed since then
(for example, on FairShip `main`, `run_simScript.py -g` now takes a geometry
file). They also contain paths to personal AFS and EOS areas that you need to
replace with your own.

The scripts directly under `fixedTarget/` are an older version of
`fixedTarget/batch/` that points to a personal FairShip installation. Use
`fixedTarget/batch/` instead.
