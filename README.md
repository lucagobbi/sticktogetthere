# sticktogetthere
An Ethereum Dapp for fundraising written in Django, Solidity and Web3.py

### What is it?
Stick To Get There is a platform written in Django that implements a smart contract through Web3.py for the back-end and some Web3.js in the front-end.
The smart contract is built to implement a fundraising system to collect funds, then propose spending requests that can be allowed only by contributors.

The admin is launching the platform setting his/her account as head account, this will be the only one allowed to create new projects, or, in other words, new contracts.
All the interactions between users and the platform is happening via blockchain and they can communicate with the platform through front-end UI which exploits Web3.js and Metamask, no data are stored locally in DB.

The admin can create a project describing the cause, setting an amount to raise and a deadline for the campaign. Once the project is sent, a new smart contract is deployed on the blockchain and available on the platform. Users can search for this project and contribute for the cause. The admin can also create spending requests which can be completed only if contributors have reached consensus on that, implenting a voting system via blockchain. Once consensus is reached the admin can effectively spend those funds.

### Setting up the environment
Once you have downloaded the source code from Github you should create a virtual environment to launch the website locally. 

Be sure you have Python installed in your machine, this project is built with Python 3.9.5

In your workspace run this command to create a new venv:

```
python -m venv venv
```

Be sure to activate your venv to install there all the requirements, on Windows using PowerShell:

```
path\to\venv\Scripts\Activate.ps1
```

Once you're working in the venv, install there all the requirements:

```
pip install -r path/to/requirements.txt
```

Now, before launching Django, you have to change some paramters in the code to make it work in your environment.
Go to fundraising/utils.py and set paramters of web3.py to work with your blockchain provider. If you are working with Ganache be sure to change the following parameters with the ones in your Ganache workspace:

```
provider = "***RPC_server***"
chain_Id = "***network_id***"
```

Change the value of my_address and private_key to set your admin account (I picked up the first one in my Ganache workspace):

```
my_address = "***admin_address***"
private_key = "***admin_private_key***"
```

Now you should be able to start Django calling these commands:

```
python manage.py makemigrations
python manage.py migrate
```

Create a superuser from CLI, this will be your admin account.
Run this command and follow all the steps to create a new user:

```
python manage.py createsuperuser
```

Well, it's done. You should now be able to launch the server running:

```
python manage.py runserver
```

### Using the platform

The UI inside the platform is very user-friendly. If you are logged in as admin you can create new project: open new project within the dropdown under the username, follow the steps to create a new project and send it.
You should now be able to see the project in projects. Users can contribute and vote totrequests interacting with the related contract via blockchain. Have fun!

### Testing with Brownie

This project also include a brownie directory built with the Brownie development and testing framework which includes some tests of the Fundraising smart contract. I could write all the project using Brownie, simplifying various steps instead of using Web3.py; however, for learning purposes, I decided to develop this project through raw Web3.py.

Once you are in the brownie directory simply call:

```
brownie test
```
If tests are passed the contract is working as expected.

### License

GPL-3.0-or-later

#

Thank you for being patient till here and let me know if I can make any improvements!

