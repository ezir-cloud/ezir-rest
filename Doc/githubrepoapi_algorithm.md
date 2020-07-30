
## Title and People    

This documentation is about github api. Github  Search API helps you search for the specific item you want to find.    
For example, you can find a user or a specific file in a repository etc.     
 
## Overview   
This documentation is about searching the repositories in github. Search the repositories by repository name which     
gives the total count of those repositories in github.Think of it the way you think of performing a search on Google.    
It's designed to help you find the one result you're looking for just like searching on Google.To satisfy that need,    
the GitHub Search API provides up to 1,000 results for each search.     

## Context   
GitHub Search API provides up to 1,000 results for each search. The problem is that if search API results more than     
1,000 then how to handle it.This project is necessary for getting all results that are provided by github search API.   

## Existing Solution 

- Rate limit       
a . The Search API has a custom rate limit. For requests using Basic Authentication, OAuth,   or client ID and secret,   
you can make up to 30 requests per minute.   
b . For unauthenticated requests, the rate limit allows you to make up to 10 requests per minute.   
  
- Pagination   
a.  Requests that return multiple items will be paginated to 30 items by default.You can specify further pages with the  
?page parameter.   
Example    
https://api.github.com/search/repositories?q=dockerfile    
https://api.github.com/search/repositories?q=dockerfile&page=1      

b. For some resources, you can also set a custom page size up to 100 with the ?per_page parameter    
Example   
https://api.github.com/search/repositories?q=dockerfile&per_page=100    

## Proposed Solution   
GitHub Search API provides up to 1,000 results for each search.  Github search api provides searching results by date   
and time. Github search api is searching results for every day and  provides results till  1,000. If the results is    
more than 1,000 then github search api is searching results with time.     

Example GitHub Search API using date   
https://api.github.com/search/repositories?q=dockerfile+created:2013-01-01    
 
Example GitHub Search API using date and time    
https://api.github.com/search/repositories?q=dockerfile+created:2020-01-01T14:00:00Z..2020-01-01T19:00:00Z     

Create GithubRepoDetails class  
Four functions are  github search api by every day.    
- Create function get_repo_details_by_year(repo_name, year)     
Create 365 and 366 links for github api    
Example
https://api.github.com/search/repositories?q=dockerfile+created:2020-01-01   
    
- Create function get_repo_details_by_month(repo_name,month,year)     
Create 30 or 31 links for github api   
Example     
https://api.github.com/search/repositories?q=dockerfile+created:2020-01-01   

- Create function get_repo_details_by_date(repo_name,year, month, date)    
Create one link of specified date  for github api   

- Create function get_repo_details_by_two_date(repo_name,start_date, last_late)         
Create link between start date 2019-01-01  and last date 2020-01-01 
Example   
https://api.github.com/search/repositories?q=dockerfile+created:2019-01-01..2020-01-31  

1. this condition is applied in the above four functions.    
- If github search api results more than 1,000 then it searches by time   
and  this condition is applied in the above four functions.The time limit of github search api is one hour that means    
every search api gets results of one hour.    
Example    
https://api.github.com/search/repositories?q=dockerfile+created:2020-01-01T14:00:00Z..2020-01-01T15:00:00Z      

- If a github search api of one hour is more than 1,000 then it searches by min that means every search api gets    
results of one min.    
https://api.github.com/search/repositories?q=java+created:2020-01-01T14:02:00Z..2020-01-01T14:03:00Z   
   

* Every url which is used to search the results in the github is passed in function arguments.Each function call by job.  
Every job is scheduled by one min. The job details are saved in sqlite database using sqlalchemy. Table name is    
githubapijob . columns are JobId, JobType,CreatedAt, UpdatedAt, JobObject, Jobstatus, Joblog, previousjobid.      


* Pass job id in add.job argument and use job id to job function if api work properly then job status is complete.     
if job is not complete the api response add in gob log and got status is fail and create new job the old job id is      
stored in previousjobid column.   

 
Column of githubapijob table    
JobId : every job has a unique id.     
JobType : job type is github api    
CreatedAt : when url is passed as argument to that time store in CreatedAt.    
UpdatedAt : This is the update time of the job.    
JobObject : The job object is serialized.    
Jobstatus : Jobstatus are running, completed and fail. When a job fail it retry after completing all jobs.     
Joblog    : joblog column has four things. First  job complete, successful status.second  If  Api calls, the total count   
is zero then this statement is store in log.  {   
  "total_count": 0,    
  "incomplete_results": false,   
  "items": [   
   
  ]   
}     
Third, use a job using try and exception. If a job fails then the exception is stored in the logjob column.        
previousjobid: first job id is 1. if first job is fail. then it create new job  with job id 2. if second job is fail then    
create new job with job id 3. These records are in  previousjobid column.   
 
* If the search api gets a total count is less than 100 and equal to 100 repositories details stored in elasticsearch    
database.if total count is more than 100 then first stored 100 repositories details and create  the second url to      
search more repositories details.     


* The first job is running and takes 1 to 100 repository details then the second job is running and takes  1 to 100     
repository details till the last job. That means total jobs that are created to search api results. If the search       
result is more than 100  then create a new url and create a new job  that runs after completing all the available jobs.      

