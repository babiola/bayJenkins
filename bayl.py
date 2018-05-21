import jenkinsapi
from jenkinsapi.jenkins import Jenkins
import sqlite3
import sys
from datetime import datetime,date


#url = sys.argv[1]
url = input('Please enter the URL here:')
def populate_target(jenkinsurl):
    server = Jenkins(jenkinsurl.strip(), username='bayl', password='qazwsx123')
    s=server.version
    print('jenkins version running  '+s)
    try:
        conn = sqlite3.connect('seedstars.db')
        c = conn.cursor()
        sql = '''create table Jobs_status (jobname text, status text, date_logged text)'''
        c.execute(sql)
        jobs = server.get_jobs()
        for j in jobs:
            print(j)
            job_instance = server.get_job(j[0])
            print(job_instance.name)
            print('Inserting job '+job_instance.name +' into db')
            time = datetime.strftime(datetime.now(),"%Y%m%d %H:%M:%S")
            c.execute("""insert into Jobs_status('jobname', 'status', 'date_logged') values(?,?,?)""",(job_instance.name,job_instance.is_running(), time))
            conn.commit()
            print(job_instance.name +'  successfully inserted into db')
    except sqlite3.Error:
        print('table already exist..')
        conn = sqlite3.connect('seedstars.db')
        c = conn.cursor()
        jobs = server.get_jobs()
        for j in jobs:
            print(j)
            job_instance = server.get_job(j[0])
            print(job_instance.name)
            print(job_instance.get_description())
            print(job_instance.is_running())
            print('Inserting job '+job_instance.name +' into db')
            time = datetime.strftime(datetime.now(),"%Y%m%d %H:%M:%S")
            c.execute("""insert into Jobs_status('jobname', 'status', 'date_logged') values(?,?,?)""",(job_instance.name,job_instance.is_running(), time))
            conn.commit()
            print(job_instance.name +'  successfully inserted into db')
 
populate_target(url)
