from apscheduler.schedulers.blocking import BlockingScheduler
scheduler = BlockingScheduler()

database_url ='sqlite:///job_store.sqlite'
scheduler.add_jobstore('sqlalchemy', url=database_url)

def add_job_in_jobstore():
    print ("Hello")

job_obj=scheduler.add_job(add_job_in_jobstore, 'interval', seconds=59)
print(job_obj.id)


if __name__ == '__main__':
    print("scheduler starting...")
    scheduler.start()