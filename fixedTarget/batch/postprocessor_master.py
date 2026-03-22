from GangaCore.GPIDev.Lib.File.MassStorageFile import MassStorageFile
import rucio_it_tools.rucio_it_register
import os

def args_list_to_dict(args_list):
    result = {}
    i = 0
    while i < len(args_list):
        key = args_list[i].lstrip("-")
        # Check if next item exists and is not another flag
        if i + 1 < len(args_list) and not args_list[i + 1].startswith("-"):
            result[key] = args_list[i + 1]
            i += 2
        else:
            # Flag without value → set to True
            result[key] = True
            i += 1
    return result

# This is a config file set up for SHiP
if 'RUCIO_CONFIG' not in os.environ:
    os.environ['RUCIO_CONFIG'] = '/cvmfs/ganga.cern.ch/Ganga/install/ship/rucio/etc/rucio.cfg'

def check(j):
    # Only do this on the master job
    if j.master:
        return True
    file_list = []
    j_arg_dict = args_list_to_dict(sj.application.args)
    for _sj in j.subjobs:
        if not _sj.status in ['completed', 'completing']:
            print(f"WARNING: Subjobs {_sj.id} did not complete")
            continue
        sj_arg_dict = args_list_to_dict(sj.application.args)
        for _f in _sj.outputfiles:
            if isinstance(_f, MassStorageFile):
                _loc = _f.locations[0]
                # Check you can open it
#               try:
#                    _tfile = uproot.open(_loc)
#                    _tfile.values()
#                    _tfile.close()
#                except uproot.deserialization.DeserializationError:
#                    print(f"ERROR: Unable to open {_loc} from job {_sj.fqid}! Job likely failed!")
#                    _tfile.close()
#                    _sj.force_status('failed')
                _size = rucio_it_tools.rucio_it_register.get_file_on_disk_size_in_bytes(_loc)
                _checksum = rucio_it_tools.rucio_it_register.get_file_on_disk_adler32_checksum(_loc)
#                print(_loc,' - ', _size, ' - ', _checksum)
                file_list.append({
                    "path": _loc,
                    "size": _size,
                    "adler32": _checksum
                })
    metadata = {
                "runfile": j_arg_dict['runfile'],
                "production_type": "target production",
                "job_args" : str([_a for _a in j.application.args]),
                "creator": os.environ.get("USER"),
                "ganga_id": str(j.id),
                "FairShip_tag": "26.03",  # mainly useful if using local version of FairShip
                "cvmfs_version": j_arg_dict['cvmfs_version'],
                "comment": j.comment,
                "data_type": "simulation",
                "production_site": j_arg_dict['site'],
                "run_nos" : str([(_sj.id, _sj.application.args[-1]) for _sj in j.subjobs if _sj.status=='completed']),
                "title" : j.name,
               }
#    print(f"INFO: File list - {file_list}")
#    print(f"INFO: metadata - {metadata}")

    if len(file_list)>0:
        try:
            rucio_it_tools.rucio_it_register.register_files_with_structure(
                rse_name = "SHIP_TIER_0_DISK",
                files = file_list,
                metadata = metadata,
    #            dry_run = True
            )
        except Exception as e:
            print(f"ERROR: Not able to register file {file_list} with rucio: {e}")
            j.force_status("failed")
            j.comment += " - Rucio registration failed"
            return False
    return True
