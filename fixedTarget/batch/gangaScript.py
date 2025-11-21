import time
import os
import random

# Set this path to wherever you want the output to go
config['Output']['MassStorageFile']['uploadOptions']['path'] = '/eos/experiment/ship/test'

# Now set up the random seed, how many events per subjobs and how many events total
random.seed(os.environ.get("USER"))
startRun = int(time.time()) + random.randint(0,10000)
evtsPerJob = 10 #100000
evtsToGen = 10
nSJ = int(evtsToGen/evtsPerJob)

j = Job(name = f'run fixed target production - {evtsToGen} events')
j.application = Executable(exe = File('bashScript.sh'), args = ['-o', '"./"', '-n', evtsPerJob])

# IMPORTANT: Only put the run seed in the splitter arguments
j.splitter = ArgSplitter(args = [['-r', startRun + _i] for _i in range(nSJ)], append = True)
j.outputfiles = [MassStorageFile('pythia8_evtgen_Geant4_*.root')]
j.backend = Condor()
#j.backend.cdf_options['+MaxRuntime'] = '2000'
j.backend.cdf_options['+JobFlavour'] = '"longlunch"'

# For running at CERN only
j.backend.cdf_options['accounting_group'] = 'group_u_SHIP.u_ship_cg'

# Add in the postprocessor to do the file registration
cc = CustomChecker(module = 'postprocessor.py')
j.postprocessors.append(cc)
j.comment = f'{evtsPerJob} events in each of {nSJ} subjobs'
j.submit()
