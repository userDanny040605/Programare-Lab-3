import os
import datetime

# Folder location
folder_path = "python"

# Dictionary to store file information
files_info = {}

def commit():
    global files_info
    for filename, info in files_info.items():
        info['changed'] = False
    print("Snapshot updated to:", datetime.datetime.now())

def get_file_info(filename):
    file_info = {}
    file_path = os.path.join(folder_path, filename)
    file_info['extension'] = filename.split('.')[-1]
    file_info['created'] = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
    file_info['updated'] = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
    if file_info['extension'] in ['png', 'jpg']:
        size = os.path.getsize(file_path)
        file_info['size'] = size
    elif file_info['extension'] == 'txt':
        with open(file_path, 'r') as file:
            lines = file.readlines()
            file_info['line_count'] = len(lines)
            file_info['word_count'] = sum(len(line.split()) for line in lines)
            file_info['char_count'] = sum(len(line) for line in lines)
    elif file_info['extension'] in ['py', 'java']:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            file_info['line_count'] = len(lines)
            file_info['class_count'] = sum(1 for line in lines if line.strip().startswith("class "))
            file_info['method_count'] = sum(1 for line in lines if line.strip().startswith("def "))
    return file_info

def info(filename):
    if filename not in files_info:
        files_info[filename] = get_file_info(filename)
    file_info = files_info[filename]
    if file_info['extension'] in ['png', 'jpg']:
        print("Image file:", filename)
        print("Size:", file_info.get('size', 'N/A'), "bytes")
    elif file_info['extension'] == 'txt':
        print("Text file:", filename)
        print("Line count:", file_info.get('line_count', 'N/A'))
        print("Word count:", file_info.get('word_count', 'N/A'))
        print("Character count:", file_info.get('char_count', 'N/A'))
    elif file_info['extension'] in ['py', 'java']:
        print("Program file:", filename)
        print("Line count:", file_info.get('line_count', 'N/A'))
        print("Class count:", file_info.get('class_count', 'N/A'))
        print("Method count:", file_info.get('method_count', 'N/A'))

def status():
    print("Current snapshot time:", datetime.datetime.now())
    for filename, info in files_info.items():
        file_path = os.path.join(folder_path, filename)
        updated_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        if info['updated'] > updated_time:
            print(filename, "was changed since last snapshot.")
        else:
            print(filename, "was not changed since last snapshot.")

def interactive_command_line():
    while True:
        command = input("Enter command (commit/info <filename>/status): ").strip().split()
        if command[0] == "commit":
            commit()
        elif command[0] == "info" and len(command) == 2:
            filename = command[1]
            info(filename)
        elif command[0] == "status":
            status()
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    interactive_command_line()
