# Device Management Project 
This application has been designed to offer device management functionality. 

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)

## Overview
This application has been built using Django and deployed on Heroku.

## Features
This section will describe the features available:

### Standard Features
- Register for an account
- Log into an existing account

### Basic User Features 
Users can take the following actions. 
- View current assignments
- Propose an edit to the assignment
- Request the assignment is deleted.

The proposal and request functionality is an example of soft CRUD, storing the request and moving it into an approval flow for administrators. 
![image](https://github.com/user-attachments/assets/d07a5564-1ace-4d52-9b7a-3f27e8b4cfd5)


### Staff User Features 
Staff users can complete the following actions.

- View all / edit / delete assignments for all users(highlighted assignments indicate a pending change)
![image](https://github.com/user-attachments/assets/2e280485-abda-4603-ab70-f94a9d3e1dd9)

- View proposed edits and requested deletions of all assignments, either approving or denying the changes
![image](https://github.com/user-attachments/assets/f10b17d3-e3ea-4db9-86a3-ea25934b26d8)
![image](https://github.com/user-attachments/assets/cddb698f-8b0b-4022-8664-63270559a50b)



- View all / edit / delete  devices
![image](https://github.com/user-attachments/assets/823ab80c-28e4-46fd-bf7f-f8c90748a158)
![image](https://github.com/user-attachments/assets/e8cf9c0f-9126-4d1e-827c-9dd42a8bf368)



