from __future__ import print_function

import os # used for file manipulation
import auth  # class containing code to enter the drive
import download  # class containing download from drive functions
import serialize  # class containing functions for saving history
import history
from instabot import Bot  # module for uploading to Instagram


def main():
    # enters the drive account
    service = auth.login()

    # read the history, which contains the last posts data [type, last_turtle, last_product]
    post_history = serialize.read_history()

    # -----------------------------------------------------
    # read history and select post
    # -----------------------------------------------------

    # used to search through files in google drive, we will append the folder name to get in the next step
    query = "mimeType='application/vnd.google-apps.folder' and name contains"

    # set the type of post to be making today
    # history is updated on program run because new files may have been added
    if post_history.post_type:
        query += " 'TRTLE'"
        post_number = post_history.turtle_history + 1
    else:
        query += " 'PST'"
        post_number = post_history.product_history + 1

    # get the set of turtle posts or product posts
    results = service.files().list(q=query, spaces='drive', fields="nextPageToken, files(id, name, parents)",
                                   pageToken=None).execute()
    folders = results.get('files', [])

    # loop around the post schedule if we've reached the end
    if post_number > len(folders):
        post_number = 1

    # find the folder containing the image and caption files
    folder = folders[len(folders) - post_number]     # list of folders is stored backwards in drive

    # prepare image
    image_location = download.image_download(service, folder["id"])

    # prepare caption
    caption_location = download.caption_download(service, folder["id"])
    caption_text = download.extract_caption(caption_location)

    # updates the history for next run
    serialize.update_history(post_history, post_number)

    # -------------
    # POSTING CODE
    # -------------

    # start bot
    bot = Bot()
    bot.login(username="<instagram username here>", password="<instagram password here>")

    # prints errors
    if bot.api.last_response != 200:
        print(bot.api.last_response)

    bot.upload_photo(image_location, caption=caption_text)

    # delete junk file
    os.chdir(r"<directory containing post here>")
    os.remove('image.jpg.REMOVE_ME')


if __name__ == '__main__':
    main()
