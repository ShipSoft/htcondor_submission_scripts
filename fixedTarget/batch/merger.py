#!/usr/bin/env python
import os
import argparse
import ROOT
import uproot
import json
from datetime import datetime

def mergeFiles(myfiles, tmpFile):
    myChain = ROOT.TChain("cbmsim")
    for _f in myfiles:
        myChain.Add(_f)
    myChain.Merge(tmpFile)


parser = argparse.ArgumentParser(
    description="Run FairShip file merger"
)

parser.add_argument("-i", "--inFiles", nargs="*",
                    help="input files to merge")

parser.add_argument("-n", "--genEvents",
                    default=500000,
                    type=int,
                    help="How many events were generated to make this file"
                    )

parser.add_argument("-e", "--eCut",
                    default=30,
                    type=float,
                    help="What was the energy cut to produce the file"
                    )

parser.add_argument("-j", "--gangaJob",
                    type=int,
                    help="Which ganga job produced these files",
                    )
parser.add_argument("-s", "--site",
                    default="CERN",
                    help="Which site was this run at"
                    )

parser.add_argument("-o", "--outputPath",
                    help="A placeholder")

parser.add_argument("--prodSite",
                    default="CERN",
                    help="Which site was this run at"
                    )

args = parser.parse_args()


if args.prodSite == "GRIDPP":
    os.environ["X509_USER_PROXY"]="/home/hep/mesmith/private/my_proxy.pem"
    os.environ["X509_VOMSES"]="/cvmfs/grid.cern.ch/etc/grid-security/vomses"
    os.environ["X509_VOMS_DIR"]="/cvmfs/grid.cern.ch/etc/grid-security/vomsdir"
    os.environ["X509_CERT_DIR"]="/cvmfs/grid.cern.ch/etc/grid-security/certificates"

files_to_merge = args.inFiles
if not len(files_to_merge)>0:
    print("ERROR: no files to merge! Doing nothing")
    sys.exit()
print("INFO: Merging %s files from job %s" % (len(files_to_merge), args.gangaJob))

total_pot = len(files_to_merge) * args.genEvents
outName = f"pythia8_Geant4_eCut_{args.eCut}_PoT_{total_pot}_{args.site}_j{args.gangaJob}.root"

mergeFiles(files_to_merge, outName)

fsr = {
    "PoT" : total_pot,
    "EnergyCut": args.eCut,
    "PoTperFile": args.genEvents,
    "nFilesMerged": len(files_to_merge),
    "filesMerged": args.inFiles,
    "prodSite": args.prodSite,
    "mergeDate": datetime.today().strftime('%Y-%m-%d')
}

print("INFO: Adding the file summary")
with uproot.update(outName) as _f:
    _f["FileSummary"] = json.dumps(fsr)

print("INFO: All done")
