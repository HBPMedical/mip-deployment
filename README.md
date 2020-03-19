# MIP-LOCAL Deployment Guide

## Introduction

The main objective of this pack is to provide you with the information and guidance needed to successfully install MIP.

This pack contains two sets of metadata and data for the following medical conditions:
  - Dementia
  - Trauma Brain Injury

This pack does not contain the data pre-processing tools (Data Factory) that are used to prepare your data and metadata.

### How to add Custom Data

You can follow this <a href="./documentation/NewDataRequirements.md">guide</a>.

## System Requirements

The server must be set up according to the MIP Technical Requirements and must be in a clean state.

It should also have:
  - git
  - docker (tested using version 17.05.0-ce)
  - docker-compose (tested using version 1.17.0)

The iptables config should have the following configuration (for ports 80 and 8095)
```
Input:
-A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
-A INPUT -p tcp -m tcp --sport 80 -j ACCEPT
Output:
-Α OUTPUT -p tcp -m tcp --dport 80 -j ACCEPT
-A OUTPUT -p tcp -m tcp --sport 80 -j ACCEPT

Input:
-A INPUT -p tcp -m tcp --dport 8095 -j ACCEPT
-A INPUT -p tcp -m tcp --sport 8095 -j ACCEPT
Output:
-Α OUTPUT -p tcp -m tcp --dport 8095 -j ACCEPT
-A OUTPUT -p tcp -m tcp --sport 8095 -j ACCEPT
```

## Deploy

Clone this repository.
Execute `sudo ./run.sh` script to install all the components.

## Test

After the installation is done, MIP will be visible on localhost. To verify everything is working properly go to http://localhost and
  - Check that 2 medical conditions (dementia and TBI) are visible,
  - and that 5 datasets are accessible (4 in dementia and 1 in TBI).

You can login with the default user:
```
username: user
password: password
```



If everything is working properly you should configure the users following this <a href="./documentation/UsersConfiguration.md">guide</a>.

Enjoy!

