Using Python and the Flask framework, a REST API was developed on an AWS EC2 instance via the Git Bash terminal.
The API pulls data about an MMA organisation "UFC" from an API service called Sportradar, and returns it to the 
user. A trial account was created with Sportradar, which provided limited API requests, and so a script called 
"downloadData.py" was created to download all the necessary sports data. This was stored in "ufc_full_competitions.json", 
essentially caching the data, which meant that no more API requests were necessary (unless the data was to be updated),
and also the wait-times were significantly reduced since API calls were no longer required (approx. 300ms per API call).

There are two URL endpoints; "/" and "/compData". The first one brings the user to a homepage, where the choice is given
to view information about previous or upcoming events, and also the number of previous/upcoming events to display. 
The second endpoint provides raw data about both previous and upcoming events, and is provided in a JSON format.
