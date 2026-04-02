# -----------------------------------------------------
# Put the functions defined here into your ~/.ganga.py
# and it will be available in the Ganga namespace.
# Then you can just do mergeOutput(jobNo) and it will
# submit the job.
# -----------------------------------------------------

def args_list_to_dict(args_list):
    result = {}
    i = 0
    while i < len(args_list):
        key = str(args_list[i]).lstrip("-")
        # Check if next item exists and is not another flag
        if i + 1 < len(args_list) and isinstance(args_list[i + 1], str) and not args_list[i + 1].startswith("-"):
            result[key] = args_list[i + 1]
            i += 2
        else:
            # Flag without value → set to True
            result[key] = True
            i += 1
    return result

def mergeOutput(jNo):

    script_path = "/path/to/scripts/" # set this to wherever you checked out the scripts package

    j = Job(name = f"Merge output of production job {jNo}")
    j.virtualization = Apptainer(image="/cvmfs/unpacked.cern.ch/registry.cern.ch/ship/gha-runner:latest/")
    j.virtualization.mounts = {'/cvmfs':'/cvmfs'}
    j.application = Executable(exe = File(script_path + 'wn_script.py'))
    j.inputfiles = [LocalFile(script_path + "merger.py")]

    # Copy over the args but change the run file from run_fixedTarget.py to merger
    j_arg_dict = args_list_to_dict(j.application.args)
    this_site = j_arg_dict["site"]
    myargs = ['merger.py' if _a=='run_fixedTarget.py' else _a for _a in jobs(jNo).application.args]
    myargs.extend(['-j', jNo, '--prodSite', this_site, '--useLocalFile'])
    myargs.append('-i')

    # Now grab the files
    if this_site == "GRIDPP": # Do something different for GRIDPP where the files are on Dirac
        inputfiles = jobs(jNo).backend.getOutputDataAccessURLs(protocol='"root"')
    else:
        inputfiles = []
        for sj in jobs(jNo).subjobs.select(status="completed"):
            for _f in sj.outputfiles:
                if isinstance(_f, MassStorageFile)
                    inputfiles.append(_f.locations[0])
    myargs.extend(inputfiles)
    j.application.args = myargs

    j.outputfiles = [LocalFile('pythia_*.root')]
    j.backend = Condor()
    j.backend.cdf_options["+MaxRuntime"] = '3000' # Set this to something reasonable
    j.submit()
