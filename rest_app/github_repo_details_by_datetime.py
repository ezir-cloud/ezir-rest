import requests
import calendar
import datetime
import datetime as dt
from datetime import date,timedelta
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()

class GitRepoApisDetails:

        def job_is_get_repo(self,query_url):

            headers = {'content-type': 'application/json'}
            self.response = requests.get(query_url, headers=headers)
            self.matched_repositories = self.response.json()

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


            return all_repositories_details


        def get_repo_details_by_month(self,repo_name,year,month):


            total_days=calendar.monthrange(year,month)[1]
            self.total_urls = []


            for days in range(1,total_days+1):

                day_obj = datetime.date(year, month, days)
                self.target_url = "https://api.github.com/search/repositories?q={repo_name}+created:{date}".format(repo_name=repo_name,date=day_obj)

                self.total_urls.append(self.target_url)

            self.add_job_for_githubapi(self.total_urls)


        def get_repo_details_by_year(self, repo_name, year):

            self.total_urls = []

            for month in range(1, 13):

                total_days=calendar.monthrange(year,month)[1]

                for days in range(1,total_days+1):

                    day_obj = datetime.date(year, month, days)
                    self.target_url = "https://api.github.com/search/repositories?q={repo_name}+created:{date}".format(repo_name=repo_name,date=day_obj)
                    self.total_urls.append(self.target_url)

            self.add_job_for_githubapi(self.total_urls)


        def get_repo_details_by_two_date(self, repo_name, year1, month1, days1, year2, month2, days2):

            start_dt = date(year1, month1, days1)
            end_dt = date(year2, month2, days2)
            self.total_urls = []

            for index in range((end_dt - start_dt).days + 1):

                new_date = start_dt + timedelta(index)
                day_obj = new_date.strftime("%Y-%m-%d")

                self.target_url = "https://api.github.com/search/repositories?q={repo_name}+created:{date}".format(repo_name=repo_name, date=day_obj)
                self.total_urls.append(self.target_url)

            self.add_job_for_githubapi(self.total_urls)


        def  get_repo_by_date(self, repo_name, year , month, date ):


            day_obj = datetime.date(year, month, date)
            self.target_url = "https://api.github.com/search/repositories?q={repo_name}+created:{date}".format(repo_name=repo_name, date=day_obj)
            self.job_is_get_repo(self.target_url)



        def add_job_for_githubapi(self, total_urls ):

            flag = 1
            nextTime = ''

            for url in total_urls:

                if flag == 1:

                    nextTime = dt.datetime.now() + dt.timedelta(seconds=5)
                    run_date = dt.datetime.strftime(nextTime, "%Y-%m-%d %H:%M:%S")
                    sched.add_job(obj.job_is_get_repo, 'date', run_date=run_date,  misfire_grace_time=50 ,args=[url])
                    flag = 0

                else:

                    nextTime = nextTime + dt.timedelta(seconds=1)
                    run_date = dt.datetime.strftime(nextTime, "%Y-%m-%d %H:%M:%S")
                    sched.add_job(obj.job_is_get_repo, 'date', run_date=run_date,  misfire_grace_time=50, args=[url])



obj=GitRepoApisDetails()
url=obj.get_repo_details_by_month("dockerfile",2020,2)
url=obj.get_repo_details_by_year("dockerfile",2019)
url=obj.get_repo_by_date("dockerfile", 2020 , 1, 1)
url = obj.get_repo_details_by_two_date("dockerfile", 2019 , 1, 1, 2020, 1, 1 )

try:
    sched.start()
except (Exception):
    pass
