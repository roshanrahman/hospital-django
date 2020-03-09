from google.cloud import storage
# https://console.cloud.google.com/storage/browser/[bucket-id]/
client = storage.Client()
bucket = client.get_bucket('hospital-django.appspot.com')


def upload_file_to_firebase(file):
    print(file.name)
    try:
        blob = storage.Blob(f'documents/{file.name}', bucket=bucket)
        blob.upload_from_file(file, content_type=file.content_type)
        blob.make_public()
        return blob.public_url
    except Exception as e:
        print(e)
        return None
