# Tachiyomi-Backup-Reader
This project is a small script that reads the backup files Tachiyomi makes and can compare it to an error log from restoring a backup.
I created this project because I was restoring a backup and had over 150 titles that were not correctly loaded. So I created this program to run through the results file and tell you what titles had an issue. It cuts out specific errors and only tells yo uthe title's name. Also if you load one of your backups into backup.json it will read the backup and attempt to figure out how many chapters of each failed title were read. It is very simple right now, once it runs it puts all the results in a failed_results.txt and closes. Eventually my goal is to have it prompt you what reports to generate, but right now it only makes one.
