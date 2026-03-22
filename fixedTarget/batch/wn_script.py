#!/usr/bin/env python3
import argparse
import subprocess
import shlex

def main():
    parser = argparse.ArgumentParser(
        description="Run FairShip fixed target simulation with environment setup"
    )

    # Main configurable inputs
    parser.add_argument(
        "--fs-install",
        help="Base FairShip installation path"
    )

    parser.add_argument(
        "--cvmfs_version",
        default='26.03',
        help="Which CVMFS version of FairShip to use (default: 26.03)"
    )

    parser.add_argument(
        "--site",
        default="CERN",
        help="Which site are we running - for setting site-specific options"
    )

    parser.add_argument(
        "--work-dir",
        help="WORK_DIR (default: <fs-install>/sw/)"
    )

    parser.add_argument(
        "--init-script",
        help="Path to init.sh (default derived from fs-install)"
    )

    parser.add_argument(
        "--runfile",
        help="Which python file to run (taken from the install dir location)",
        default = "run_fixedTarget.py"
    )

    # Everything after this is passed through to the FairShip script
    parser.add_argument(
        "script_args",
        nargs=argparse.REMAINDER,
        help="Arguments passed to runfile"
    )

    args = parser.parse_args()

    # Derive defaults if not provided
    FS_INSTALL = args.fs_install or '/cvmfs/ship.cern.ch/' + args.cvmfs_version
    WORK_DIR = args.work_dir or f"{FS_INSTALL}/sw/"
    INIT_SCRIPT = args.init_script or f"{FS_INSTALL}/sw/slc9_x86-64/FairShip/latest/etc/profile.d/init.sh"
    RUN_SCRIPT = f"{FS_INSTALL}/sw/slc9_x86-64/FairShip/latest/macro/{args.runfile}"

    print(f"INFO: Running at the site {args.site}")
    print(f"INFO: Environment set up for FairShip located at {FS_INSTALL}")


    # Safely quote passthrough args
    script_args = args.script_args[1:] if args.script_args[:1] == ["--"] else args.script_args
    passthrough = " ".join(shlex.quote(a) for a in script_args)

    print(f"INFO: Executing: python {RUN_SCRIPT} {passthrough}")

    # Build bash command
    command = f"""
    export WORK_DIR="{WORK_DIR}"
    source "{INIT_SCRIPT}"
    python "{RUN_SCRIPT}" {passthrough}
    """

    subprocess.run(["bash", "-c", command], check=True)

    print("INFO: Finished running. These files are on the WN:")

    subprocess.run(["ls", "-lh"])


if __name__ == "__main__":
    main()
