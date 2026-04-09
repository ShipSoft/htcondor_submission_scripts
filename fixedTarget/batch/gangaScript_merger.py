jNo = 61

j = Job(name = f"Merge output of production job {jNo}")
j.virtualization = Apptainer(image="/cvmfs/unpacked.cern.ch/registry.cern.ch/ship/gha-runner:latest/")
j.virtualization.mounts = {'/cvmfs':'/cvmfs', '/home/hep/mesmith':'/home/hep/mesmith' }
j.application = Executable(exe = File('wn_script.py'))
j.inputfiles = [LocalFile("merger.py")]
myargs = ['merger.py' if _a=='run_fixedTarget.py' else _a for _a in jobs(jNo).application.args]
myargs.extend(['-j', jNo, '--prodSite', 'GRIDPP'])
myargs.append('-i')
inputfiles = jobs(jNo).backend.getOutputDataAccessURLs(protocol='"root"')
myargs.extend(inputfiles)
j.application.args = myargs
j.outputfiles = [LocalFile('pythia_*.root')]

j.backend = Condor()
j.backend.cdf_options["+MaxRuntime"] = '3000'

j.submit()
