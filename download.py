from googleapiclient.http import MediaIoBaseDownload


# download image from google drive
def image_download(service, post_folder):

    # get the meta_data for the post image
    query = "mimeType='image/JPEG' and parents in '" + post_folder + "'"
    results = service.files().list(q=query, spaces='drive', fields="nextPageToken, files(id, name, parents)",
                                   pageToken=None).execute()

    # get the id for the post image
    images = results.get('files', [])
    for image in images:
        image_id = image["id"]

    # download image
    image_destination = r'<directory here>/image.jpg'
    request = service.files().get_media(fileId=image_id)
    fh = open(image_destination, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print
        "Download %d%%." % int(status.progress() * 100)
    fh.close()

    # for future reference of uploading this image
    return image_destination


# download the caption from google drive
def caption_download(service, post_folder):

    # get the metadata for the google doc containing the caption
    query = "mimeType='application/vnd.google-apps.document' and parents in '" + post_folder + "'"
    results = service.files().list(q=query, spaces='drive', fields="nextPageToken, files(id, name, parents)",
                                   pageToken=None).execute()

    # get the id for the post image
    files = results.get('files', [])
    for file in files:
        caption_id = file["id"]

    # download caption
    caption_destination = r'<directory here>/caption.txt'
    request = service.files().export_media(fileId=caption_id, mimeType='text/plain')
    fh = open(caption_destination, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print
        "Download %d%%." % int(status.progress() * 100)
    fh.close()

    # for future reference of uploading this image
    return caption_destination


# convert pdf to string
def extract_caption(directory):

    # I don't know exactly how this works, but emoji don't get read correctly otherwise.
    with open(directory, encoding="utf8") as caption:
        text = caption.read()

    return text
