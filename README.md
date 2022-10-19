# traveltime

This python script (wrapped in docker and docker-compose) will find which city is optimal for your team members to attend.

Create a .env file with API keys from [https://traveltime.com] (see `.env.example`). Put the people
into `people/collection_name.yml`, put a list of groups and their members into
`groups/collection_name.yml` and potentially update `cities.yml` with more relevant locations, then
run `docker-compose up` and you'll find the output in `output/output.csv`.

You may need to update the postcode-outcodes.csv from [FreeMapTools](https://www.freemaptools.com/download-uk-postcode-lat-lng.htm).
