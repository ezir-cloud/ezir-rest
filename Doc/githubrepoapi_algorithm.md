Step 1 : Start     
Step 2 : Create Github class   
Step 3: Create function get_repo_details   
Step 4: Initialize  target url (https://api.github.com/search/repositories)    
Step 5 : Take  year, month with day,year, date with month,year,or take start date and last date.    
Step 6  : First api call takes total count and 100 repositories details.    
Step 7: If total count more than 100 then again api call.    
Step 8 : Every day total count is less than 1000 or equal to 1000 api call 1 to 10 times and  get repositories details.       
Step 9 : If total count is more than 1000 then the api call with time.    
Step 10 : The api call with time based on one hour.that means the api call 24 times(24hrs) .    
Step 11: If total count is more than 1000 in one hour then the api call with min.    
Step 12 :  Api call with min is 60 times. First 30 api call first min and last 30 api call second min.    
Step 13 : After one hour the api call with the second hour and get repositories details.    
Step 14:  End   
 