import os
import shutil
import glob
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--path2rm", 
                    default='/Users/emdann/rmirro/remarkable/Papers/',
                    help='Local path to destination folder on ReMarkable (synced via rmirro).')
parser.add_argument("--path2pp", 
                    default='/Users/emdann/Google Drive/My Drive/Paperpile/All Papers/',
                    help='Local path to destination folder on Paperpile GDrive (synced via GDrive for desktop).')
parser.add_argument("--force_upload", 
                    action='store_true', 
                    help='Force upload to reMarkable.')
parser.add_argument("--force_download", 
                    action='store_true', 
                    help='Force download from reMarkable.')
args = parser.parse_args()

def find_file_glob(root_dir, filename):
    pattern = os.path.join(root_dir, '**', filename)
    files = glob.glob(pattern, recursive=True)
    return files

def format_timestamp(t):
    mod_time_readable = datetime.datetime.fromtimestamp(t)
    return mod_time_readable.strftime('%Y-%m-%d %H:%M:%S')

def get_paperpile_like_files(rm_directory):
    '''Get files resembling Paperpile pdfs and their last edit date.'''
    pp_like_files = [x for x in os.listdir(REMARKABLE_DIR) if ' et al. ' in x]
    pp_files_timestamps = {}
    for f in pp_like_files:
        pp_files_timestamps[f] = os.path.getmtime(os.path.join(REMARKABLE_DIR, f))
    return(pp_files_timestamps)

def sync_file_2_gdrive(f, t, gdrive_directory, rm_directory, force_sync=False):
    '''Sync paper pdf file from remarkable directory to gdrive paperpile directory.'''
    gdrive_match = find_file_glob(gdrive_directory, f)
    if len(gdrive_match) > 0:
        for g_f in gdrive_match:
            # Find original PDF, not links in other folder
            if not os.path.islink(g_f):
                gdrive_f = g_f
        if not force_sync:
            gdrive_f_timestamp = os.path.getmtime(gdrive_f)
            # print(f, format_timestamp(t),' -  gdrive timestamp: ', format_timestamp(gdrive_f_timestamp))
            if gdrive_f_timestamp < t:
                print(f"Syncing {f} to {gdrive_directory}")
                shutil.copy(os.path.join(rm_directory, f), gdrive_f)
        else:
            print(f"Syncing {f} to {gdrive_directory}")
            shutil.copy(os.path.join(rm_directory, f), gdrive_f)

def sync_file_2_rm(f, gdrive_directory, rm_directory, force_sync=False):
    rm_match = find_file_glob(rm_directory, f)
    if not force_sync:
        if len(rm_match) == 0:
            print(f"Syncing {f} to {rm_directory}")
            shutil.copy(os.path.join(gdrive_directory, f), rm_directory)
        else:
            print(f"{f} already uploaded to {rm_directory}")
    else:
        print(f"Syncing {f} to {rm_directory}")
        shutil.copy(os.path.join(gdrive_directory, f), rm_directory)

REMARKABLE_DIR = args.path2rm
GDRIVE_PAPERPILE = args.path2pp

print('#####################################')
print('#### Remarkable 2 Paperpile sync ####')
print('#####################################')
print('')

### --- Download read papers --- ###
print('Downloading read papers...')
pp_files_rm = get_paperpile_like_files(REMARKABLE_DIR)
for f,t in pp_files_rm.items():
    sync_file_2_gdrive(f,t, GDRIVE_PAPERPILE, REMARKABLE_DIR, force_sync=args.force_download)

### --- Upload papers 2 read --- ###
print('Uploading papers 2 read...')
SYNC_DIR = f'{GDRIVE_PAPERPILE}/to_remarkable/'
SYNC_RM_DIR = f'{REMARKABLE_DIR}/To read/'
files2sync = os.listdir(SYNC_DIR)
# remove files uploaded to ReMarkable in last sync 
# (supposedly annotated papers have already been moved to REMARKABLE_DIR)
files_in_rm = os.listdir(SYNC_RM_DIR)
old_files = list(set(files_in_rm) - set(files2sync))
for f in old_files:
    os.remove(f'{SYNC_RM_DIR}{f}')

if len(files2sync) == 0:
    print('Nothing to sync from Paperpile/to_remarkable')
for f in files2sync:
    sync_file_2_rm(f, SYNC_DIR, SYNC_RM_DIR, force_sync=args.force_upload)


        

