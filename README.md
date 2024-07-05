# Sync Paperpile to ReMarkable via Google Drive

Script to sync via GDrive to read and annotate in ReMarkable papers on Paperpile.

## Requirements

1. [Google Drive for desktop](https://support.google.com/drive/answer/10838124?sjid=5971543940215022341-EU)
2. Sync of ReMarkable to laptop with [rmirro](https://github.com/hersle/rmirro/tree/main)
3. [Sync of Paperpile to Google Drive](https://paperpile.com/h/guide-google-drive/#:~:text=Google%20Drive%20syncing%20is%20initially,no%20manual%20action%20is%20required.)

## Workflow 

### Download papers to read

Make a sync folder in Paperpile (I have a "to_remarkable" folder)

Make a "Papers" folder in ReMarkable 

Run `paperpile_sync.py` to upload papers from Paperpile to "To read" folder on ReMarkable
```
python3 paperpile_sync.py
``` 
Sync remarkable with laptop
```
python3 rmirro.py
``` 

### Upload read papers

Read and annotate the papers

Move papers outside of "To read" folder

Sync remarkable with laptop
```
python3 rmirro.py
``` 

Run `paperpile_sync.py` to sync annotated papers to Paperpile.

Find annotated papers in Paperpile app
