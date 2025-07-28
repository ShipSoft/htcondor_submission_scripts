import time
import os
import random
random.seed(os.environ.get("USER"))
startRun = int(time.time()) + random.randint(0,10000)
evtsPerJob = 10 #100000
evtsToGen = 100
nSJ = int(evtsToGen/evtsPerJob)


j = Job(name = f'run fixed target production - {evtsToGen} events')
j.application = Executable(exe = File('bashScript.sh'), args = ['-o', '"./"', '-n', evtsPerJob])
j.splitter = ArgSplitter(args = [['-r', startRun + _i] for _i in range(nSJ)], append = True)
j.outputfiles = [LocalFile('*.root')]
j.backend = Condor()
j.backend.cdf_options['+MaxRuntime'] = '1000'
j.comment = f'{evtsPerJob} events in each of {nSJ} subjobs'
j.submit()
