import Diff
import json


if __name__ == '__main__':
    with open('stories/store1.json') as store_file:    
        store = json.load(store_file)

    print(Diff.diffPoints(store[0], store[1]))
