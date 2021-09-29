# file_compressor/compressor/tasks.py
import os 
from celery import shared_task
from django.conf import settings
import lzma
import zlib

# The celery task that compresses the file in the background taking file path as its parameter
# Returns results dict {archive_path, file_size, zip_file_size, ratio}
@shared_task
def compress_file(file_path):
    os.chdir(settings.FILES_DIR)
    path, file = os.path.split(file_path)
    file_name, ext = os.path.splitext(file)
    file_size = os.path.getsize(file_path)
    zip_file = f"{file_name}.xz"
    zip_file_path = f"{settings.MEDIA_URL}files/{zip_file}"
    results = {'archive_path': zip_file_path, 'file_size': file_size}
    
    try:
        bin = open(file_path, "rb")
        data = bin.read()
        # Tried lzma first and got a compression ratio of ~1.72:1 
        # then I read about zlib which is also a lossless compression and got ~1.27:1 
        #compressed_data = zlib.compress(data)
        f1 = lzma.open(zip_file, "wb")
        #f1 = open(zip_file, 'wb')
        f1.write(compressed_data)
        f1.close()
        
        zip_file_size = os.path.getsize(zip_file)

        results["zip_file_size"] = zip_file_size
        results["ratio"] = round(int(file_size)/int(zip_file_size), 2)
        bin.close()
        os.remove(file_path)

    except IOError as e:
        print(e)
        return e

    return results
