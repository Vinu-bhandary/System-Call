import os


def create_folder(path):
    try:
        os.makedirs(path)
        return 'TrueC'

    except Exception as e:
        return e


def rename_folder(path, new_path):
    try:
        os.rename(path, new_path)
        return 'TrueR'

    except Exception as e:
        return e


def move_folder(src, dest):
    try:
        os.replace(src, dest)
    except Exception as e:
        print(f"An error occurred: {e}")


def delete_folder(path):
    try:
        os.rmdir(path)
        return 'TrueD'
    except Exception as e:
        return e


def open_folder(path):
    try:
        os.startfile(path)
        return 'TrueO'
    except Exception as e:
        return e

def find_folder(file_name):
    user= os.path.expanduser("~")
    try:
        search_path = [user,"C:\\", "D:\\", "E:\\","G:\\"]
        for path in search_path:
            for root,dirs,files in os.walk(path):
                if file_name in dirs:
                    return os.path.join(root, file_name)
        exit
    except Exception as e:
        exit

