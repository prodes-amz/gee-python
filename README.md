<img src="pics/google-ee.png" width="192">

# Google Earth Engine - client-side processing (gee-python)
...

**All modules available here are under construction. Therefore, many errors and malfunctions can occur.**

1. [Setting up your environment](#1-Setting-up-your-environment)
2. [Prepare your virtual environment](#2-Prepare-your-virtual-environment)
3. [Examples ](#3-Examples)
4. [TODO-list](#4-TODO-list)

# Setting up your environment

## Python version and OS
The `gee-python` was developed using Python version 3.7+, and Linux Ubuntu 20.04 focal fossa operational system. 

## Preparing your `.env` file

This library uses decoupling, which demands you to set up variables that is only presented locally, for instance, the path you want to save something, or the resources of your project. In summary, your environment variables. So, copy a paste the file `.env-example` and rename it to `.env`. Afterwards, just fill out each of the variables content within the file:

```
DL_DATASET=PATH_TO_MAIN_DATA_FOLDER
```

# Prepare your virtual environment
First of all, check if you have installed the libraries needed:
```
sudo apt-get install python3-env
```
then, in the
```
python -m venv .venv
```
and activates it:
```
source .venv/bin/activate
```
as soon you have it done, you are ready to install the requirements.

## Installing `requirements.txt`
```
pip install -r requirements.txt
```

## Google account and credentials


# Examples 
...

# TODO-list
Well, this source-code is being released only for personal tests, but also to help out who probably has similar needs. For this reason, we have a lot to do in terms of unit tests, python conventions, optimization issues, refactoring, so on! So, Feel free to use and any recommendation will be totally welcome! 

```
-- unittests of most of the procedures:
-- ...
```

**Enjoy it!**  





