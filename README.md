# CourseData

## Example Data
[Example Data for CS61C] (https://berkeley.collegescheduler.com/api/terms/2016%20Fall/subjects/COMPSCI/courses/61C/regblocks).
You might have to be logged into your CalNet account. Scroll down past 'registrationBlocks' to see the 'sections'.


## Usage
All of the json files have already been retrieved for you; however, updates to their schedules/courses will probably be made and these won't be reflected in my files.

So you can get them yourself! (however, it takes a long time and if you just want to look at the data just look at the files I already retrieved - time delays between each request to prevent the request from being rejected)

```
from coursedata import *
cookie = "__RequestVerificationToken=INSERT_YOUR_COOKIE_HERE"
set_cookie(cookie)
subject_ids = get_subject_ids()
course_numbers = get_subject_data(subject_ids)
get_courses(course_numbers)
```

You'll also have to supply your own cookie. Go to the [new scheduler] (https://berkeley.collegescheduler.com/spa#courses/add), then open Chrome Developer Console (Ctrl+Shift+i), then go to 'Networks', then refresh the page. Click on of the requests under XHR and copy and paste that cookie into your script.

This will generate a directory of courses and their individual infos/json files.

'get_course_number_from_json' is included as an alternative for getting 'course_numbers' if the subjects jsons are already stored because there is no need to send redundant/useless requests to Berkeley's servers. ):

Disclaimer:
I have no clue what I'm doing :D