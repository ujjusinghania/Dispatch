printf "Reset the database? If so enter DB password\t"
printf "# DROP ALL TABLES\n" > reset.sql
cat dropAll.sql >> reset.sql
printf "\n\n# CREATE TABLES\n" >> reset.sql	
cat tableDef.sql >> reset.sql
printf "\n\n# POPULATE TABLES\n" >> reset.sql
cat tableInsert.sql >> reset.sql


/Applications/MAMP/Library/bin/mysql -u root -p Dispatch < reset.sql

rm reset.sql