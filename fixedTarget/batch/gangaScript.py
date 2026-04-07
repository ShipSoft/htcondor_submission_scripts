import time
import os
import random

SITE = 'CERN'  # or GENT or GRIDPP
# Set this path to wherever you want the output to go
config['Output']['MassStorageFile']['uploadOptions']['path'] = '/eos/experiment/ship/simulation/bkg/Mbias2026/CERN'
config['Output']['MassStorageFile']['uploadOptions']['defaultProtocol'] = 'root://eospublic.cern.ch//eos/experiment/ship/simulation/bkg/Mbias2026/CERN'
# Now set up the random seed, how many events per subjobs and how many events total
user = os.environ.get("USER")
random.seed(user + str(time.time()))
if SITE == 'CERN':  # either h or service account
    run_min = 0
    run_max = 300000000 - 1
elif SITE == 'GRIDPP':
    run_min = 300000000
    run_max = 600000000 - 1
else:
    run_min = 600000000
    run_max = 900000000

evtsPerJob =10000# 500000# 800000  # 200000
nJ = 1# 70  # in total want 14000 subjobs per week as a first try
nSJ = 1#400# 200  # fixed number of subjobs per job to register all subjobs on rucio at the same time
ecut = 30  # 5

totalEvts = evtsPerJob * nSJ

startRun = random.randint(run_min, run_max - nJ * nSJ)

for J in range(nJ):
    j = Job(name = f'run fixed target production number {J} - {nSJ * evtsPerJob} events')
    j.virtualization = Apptainer(image="/cvmfs/unpacked.cern.ch/registry.cern.ch/ship/gha-runner:latest/")
    j.virtualization.mounts = {'/cvmfs':'/cvmfs'}
    j.application = Executable(exe = File('wn_script.py'), args = ['--runfile', 'run_fixedTarget.py', '--cvmfs_version', '26.03', '--site', SITE, '--', '-o', './', '-n', evtsPerJob, '-e', str(ecut)])
    # IMPORTANT: Only put the run seed in the splitter arguments
    j.splitter = ArgSplitter(args = [['-r', startRun + J * nSJ + _i] for _i in range(nSJ)], append = True)
    j.outputfiles = [DiracFile('pythia8_evtgen_Geant4_*.root')]
    if SITE == 'GRIDPP':
        j.backend = Dirac()
        j.backend.settings['CPUTime'] = '40000'
    else:
        j.backend = Condor()
        j.backend.cdf_options['+MaxRuntime'] = '86000'

    # For running at CERN only
    if SITE == 'CERN':
        j.backend.env['EOS_MGM_URL'] = "root://eospublic.cern.ch"
        j.backend.cdf_options['accounting_group'] = 'group_u_SHIP.u_ship_cg'

    # Add in the postprocessor to do the file registration
    fc = FileChecker(files = ['stdout'], searchStrings = ['Macro finished successfully.'], failIfFound = False, checkMaster=False)
    j.postprocessors.append(fc)
    if SITE == 'CERN':
        cc = CustomChecker(module = 'postprocessor_master.py', checkSubjobs=False)
        j.postprocessors.append(cc)
    j.comment = f'%s events in each of %s subjobs, %.2f million total' % (evtsPerJob, nSJ, totalEvts/1.e6)
    j.submit()
