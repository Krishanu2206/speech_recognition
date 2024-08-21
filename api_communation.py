import requests
from api_secrets import API_KEY_ASSEMBLY_AI
import time

#upload the file 
upload_endpoint = 'http://api.assemblyai.com/v2/upload'
transcript_endpoint = 'http://api.assemblyai.com/v2/transcript'

headers = {'authorization': API_KEY_ASSEMBLY_AI}

def upload(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data

    response = requests.post(upload_endpoint,
                            headers=headers,
                            data=read_file(filename))

    audio_url = response.json()['upload_url']
    return audio_url

# transcribe the file recording
def transcribe(audio_url):
    transcript_json = {"audio_url" : audio_url}
    transcript_response = requests.post(transcript_endpoint, json=transcript_json, headers=headers)

    job_id = transcript_response.json()['id']
    return job_id

## Polling
def poll(job_id):
    polling_endpoint = transcript_endpoint + '/' + job_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()

def get_transcription_results_url(audio_url):
    job_id = transcribe(audio_url)
    while True:
        data = poll(job_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
        
        print("WAITING 30 SECONDS...")
        time.sleep(30)

# Saving the transcript

def save_transcript(audio_url, filename):
    data, error = get_transcription_results_url(audio_url)
    if error:
        print("Error: ", error)
    print(data)

    text_filename = filename + ".txt"
    with open(text_filename, "w") as f:
        f.write(data['text'])

    print("Transcript saved to: ", text_filename)



