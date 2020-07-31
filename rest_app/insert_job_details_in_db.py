from sqlalchemy import create_engine , Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

import requests
import calendar
import datetime
import datetime as dt
import json
import uuid
from apscheduler.schedulers.blocking import BlockingScheduler


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
    Joblog         = Column(String(200))
    previousjobid  = Column(String(200))

Base.metadata.create_all(Engine)

# JobId, JobType,CreatedAt, UpdatedAt, JobObject, Jobstatus, Joblog, previousjobid.
sched = BlockingScheduler()

class GitRepoApisDetails:

        previousjobid=''
        flag1=0
        def job_is_get_repo(self,query_url,job_id):

            headers = {'content-type': 'application/json'}
            self.response = requests.get(query_url, headers=headers)
            self.matched_repositories = self.response.json()

            #x = session.query(job_details_by_githubapi).get(job_id)
            if self.matched_repositories['total_count']==0:

                if GitRepoApisDetails.flag1==0:

                    session.query(job_details_by_githubapi).filter(job_details_by_githubapi.JobId == job_id).update({job_details_by_githubapi.Jobstatus:'completed',job_details_by_githubapi.Joblog:self.matched_repositories,job_details_by_githubapi.previousjobid:job_id},synchronize_session=False)
                    GitRepoApisDetails.previousjobid=job_id
                    GitRepoApisDetails.flag1=1
                    session.commit()

                else:

                    session.query(job_details_by_githubapi).filter(job_details_by_githubapi.JobId == job_id).update({job_details_by_githubapi.Jobstatus:'completed',job_details_by_githubapi.Joblog:self.matched_repositories,job_details_by_githubapi.previousjobid:GitRepoApisDetails.previousjobid},synchronize_session=False)
                    GitRepoApisDetails.previousjobid = job_id
                    session.commit()


            else:

                if GitRepoApisDetails.flag1 == 0:

                    session.query(job_details_by_githubapi).filter(job_details_by_githubapi.JobId == job_id).update({job_details_by_githubapi.Jobstatus:'completed',job_details_by_githubapi.Joblog:'got_proper_output',job_details_by_githubapi.previousjobid:job_id},synchronize_session=False)
                    GitRepoApisDetails.previousjobid = job_id
                    GitRepoApisDetails.flag1 = 1
                    session.commit()

                else:

                    session.query(job_details_by_githubapi).filter(job_details_by_githubapi.JobId == job_id).update({job_details_by_githubapi.Jobstatus:'completed',job_details_by_githubapi.Joblog:'got_proper_output',job_details_by_githubapi.previousjobid:GitRepoApisDetails.previousjobid},synchronize_session=False)
                    GitRepoApisDetails.previousjobid = job_id
                    session.commit()

                all_repositories_details = []
                for repo in self.matched_repositories["items"]:

                    repo_details = dict()
                    repo_details["id"] = repo.get("id")
                    repo_details["name"] = repo.get("name")
                    repo_details["full_name"] = repo.get("full_name")
                    repo_details["private"] = repo.get("private")
                    repo_details["owner"] = dict()
                    repo_details["owner"]["login"] = repo.get("owner").get("login")
                    repo_details["owner"]["id"] = repo.get("owner").get("id")
                    repo_details["owner"]["html_url"] = repo.get("owner").get("html_url")
                    repo_details["html_url"] = repo.get("html_url")
                    repo_details["description"] = repo.get("description")
                    repo_details["url"] = repo.get("url")
                    repo_details["contents_url"] = repo.get("contents_url")
                    repo_details["created_at"] = repo.get("created_at")
                    repo_details["updated_at"] = repo.get("updated_at")

                    if repo.get("license"):
                        repo_details["license"] = dict()
                        repo_details["license"]["key"] = repo.get("key")
                        repo_details["license"]["name"] = repo.get("name")
                        repo_details["license"]["spdx_id"] = repo.get("spdx_id")
                        repo_details["license"]["url"] = repo.get("url")

                    repo_details["forks"] = repo.get("forks")
                    repo_details["watchers"] = repo.get("watchers")
                    all_repositories_details.append(repo_details)
            print(all_repositories_details)
            return all_repositories_details


        def get_repo_details_by_month(self,repo_name,year_for_repo,month_for_repo,year,month,day,hour,min,sec=00):

            total_days=calendar.monthrange(year_for_repo,month_for_repo)[1]
            self.total_urls = []

            for days in range(1,total_days+1):

                day_obj = datetime.date(year_for_repo, month_for_repo, days)
                self.target_url = "https://api.github.com/search/repositories?q={repo_name}+created:{date}".format(repo_name=repo_name,date=day_obj)
                self.total_urls.append(self.target_url)

            x = datetime.datetime(year, month, day, hour, min, sec)
            self.add_job_for_githubapi(self.total_urls,x)


        def get_repo_details_by_year(self, repo_name, year):

            self.total_urls = []
            for month in range(1, 13):

                total_days=calendar.monthrange(year,month)[1]
                for days in range(1,total_days+1):

                    day_obj = datetime.date(year, month, days)
                    self.target_url = "https://api.github.com/search/repositories?q={repo_name}+created:{date}".format(repo_name=repo_name,date=day_obj)
                    self.total_urls.append(self.target_url)
            self.add_job_for_githubapi(self.total_urls)

        #total_urls
        def add_job_for_githubapi(self,total_urls,job_date):

            flag = 1
            nextTime = ''

            for url in total_urls:

                uid = uuid.uuid4().hex
                print(uid)
                if flag == 1:

                    nextTime = job_date + dt.timedelta(seconds=10)
                    #nextTime = dt.datetime.now() + dt.timedelta(seconds=5)
                    run_date = dt.datetime.strftime(nextTime, "%Y-%m-%d %H:%M:%S")
                    sched.add_job(obj.job_is_get_repo, 'date', run_date=run_date,  misfire_grace_time=50 ,args=[url,uid])

                    job_object_details = {}
                    for job in sched.get_jobs():

                        job_object_details['name'] = "%s" % job.name
                        job_object_details['trigger'] = "%s" % job.trigger

                    job_details_json = json.dumps(job_object_details)
                    github_api = job_details_by_githubapi(JobId=uid, JobType='github', CreatedAt=nextTime,UpdatedAt='30-07-20',JobObject= job_details_json,Jobstatus='complete', Joblog='log', previousjobid='0')
                    session.add(github_api)
                    session.commit()
                    flag = 0

                else:

                    nextTime = nextTime + dt.timedelta(seconds=10)
                    run_date = dt.datetime.strftime(nextTime, "%Y-%m-%d %H:%M:%S")
                    sched.add_job(obj.job_is_get_repo, 'date', run_date=run_date,  misfire_grace_time=50, args=[url,uid])

                    job_details = {}

                    for job in sched.get_jobs():
                        job_details['name'] = "%s" % job.name
                        job_details['trigger'] = "%s" % job.trigger

                    job_details_json = json.dumps(job_details)
                    github_api = job_details_by_githubapi(JobId=uid, JobType='github', CreatedAt=nextTime,
                                                          UpdatedAt='30-07-20', JobObject=job_details_json,
                                                          Jobstatus='complete', Joblog='log', previousjobid='0')

                    session.add(github_api)
                    session.commit()


obj=GitRepoApisDetails()
url=obj.get_repo_details_by_month("dockerfile",2020,2,2020,7,31,20,5)

#obj.add_job_for_githubapi(2020,7,31,12,30)


try:
    sched.start()
except (Exception):
    pass