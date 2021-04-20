from __future__ import print_function

import os  # used for file manipulation (built-in)
import auth  # class containing code to enter the drive
import download  # class containing download from drive functions
import serialize  # class containing functions for saving history
from instabot import Bot  # module for uploading to Instagram (imported module)


def main():
    # ------
    # setup
    # ------

    service = auth.login()  # enters the drive account
    history = serialize.read_history()

    # -----------------------------
    # read history and select post
    # -----------------------------

    # used to search through files in Google Drive
    query = "mimeType='application/vnd.google-apps.folder' and name contains "
    query += "'TRTLE'" if history.post_type == 'turtle' else "'PST'"

    # get the set of turtle posts or product posts from the Drive
    results = service.files().list(q=query, spaces='drive', fields="nextPageToken, files(id, name, parents)", pageToken=None).execute()
    folders = results.get('files', [])

    history.update_post_number(len(folders))    # we do this now in case an new post was added to the drive since last run
    post_number = history.turtle if history.post_type == 'turtle' else history.product
    folder = folders[-post_number]  # list of folders is stored backwards in Drive

    # prepare image
    image_location = download.image_download(service, folder["id"])

    # prepare caption
    caption_location = download.caption_download(service, folder["id"])
    caption_text = download.extract_caption(caption_location)

    # saves the history
    serialize.update_history(history)

    # -------------
    # POSTING CODE
    # -------------

    with open('loginInfo', 'r') as file:
        username = file.readline().strip()
        password = file.readline().strip()

    # start bot
    bot = Bot()
    bot.login(username=username, password=password)

    # prints error codes (200 means success)
    if bot.api.last_response != 200:
        print(bot.api.last_response)

    bot.upload_photo(image_location, caption=caption_text)

    # delete junk file
    os.chdir(r"C:\Users\William\PycharmProjects\ConservOceanBot\POST")
    os.remove('image.jpg.REMOVE_ME')


if __name__ == '__main__':
    main()
