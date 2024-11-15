# mtanaka@sc.e.titech.ac.jp

# https://qiita.com/kotai2003/items/a7de8adc204d5b9218d8
# https://qiita.com/fuutot/items/d29e0928d66379fad96d

from torch.utils.data import Dataset
from PIL import Image
import zipfile
import py7zr
import io
import os

# https://qiita.com/robozushi10/items/b334357244739d47f39e
# % 7z a -mx=1 -pPassDataset images.7z images/*.png

class PWImageDataset(Dataset):
    def __init__(self, zip_filenames, pw, transform=None, csv2label=None, exts=['png','jpg']):
        self.transform = transform
        self.csv2label = csv2label
        self.zip_filenames = zip_filenames
        if( not ( isinstance(pw, str ) or isinstance(pw, bytes ) ) ):
            raise TypeError("pw should be str or bytes.")

        if( isinstance(pw, str ) ):
            self.pw = pw.encode()

        self.filenames = []

        for zip_filename in self.zip_filenames:
            if( zip_filename.endswith(".zip") ):
                with zipfile.ZipFile(zip_filename, "r") as zp:
                    namelist = zp.namelist()

                    try:
                        with zp.open(namelist[0], pwd=self.pw) as f:
                            dummy = f.read()
                    except RuntimeError:
                        raise RuntimeError("Wrong Password.")

                    csv_filenames = [f for f in namelist if f.endswith(".csv")]
                    lines = []
                    for csv_filename in csv_filenames:
                        with zp.open(csv_filename, pwd=self.pw) as f:
                            lines += f.read().decode().splitlines()

            elif( zip_filename.endswith(".7z") ):
                with py7zr.SevenZipFile(zip_filename, "r", password=self.pw.decode()) as zp:
                    namelist = zp.getnames()

                    try:
                        zp.read([namelist[0]])
                    except Exception as e:
                        raise RuntimeError("Wrong Password.")

                with py7zr.SevenZipFile(zip_filename, "r", password=self.pw.decode()) as zp:
                    csv_filenames = [f for f in namelist if f.endswith(".csv")]
                    lines = []
                    for _, bio in zp.read(csv_filenames).items():
                        lines += bio.read().decode().splitlines()

            filenames = []
            for ext in exts:
                filenames += [f for f in namelist if f.endswith(ext)]

            for filename in filenames:
                basename = os.path.basename(filename)
                for line in lines:
                    if( line.startswith( basename ) ):
                        self.filenames.append( [zip_filename, filename, line] )
                        break

        self.filenames.sort()

        if( len(self.filenames) == 0 ):
            raise RuntimeError("Does Not Find Image Files.")

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, index):
        zip_filename = self.filenames[index][0]
        img_filename = self.filenames[index][1]
        line = self.filenames[index][2]

        if( zip_filename.endswith(".zip") ):
            with zipfile.ZipFile(zip_filename, "r") as zp:
                with zp.open(img_filename, pwd=self.pw) as f:
                    bin = io.BytesIO(f.read())
                    img_pil = Image.open( bin )

        elif( zip_filename.endswith(".7z") ):
            with py7zr.SevenZipFile(zip_filename, "r", password=self.pw.decode()) as zp:
                for _, bio in zp.read([img_filename]).items():
                    bin = io.BytesIO(bio.read())
                    img_pil = Image.open( bin )

        if( self.transform is not None ):
            img_pil = self.transform( img_pil )

        label = (line, zip_filename, img_filename)
        if( self.csv2label is not None ):
            label = self.csv2label( line, zip_filename, img_filename )

        return img_pil, label

