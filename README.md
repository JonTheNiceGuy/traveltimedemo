# Traveltime Demo

** ARCHIVE NOTICE **

This code was written while I was in a former role, and was written in my personal time in that role.

That said, I no longer work in that role, and so now this code is archived in case anyone else can make
use of it.

Please don't ask me for help, but please do consider using the tooling here for your own purposes!

---

This python script (wrapped in docker and docker-compose) will find which city is optimal for your
team members to attend.

Create a .env file with API keys from [https://traveltime.com] (see `.env.example`). Put the people
into `input/people/collection_name.yml`, put a list of groups and their members into
`input/groups/collection_name.yml` and potentially update `input/cities.yml` with more relevant
locations, then run `docker-compose up` and you'll find the output in `output/output.csv`.

You may need to update the postcode-outcodes.csv from [FreeMapTools](https://www.freemaptools.com/download-uk-postcode-lat-lng.htm).

This code is currently being used to prove some timings for meetings for UK Team Members, but there is no
reason why the journey engine couldn't be swapped out for something to work in other regions.

**Note that no determination has been made to confirm whether traveltime.com is the "right" tool
for the job, nor that it is released under an appropriate use. This is for a POC ONLY!**

---

Please note the following attributions:
> Contains Ordnance Survey data © Crown copyright and database right 2021
> 
> Contains Royal Mail data © Royal Mail copyright and database right 2021
> 
> Source: Office for National Statistics licensed under the Open Government Licence v.3.0
