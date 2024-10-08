from pw_imagedataset import *

import getpass
import random


def csv2label( line, zip_filename, img_filename ):
    data = line.split(",")
    return (float(data[1]), data[2])


zip_file = ["images/images_7z.7z", "images/images_zip.zip"]
exts = ['png']

print( "Enter password for zipfile [PassDataset]:" )
pw = getpass.getpass() # PassDataset

dataset = PWImageDataset( zip_file, pw, None, csv2label, exts )

idx = random.randint( 0, len(dataset)-1 )
img_pil, label = dataset[idx]

print( img_pil.size )
print( label )

