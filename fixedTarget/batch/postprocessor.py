from GangaCore.GPIDev.Lib.File.MassStorageFile import MassStorageFile
import rucio_it_tools.rucio_it_register
import os

# This is a config file set up for SHiP
if 'RUCIO_CONFIG' not in os.environ:
    os.environ['RUCIO_CONFIG'] = '/cvmfs/ganga.cern.ch/Ganga/install/ship/rucio/etc/rucio.cfg'

def check(j):
    # Only do this on the master job
    if j.master:
        print("ALL gone wrong")
        return True
    file_list = []
    for _sj in j.subjobs:
        if not _sj.status == 'completed':
            print(f"WARNING: Subjobs {_sj.id} did not complete")
            continue
        for _f in _sj.outputfiles:
#            print('a: ', _f.locations)
            if isinstance(_f, MassStorageFile):
                print('b')
                _loc = _f.locations[0]
                _size = rucio_it_tools.rucio_it_register.get_file_on_disk_size_in_bytes(_loc)
                _checksum = rucio_it_tools.rucio_it_register.get_file_on_disk_adler32_checksum(_loc)
#                print(_loc,' - ', _size, ' - ', _checksum)
                file_list.append({
                    "path": _loc,
                    "size": _size,
                    "adler32": _checksum
                })
    metadata = {
                "name" : j.name,
                "ganga_id": str(j.id),
                "completion_time" : str(j.time.backend_final()),
                "job_args" : str([_a for _a in j.application.args]),
                "run_nos" : str([(_sj.id, _sj.application.args[-1]) for _sj in j.subjobs if _sj.status=='completed']),
                "n_jobs" : str(len(j.subjobs)),
                "creator": os.environ.get("USER"),
                "comment": j.comment
               }
    print(f"INFO: File list - {file_list}")
    print(f"INFO: metadata - {metadata}")

    if len(file_list)>0:
        rucio_it_tools.rucio_it_register.register_files_with_structure(
            rse_name = "SHIP_TIER_0_DISK",
            files = file_list,
            metadata = metadata,
            dry_run = True
        )
    return True
