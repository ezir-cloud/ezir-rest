import calendar
import datetime
import datetime as dt
import json
import uuid


from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

sched = BlockingScheduler()

Engine = create_engine('sqlite:///github_repo_job_details.sqlite')
Base = declarative_base()
Session_macker = sessionmaker( bind= Engine)
session = Session_macker()

class job_details_by_githubapi(Base):
    __tablename__ = 'job_details_by_githubapi'
    JobId          = Column(String(200),  primary_key=True)
    JobType        = Column(String(200))
    CreatedAt      = Column(String(200))
    UpdatedAt      = Column(String(200))
    JobObject      = Column(String(200))
    Jobstatus      = Column(String(200))
    Joblog         = Column(String(500))
    previousjobid  = Column(String(200))

Base.metadata.create_all(Engine)

class GitRepoApisDetails:

    def job_is_get_repo(self,query_url):
        print(query_url)

    def get_repo_details_by_month(self,file_name, file_created_year, file_created_month,  job_year, job_month, job_day, job_hr, job_min, job_sec,  job_interval_count):

        total_days=calendar.monthrange(file_created_year,file_created_month)[1]

        nextTime = None
        for days in range(1,total_days+1):

            day_obj = datetime.date(file_created_year, file_created_month, days)
            target_url = "https://api.github.com/search/repositories?q={repo_name}+created:{date}".format(repo_name=file_name,date=day_obj)

            uid = uuid.uuid4().hex
            if nextTime is None:
                job_run_time = dt.datetime(job_year, job_month, job_day, job_hr, job_min, job_sec)
                nextTime =job_run_time + dt.timedelta(seconds=job_interval_count)
                run_date = dt.datetime.strftime(nextTime, "%Y-%m-%d %H:%M:%S")
                self.add_job_by_time(target_url,  run_date, uid)

            else:
                nextTime = nextTime + dt.timedelta(seconds=job_interval_count)
                run_date = dt.datetime.strftime(nextTime, "%Y-%m-%d %H:%M:%S")
                self.add_job_by_time(target_url,  run_date, uid)

    def add_job_by_time(self, target_url, run_date, uid):

        sched.add_job(obj.job_is_get_repo, 'date', run_date=run_date, misfire_grace_time=10, args=[target_url], id=uid)
        #
        # job_details = {}
        # for job in sched.get_jobs():
        #     job_details['name'] = "%s" % job.name
        #     job_details['trigger'] = "%s" % job.trigger
        # job_details_json = json.dumps(job_details)
        #
        # github_repo_api = job_details_by_githubapi(JobId=uid, JobType='github', CreatedAt=run_date,
        #                                            UpdatedAt='', JobObject=job_details_json,
        #                                            Jobstatus='pending', Joblog='job log', previousjobid='0')
        # session.add(github_repo_api)
        # session.commit()


obj=GitRepoApisDetails()
# (file_name, file_created_year, file_created_month,job_year, job_month, job_day, job_hr, job_min, job_sec,  job_interval_count):
obj.get_repo_details_by_month("dockerfile", 2020, 4, 2020, 8, 5, 15, 51, 40, 10)

sched.start()