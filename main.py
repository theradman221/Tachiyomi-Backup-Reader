import re
import json as js
import os
cur_dir = os.getcwd()+ "/"

# These are all values that are used throughout the program, if tachiyomi ever changes how things are handled these may need updated
backup_dict_key_mangas = "mangas" # This is the name that the json uses in the backups for all mangas, this is a dictionary
manga_info_key = "manga" # This is the name that the json uses within each manga dictionary to record each manga, this is a list
chapter_key = "chapters" # This is the name of the key within each manga for the chapter dictionaries
backup_location = "backup.json" # Only change this if you're not using the default backup.json as your backup location
failed_migrations_locations = "restore.txt" # Only change this if you're not using the default location for the failed migrations, this should be a json output from tachiyomi's errors generated during a backup load.
failed_results_name = "failed_results.txt" # This is the name of the file that is produced when you analyze the failed results.

# This program reads restore.txt and tells the user all of the manga names that were not migrated correctly.
# If a backup file is provided it will try and look up the chapter you were on and report that along with the ones that didn't migrate correctly.
try:
    backup = js.load(open(cur_dir + backup_location, "r"))
except:
    backup = None
failed = open(cur_dir + failed_migrations_locations, "r")

def main():
    # Load the backups and fails
    backups = load_backups()
    if backups != None:
        backup_keys = backups.keys()
    else:
        backup_keys = None
    failed = get_failed()
    # Create the report
    results = generate_failed_report(backups, backup_keys, failed)
    print(results)
    results_file = open(failed_results_name, "w")
    results_file.write(results)
    results_file.close()
    
def generate_failed_report(backups, backup_keys, fails):
    report = "Manga that were skipped during migration/backup loading.\n"
    report += "If a manga has a ~ in the name this seems to mean it is an alternate name.\n"
    if backups == None or backup_keys == None:
        use_backup_stats = False
        report += "No valid backup detected, no chapter information will be avaliable.\n"
    else:
        use_backup_stats = True
        report += "Valid backup detected, for all manga present in the backup an approximation of the amount of chapters read will be provided.\nPlease note that this is an approximation and may not be 100% accurate.\n" 
    # Iterate through each manga and add it to the report with or without the backup data
    for manga in fails:
        if use_backup_stats and manga in backup_keys:
            #print(manga, "is in the backup dictionary!")
            report += "Manga Name: " + manga + "\n"
            report += "Chapters Read: " + str(backups[manga]) + "\n\n"
        elif not use_backup_stats:
            #print(manga, "is not in the backup dictionary!")
            report += "Manga Name: " + manga + "\n\n"
        else:
            report += "Manga Name: " + manga + "\n"
            report += "Chapters Read: Not contained in backup. \n\n"
    return report

    
def load_backups():
    if backup != None:
        backup_mangas = {}
        manga_info = backup[backup_dict_key_mangas]
        counter = 0
        for manga in manga_info:
            manga_info = manga[manga_info_key]
            try:
                chapters = manga[chapter_key]
            except Exception:
                chapters = None
        
            chapter_counter = 0
            if chapters is not None:
                for chapter in chapters:
                    # This counts up how many chapter's you've at least started reading, is not smart at all about where you actually are.
                    chapter_counter += 1
                backup_mangas[manga_info[1]] = chapter_counter
            else:
                backup_mangas[manga_info[1]] = 0
        return backup_mangas
    else:
        return None


def get_failed():
    failed_migrations = {}
    for line in failed:
        # This check prevents empty lines from causing issues
        if len(line) > 2:
            # This splits out the date time information
            line = re.split("^.*\] {1}", line)
            line = line[1] # This will always be line[1] as it should only split once
            # This splits out any other additional details or source information
            line = re.split(" \[|-", line)
    
            chunks = len(line)
            # If it split on a - we need to add those back in for the name to be right
            if chunks > 2:
                newLine = ""
                count = 0
                while chunks > 1:
                    # Detect the first instance and don't add in the seperator
                    if count == 0:
                        newLine = line[count]
                    else:
                        newLine += "-" + line[count]
                    count += 1
                    chunks -= 1
            else:
                newLine = line[0]
            # This rstrip is important, some manga that were being missed are picked up with this.
            newLine = newLine.rstrip()
            failed_migrations[newLine] = newLine
    return failed_migrations

if __name__ == '__main__':
    main()