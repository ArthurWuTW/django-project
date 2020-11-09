import os
import sys
from datetime import datetime, timedelta

sys.path.append("..")
from secure_data.secure_data_loader import SecureDataLoader
secure_data_loader = SecureDataLoader()

if __name__ == '__main__':

    # Run dumping data script & Save .sql in backup directory
    command = 'pg_dump "host='+secure_data_loader.secure_data['POSTGRES_HOST']+' \
    port='+secure_data_loader.secure_data['POSTGRES_PORT']+' \
    dbname='+secure_data_loader.secure_data['POSTGRES_DB_NAME']+' \
    user='+secure_data_loader.secure_data['POSTGRES_USER']+' \
    password='+secure_data_loader.secure_data['POSTGRES_PASSWORD']+'" > '+secure_data_loader.secure_data['BACKUP_DIR']+'/backup.sql'
    os.system(command)

    # Change working directory
    os.chdir(secure_data_loader.secure_data['BACKUP_DIR'])

    # Setup git config
    if os.path.isdir(".git") is False:
        os.system('git init')
    os.system('git config --global user.email "'+secure_data_loader.secure_data['GIT_EMAIL']+'"')
    os.system('git config --global user.name "'+secure_data_loader.secure_data['GIT_USER']+'"')

    # Git add .
    os.system('git add .')
    
    commit_time = (datetime.now()+ timedelta(hours=8)).strftime('%Y-%m-%d-%H-%M')
    command = 'git commit -m "'+commit_time+'"'
    os.system(command)
    os.system("git log --all --oneline --decorate --graph")
