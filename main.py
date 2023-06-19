from Country import Country
from Window import Window
import os
from os.path import isfile
import re

# read all files with extension csv and open the window (temperature chart drawer)
if __name__ == '__main__':
    data_dir = os.getcwd() + '\\data'
    ends_with_csv = re.compile(r'.+csv$')

    countries = list()
    for path in os.listdir(data_dir):
        file_path = data_dir + '\\' + path
        if isfile(file_path) and ends_with_csv.search(path, re.IGNORECASE):
            countries.append(Country(file_path))

    window = Window(countries)

    screen = window.get_window()

    print('Everything loaded, displaying window')
    screen.mainloop()
    print('Goodbye')
