import rucio_it_tools.rucio_it_register
import os

if 'RUCIO_CONFIG' not in os.environ:
    os.environ['RUCIO_CONFIG'] = '/afs/cern.ch/user/m/masmith/rucio_test/etc/rucio.cfg'

def check(j):
    # Only do this on the master job
    if j.master:
        continue
    file_list = []
    for _sj in j.subjobs:
        if not _sj.status == 'completed':
            print(f"WARNING: Subjobs {_sj.id} did not complete")
            continue
        for _f in j.outputfiles:
            if '/eos/' in _f.location():
                _loc = _f.location()
                _size = rucio_it_tools.rucio_it_register.get_file_on_disk_size_in_bytes(_f)
                _checksum = rucio_it_tools.rucio_it_register.get_file_on_disk_adler32_checksum(_f)
                file_list.append({
                    "path": _loc,
                    "size": _size,
                    "adler32": _checksum
                })
    metadata = {
                "name" : j.name,
                "ganga_id": str(j.id),
                "completion_time" : str(j.time.final()),
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
