import os

download_dir = '/workspaces/slack-images/downloads'
os.makedirs(download_dir, exist_ok=True)

# When saving files, use download_dir as the base path
file_path = os.path.join(download_dir, 'your_file.ext')
with open(file_path, 'wb') as f: