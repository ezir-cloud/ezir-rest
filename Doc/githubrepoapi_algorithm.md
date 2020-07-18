<<<<<<< HEAD
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

Create function get_repo_details_by_two_date(repo_name,start_date, last_late) 
Create link between start date 2019-01-01  and last date 2020-01-01 
Example   
https://api.github.com/search/repositories?q=dockerfile+created:2019-01-01..2020-01-31  

1. this condition is applied in the above four functions.    
- If github search api results more than 1,000 then it searches by time   
and  this condition is applied in the above four functions.The time limit of github search api is one hour that means    
every search api gets results of one hour.    
Example    
https://api.github.com/search/repositories?q=dockerfile+created:2020-01-01T14:00:00Z..2020-01-01T19:00:00Z      

- If a github search api of one hour is more than 1,000 then it searches by min that means every search api gets    
results of one min.    
https://api.github.com/search/repositories?q=java+created:2020-01-01T14:02:00Z..2020-01-01T14:03:00Z   
   
Every url which is used to search the results in the github is based on a job.every job is scheduled by one min. The    
job details are saved in sqlite database using sqlalchemy. Table name is githubapijob . columns are JobId, JobType,     
CreatedAt, UpdatedAt,  JobObject.    
 
    

=======
Step 1 : Start     
Step 2 : Create Github class   
Step 3: Create function get_repo_details   
Step 4: Initialize  target url (https://api.github.com/search/repositories)    
Step 5 : Take  year eg 2012, month eg 2020-01, date eg 2020-01-01,or take start date and last date 2020-01-01 to 2020-01-25.     
Step 6  : First api call takes total count and 100 repositories details.    
Step 7: If total count more than 100 then again api call.    
Step 8 : Every day total count is less than 1000 or equal to 1000 api call 1 to 10 times and  get repositories details.       
Step 9 : If total count is more than 1000 then the api call with time.    
Step 10 : The api call with time based on one hour.that means the api call 24 times(24hrs) .    
Step 11: If total count is more than 1000 in one hour then the api call with min.    
Step 12 :  Api call with min is 60 times. First 30 api call first min and last 30 api call second min.    
Step 13 : After one hour the api call with the second hour and get repositories details.    
Step 14:  End   
 
>>>>>>> e279b6e76cb058e8def611f63e84d57c772678fd
