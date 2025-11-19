import time
import os
import random

# Set this path to wherever you want the output to go
config['Output']['MassStorageFile']['uploadOptions']['path'] = '/eos/lhcb/user/m/masmith/mySHiPTest'

random.seed(os.environ.get("USER"))
startRun = int(time.time()) + random.randint(0,10000)
evtsPerJob = 10 #100000
evtsToGen = 100
nSJ = int(evtsToGen/evtsPerJob)

j = Job(name = f'run fixed target production - {evtsToGen} events')
j.application = Executable(exe = File('bashScript.sh'), args = ['-o', '"./"', '-n', evtsPerJob])
# IMPORTANT: Only put the run seed in the splitter arguments
j.splitter = ArgSplitter(args = [['-r', startRun + _i] for _i in range(nSJ)], append = True)
j.outputfiles = [MassStorageFile('*.root')]
j.backend = Condor()
j.backend.cdf_options['+MaxRuntime'] = '1000'
cc = CustomChecker(moduel = 'postprocessor.py')
j.postprocessors.append(cc)
j.comment = f'{evtsPerJob} events in each of {nSJ} subjobs'
j.submit()
