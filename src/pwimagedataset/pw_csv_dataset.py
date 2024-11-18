# mtanaka@sc.e.titech.ac.jp

# https://qiita.com/kotai2003/items/a7de8adc204d5b9218d8
# https://qiita.com/fuutot/items/d29e0928d66379fad96d
# https://qiita.com/robozushi10/items/b334357244739d47f39e
# % 7z a -mx=1 -pPassDataset images.7z images/*.png

from torch.utils.data import Dataset
from PIL import Image
import zipfile
import py7zr
import csv
import io
import os


class PwCsvDataset(Dataset):
    def __init__(self, archive_filename, dir_name, csv_filename, password=""):
        self.filename = archive_filename
        self.dir_name = dir_name
        self.csv_data = []

        # convert password to bytes
        if isinstance(password, str):
            self.pw = password.encode()
        assert (isinstance(self.pw, bytes),
                "Password must be a string or bytes.")

        # load csv file
        if (self.filename.endswith(".zip")):
            with zipfile.ZipFile(self.filename, "r") as zp:
                # check password
                try:
                    with zp.open(zp.namelist()[0], pwd=self.pw) as f:
                        dummy = f.read()
                except RuntimeError:
                    raise RuntimeError("Wrong Password.")

                # read csv file
                with zp.open(os.path.join(self.dir_name, csv_filename), pwd=self.pw) as f:
                    reader = csv.DictReader(io.TextIOWrapper(f, "utf-8"))
                    for d in reader:
                        self.csv_data.append(d)
        elif (self.filename.endswith(".7z")):
            with py7zr.SevenZipFile(self.filename, "r", password=self.pw.decode()) as zp:

                # check password
                # try:
                #     zp.read([zp.getnames()[0]])
                # except Exception as e:
                #     raise RuntimeError("Wrong Password.")


                # read csv file
                for _, bio in zp.read([os.path.join(self.dir_name, csv_filename)]).items():
                    reader = csv.DictReader(io.TextIOWrapper(bio, "utf-8"))
                    for d in reader:
                        self.csv_data.append(d)

    def __len__(self):
        return len(self.csv_data)

    def __getitem__(self, index):
        img_path = ""
        for key, value in self.csv_data[index].items():
            if value.lower().endswith(".png") or value.lower().endswith(".jpg"):
                img_path = value
                break

        img_path = os.path.join(self.dir_name, img_path)
        return self.get_image(img_path), self.csv_data[index]

    def get_image(self, file_path, format="RGB"):
        img_pil = None
        if (self.filename.endswith(".zip")):
            with zipfile.ZipFile(self.filename, "r") as zp:
                with zp.open(file_path, pwd=self.pw) as f:
                    bin = io.BytesIO(f.read())
                    img_pil = Image.open(bin)
        elif (self.filename.endswith(".7z")):
            with py7zr.SevenZipFile(self.filename, "r", password=self.pw.decode()) as zp:
                for _, bio in zp.read([file_path]).items():
                    bin = io.BytesIO(bio.read())
                    img_pil = Image.open(bin)
        return img_pil
