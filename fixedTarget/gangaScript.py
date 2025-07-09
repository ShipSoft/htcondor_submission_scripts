j = Job()
j.application = Executable(exe = File('bashScript.sh'))
j.outputfiles = [LocalFile('*.root')]
j.backend = Condor()
j.backend.cdf_options['+MaxRuntime'] = '1000'
j.submit()
