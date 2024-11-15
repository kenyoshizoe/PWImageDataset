from pwimagedataset import PwCsvDataset

import random

if __name__ == "__main__":
    # print("Enter password for zipfile [PassDataset]:")
    # pw = getpass.getpass()  # PassDataset
    pw = "PassDataset"

    datasets = [
        PwCsvDataset("dataset.zip", "dataset", "label.csv", pw),
        PwCsvDataset("dataset.7z", "dataset", "label.csv", pw)
    ]

    for dataset in datasets:
        idx = random.randint(0, len(dataset)-1)
        img_pil, label = dataset[idx]

        print(img_pil.size)
        print(label)
