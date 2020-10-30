import os
import pickle
from history import History


# reads the pickle file containing our history
def read_history():
    post_history = None

    # read the history if it exists
    if os.path.exists('history.pickle'):
        with open('history.pickle', 'rb') as file:
            post_history = pickle.load(file)

    # create a history list if it doesn't exist
    if not post_history:
        post_history = History()

    return post_history


# updates our serialized/pickled history file
def update_history(post_history, post_number):

    # update post key and post type
    if post_history.post_type:
        post_history.turtle_history = post_number
    else:
        post_history.product_history = post_number

    post_history.post_type = not post_history.post_type

    # serialize our updated history
    with open('history.pickle', 'wb') as file:
        pickle.dump(post_history, file)
