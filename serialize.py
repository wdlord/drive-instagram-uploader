import os
import pickle
from history import History


# reads the pickle file containing our history
def read_history():
    history = None

    # read the history if it exists
    if os.path.exists('history.pickle'):
        with open('history.pickle', 'rb') as file:
            history = pickle.load(file)

    # create a history list if it doesn't exist
    return history or History()


# updates our serialized/pickled history file
def update_history(history):
    history.swap()

    # serialize our updated history
    with open('history.pickle', 'wb') as file:
        pickle.dump(history, file)
