# get confermation
printf "Reset the database? If so enter DB password\t"

# create the file reset.sql and add the wipe commands to file
printf "# DROP ALL TABLES\n" > reset.sql
cat dropAll.sql >> reset.sql

# add table defs to file
printf "\n\n# CREATE TABLES\n" >> reset.sql	
cat tableDef.sql >> reset.sql

# add the inserts to the file
printf "\n\n# POPULATE TABLES\n" >> reset.sql
cat tableInsert.sql >> reset.sql

# actually run the file on the database wipeing and rebuilding it
/Applications/MAMP/Library/bin/mysql -u root -p Dispatch < reset.sql

# delete the file
rm reset.sql