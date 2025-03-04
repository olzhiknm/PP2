import os
def list_directories_files(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))], [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def check_path_access(path):
    return os.path.exists(path), os.access(path, os.R_OK), os.access(path, os.W_OK), os.access(path, os.X_OK)

def check_path_exists(path):
    return os.path.exists(path), os.path.basename(path), os.path.dirname(path)

def count_lines_in_file(filename):
    with open(filename, 'r') as file:
        return sum(1 for _ in file)

def write_list_to_file(filename, lst):
    with open(filename, 'w') as file:
        file.writelines("\n".join(lst))

def generate_alphabet_files():
    for letter in range(65, 91):
        with open(f"{chr(letter)}.txt", 'w') as file:
            file.write("")

def copy_file_contents(source, destination):
    with open(source, 'r') as src, open(destination, 'w') as dest:
        dest.write(src.read())

def delete_file(path):
    if os.path.exists(path) and os.access(path, os.W_OK):
        os.remove(path)
