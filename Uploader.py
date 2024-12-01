import os

def WriteFile(filename, file):
    # Create a directory to store files if it doesn't exist
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Construct the file path
    filepath = os.path.join(upload_dir, file.filename)

    # Save the file to disk
    try:
        with open(filepath, "wb") as f:
            f.write(file.file.read())
    except Exception as e:
        raise f"opload failed : {e}"

