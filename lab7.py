import os
import sys

#exercitiul 1 - citeste din director fisierele cu o extensie anume

def exercitiul1(directory_path, file_extension):
    try:
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Error: '{directory_path}' invalid directory path.")
        
        if not file_extension.startswith('.'):
            raise ValueError(f"Error: '{file_extension}' invalid file extension.")

        files_found = False

        for filename in os.listdir(directory_path):
            if filename.endswith(file_extension):
                files_found = True
                file_path = os.path.join(directory_path, filename)
                
                try:
                    file = open(file_path, 'r') 
                    print(f"--- {filename} ---")
                    print(file.read())
                    print("\n")
                except Exception as e:
                    print(f"Error reading '{filename}': {e}")
                finally:
                    file.close()
        if not files_found:
            print(f"No files with extension '{file_extension}'.")

    except (NotADirectoryError, ValueError) as e:
        print(e)
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python lab7.py <directory_path> <file_extension>")
    else:
        directory_path = sys.argv[1]
        file_extension = sys.argv[2]
        exercitiul1(directory_path, file_extension)

# exercitiul 2 - schimbi fisierele in filei

def exercitiul2(directory):
    try:
        if not os.path.isdir(directory):
            raise NotADirectoryError(f"Error: '{directory}' invalid directory path.")
        files = os.listdir(directory)
        if not files:
            print("No files in directory.")
            return
        for index in range(1, len(files) + 1):
            filename = files[index - 1]
            file_path = os.path.join(directory, filename)
            extension = filename[filename.rfind('.'):]
            new_name = f"file{index}{extension}"
            new_file_path = os.path.join(directory, new_name)
            try:
                os.rename(file_path, new_file_path)
                print(f"{filename} -> {new_name}")
            except OSError as e:
                print(f"Error renaming file '{filename}': {e}")
    except Exception as e:
        print(f"Error: {e}")
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lab7.py <directory_path>")
    else: 
        directory = sys.argv[1]
        exercitiul2(directory)

# exercitiul 3 - calculezi size-ul
def exercitiul3(directory):
    total_size = 0
    try:
        if not os.path.isdir(directory):
            raise NotADirectoryError(f"Error: '{directory}' invalid directory path.")
        
        files = os.listdir(directory)
        
        if not files:
            print("No files in directory.")
            return 0
        
        for filename in files:
            file_path = os.path.join(directory, filename)
            try:
                total_size += os.path.getsize(file_path)
            except PermissionError:
                print(f"Permission denied: {file_path}")
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"Error accessing file '{file_path}': {e}")
        
        return total_size
    except Exception as e:
        print(f"Error: {e}")
        return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lab7.py <directory_path>")
    else: 
        directory = sys.argv[1]
        total_size = exercitiul3(directory)
        
        if total_size >= 0:
            print(f"Total size = {total_size}")

# # exercitiul 4 - numara cate file-uri de o anumita extensie ai

def exercitiul4(directory):
    file_extension_count = {}
    try:
        if not os.path.isdir(directory):
            raise NotADirectoryError(f"Error: '{directory}' invalid directory path.")
        
        files = os.listdir(directory)
        
        if not files:
            print("No files in directory.")
            return file_extension_count
        
        for filename in files:
            file_path = os.path.join(directory, filename)
            dot_index = filename.rfind('.')
            if dot_index != -1: 
                extension = filename[dot_index:]
                if extension in file_extension_count:
                    file_extension_count[extension] += 1
                else:
                    file_extension_count[extension] = 1
            else:
                if 'No extension' in file_extension_count:
                    file_extension_count['No extension'] += 1
                else:
                    file_extension_count['No extension'] = 1
            
        return file_extension_count
    except Exception as e:
        print(f"Error: {e}")
        return {}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lab7.py <directory_path>")
    else: 
        directory = sys.argv[1]
        file_extension_counts = exercitiul4(directory)
        
        if file_extension_counts:
            for ext, count in file_extension_counts.items():
                print(f"{ext if ext else 'No extension'} = {count}")
        else:
            print("No valid files to count.")
