# traveltime

This python script (wrapped in docker and docker-compose) will find which city is optimal for your
team members to attend.

Create a .env file with API keys from [https://traveltime.com] (see `.env.example`). Put the people
into `input/people/collection_name.yml`, put a list of groups and their members into
`input/groups/collection_name.yml` and potentially update `input/cities.yml` with more relevant
locations, then run `docker-compose up` and you'll find the output in `output/output.csv`.

You may need to update the postcode-outcodes.csv from [FreeMapTools](https://www.freemaptools.com/download-uk-postcode-lat-lng.htm).

This code is currently being used to prove some timings for meetings for UK TAMs, but there is no
reason why the journey engine couldn't be swapped out for something to work in other regions.

**Note that no determination has been made to confirm whether traveltime.com is the "right" tool
for the job, nor that it is released under an appropriate use. This is for a POC ONLY!**

Any questions, please contact the author,
[Jon Spriggs](https://phonetool.amazon.com/users/jonsprig).
