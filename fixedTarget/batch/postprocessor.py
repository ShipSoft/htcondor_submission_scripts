import rucio_it_tools.rucio_it_register
import os
def check(j):
    file_list = []
    for _f in j.outputfiles:
        if isinstance(_f, MassStorageFile):
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
                "n_jobs" : str(len(j.subjobs)),
                "creator": os.environ.get("USER"),
                "comment": j.comment
               }
    
    
    rucio_it_tools.rucio_it_register.register_files_with_structure(
        rse_name = "SHIP_TIER_0_DISK",
        files = file_list
        metadata = metadata
    )
    return True
