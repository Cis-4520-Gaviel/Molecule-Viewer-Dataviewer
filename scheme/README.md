# Multi-user Searchable Encryption: The SQL

## CIS\*4520 Course Project

### Gavin and Daniel

## Initializing

Built on Ubuntu 22.04.3 LTS

Libraries used

- [cryptography](https://pypi.org/project/cryptography/)
- [pymcl](https://github.com/Jemtaly/pymcl)
- [termcolor](https://pypi.org/project/termcolor/)
- sqlite3

### Installing pymcl

Clone the [pymcl repository](https://github.com/Jemtaly/pymcl)

If you are using WSL, you will need to run this command to fix ldconfig.

```bash
cd /usr/lib/wsl/lib
sudo rm libcuda.so
sudo rm libcuda.so.1
sudo ln -s libcuda.so.1.1 libcuda.so
sudo ln -s libcuda.so.1.1 libcuda.so.1
```

Then navigate to pypbc and run

```
sudo pip3 install .
```

## Running the Gaviel scheme

In the \scheme folder, run SchemeTest.py

```bash
python3 SchemeTest.py
```

This will run and initialize the entire scheme.
