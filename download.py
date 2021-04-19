from googleapiclient.http import MediaIoBaseDownload


# download image from google drive
def image_download(service, post_folder):

    # get the meta_data for the post image
    query = "mimeType='image/JPEG' and parents in '" + post_folder + "'"
    results = service.files().list(q=query, spaces='drive', fields="nextPageToken, files(id, name, parents)", pageToken=None).execute()

    # get the id for the post image
    images = results.get('files', [])
    image_id = images[-1]["id"]

    # download image
    image_destination = r'C:\Users\William\PycharmProjects\ConservOceanBot\POST\image.jpg'
    request = service.files().get_media(fileId=image_id)
    fh = open(image_destination, 'wb')

    # this block is from the Drive API documentation
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
    results = service.files().list(q=query, spaces='drive', fields="nextPageToken, files(id, name, parents)", pageToken=None).execute()

    # get the id for the post image
    files = results.get('files', [])
    caption_id = files[-1]["id"]

    # download caption
    caption_destination = r'C:\Users\William\PycharmProjects\ConservOceanBot\POST\caption.txt'
    request = service.files().export_media(fileId=caption_id, mimeType='text/plain')
    fh = open(caption_destination, 'wb')

    # this block is from the Drive API documentation
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

    # encoding specification needed to be able to read the emojis
    with open(directory, encoding="utf8") as caption:
        text = caption.read()

    return text
