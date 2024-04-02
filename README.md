# Assignment 4

## Technologies

The backend was built using

- `swig3.0`
- `python3.7+`

The front end was built using

- `ReactJS`
- `node`

## Cryptosystem

Built on Ubuntu 22.04.3 LTS

- [cryptography](https://pypi.org/project/cryptography/)
- [pymcl](https://github.com/Jemtaly/pymcl)
- [otc](https://pypi.org/project/otc/)

### Installing pymcl

Configure

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

## Running

There are two sections of code that will be needed to execute to run the full stack.

### Web Server

To start the server, first run the command:

```
make
```

Then enter the command

```
python3 server.py [port]
```

where [port] is the specified port.

The intended port to use with this server is `51584`.

### Front End

To initialize the node server, you will need `node` and `npm`.

Run

```
yarn install --immutable
```

If the port you have entered to run for the webserver was not 51584, you will need to go to the `package.json` and edit the line:

```json
"proxy": "http://localhost:51584", //change 51584 to the port number
```

To start the front end, run the following command

```
yarn start
```

And it will automatically run on `localhost:3000`.

### Database Initialization

When starting the app initially, the database will be empty. To initialize the database with default element properties - which are used to make configure how each element looks - run the following command

```bash
python3 molsql.py
```

This will initialize the database with test data to use.

### Nightmare Mode

This assignment was done in nightmare mode.
The molecule has an option to continually spin.

## About

Author: Daniel Wang

ID: 1191584
