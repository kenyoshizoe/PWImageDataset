# pPassLoader
## Install
```
# for pip
pip install git+https://github.com/kenyoshizoe/PWImageDataset.git
# for poetry
poetry add git+https://github.com/kenyoshizoe/PWImageDataset.git
# for rye
rye add pwimagedataset --git https://github.com/kenyoshizoe/PWImageDataset.git
```

## Command for making archive with password

```shell
% zip -e --password=xxxx images.zip images/*
```

```shell
% 7z a -mx=1 -pxxxx images.7z images/*
```
### References

- [ZIP](https://qiita.com/snaka/items/b84d9c56a7b5dc8fc055)
- [7Z](https://qiita.com/robozushi10/items/b334357244739d47f39e)
