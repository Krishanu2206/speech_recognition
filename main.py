import sys
from api_communation import *

filename = sys.argv[1]

##CALLING THE FUNCTIONS
audio_url = upload(filename)
job_id = transcribe(audio_url)
print("job_id: ", job_id)

save_transcript(audio_url, filename)