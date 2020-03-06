import pyrebase
from google.cloud import storage
# https://console.cloud.google.com/storage/browser/[bucket-id]/
client = storage.Client()
bucket = client.get_bucket('hospital-django.appspot.com')


def upload_file_to_firebase(file):
    print(file.name)
    blob = storage.Blob(f'documents/{file.name}', bucket=bucket)
    blob.upload_from_file(file)
    blob.make_public()
    print(blob.public_url)
