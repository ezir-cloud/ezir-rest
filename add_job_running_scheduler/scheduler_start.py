from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from pytz import utc


jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///job_store.sqlite',tablename='apscheduler_jobs')
}
executors ={
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
job_defaults ={
        'coalesce': False,
        'max_instances': 3
    }

scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
print("scheudler_start: ", id(scheduler))


def add_job_in_jobstore():
    print ("Hello")

job_obj=scheduler.add_job(add_job_in_jobstore,  'interval', seconds=5)
print(job_obj.id)

if __name__ == '__main__':
    print("scheduler starting...")
    scheduler.start()
