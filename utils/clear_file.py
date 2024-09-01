import os

def clear_file(dir: str, file_name: str):
    files = os.listdir("./file")
    for file in files:
        if file == file_name:
            os.remove(dir + file_name)
            # os.remove("C:/Users/pedro/Downloads/" + file)
