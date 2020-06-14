import os
import glob
import shutil
from scrapper import home_folder

august_date = 1564617600
september_date = 1567296000
october_date = 1569888000
november_date = 1572566400
december_date = 1575158400
january_date = 1577836800
february_date = 1580515200
march_date = 1583020800
april_date = 1585699200
may_date = 1588291200
june_date = 1590969600

months = ['June', 'August', 'May', 'April', 'March', 'February',
          'January', 'December', 'November', 'October', 'September', 'WTF']

for month in months:
    directory = home_folder + month
    if not os.path.exists(directory):
        os.mkdir(directory)


def check_month(date):

    if date >= june_date:
        return 'June'
    if date >= may_date:
        return 'May'
    if date >= april_date:
        return 'April'
    if date >= march_date:
        return 'March'
    if date >= february_date:
        return 'February'
    if date >= january_date:
        return 'January'
    if date >= december_date:
        return 'December'
    if date >= november_date:
        return 'November'
    if date >= october_date:
        return 'October'
    if date >= september_date:
        return 'September'
    if date >= august_date:
        return 'August'
    else:
        return 'WTF'

def move(file_name, folder):
    print folder, home_folder
    shutil.move(home_folder + file_name, home_folder + folder + '\\' + file_name)

file_ex = ['jpg', 'mp4', 'mov']

if __name__ == "__main__":
    file_list = []
    for ext in file_ex:
        file_list += glob.glob(home_folder + '*.' +ext)

    for file in file_list:
        file_name = file.split('\\')[-1]
        date_file = int(file_name.split('.')[0])
        folder = check_month(date_file)
        move(file_name, folder)