import calendar
import datetime
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

class GitRepoApisDetails:

    def get_repo_details_by_month(self, repo_name, year, month):

        total_days=calendar.monthrange(year, month)[1]

        github_repo_urls = []
        sched = BlockingScheduler()
        for days in range(1, total_days+1):

            day_obj = datetime.date(year, month, days)
            self.target_url = "https://api.github.com/search/repositories?q={repo_name}+created:{date}".format(repo_name=repo_name,date=day_obj)
            self.url_jobs= sched.add_job(self.some_job, 'interval', seconds=1, args = [self.target_url])
            github_repo_urls.append(self.url_jobs)

            # github_repo_urls.append(self.target_url)

        print(github_repo_urls)

    def some_job(self):
        print("job by interval")

obj=GitRepoApisDetails()
obj.get_repo_details_by_month("dockerfile", 2020, 2)