## upylib
- uki's python library

### install
1. install user
```bash
python3 setup.py install --user --prefix=
```

2. install permanant
```bash
sudo pip3 install upylib --upgrade
```

3. manual
```bash
sudo rm -rf /usr/lib/python3/dist-packages/upylib*
sudo pip install --target=/usr/lib/python3/dist-packages .
````


### uninstall

1. uninstall permanant
```bash
sudo python3 -m pip uninstall upylib
```

2. manual
```bash
sudo rm -rf /usr/lib/python3/dist-packages/upylib*
```

### pipy
- upload.sh 참조