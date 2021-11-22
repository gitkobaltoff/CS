# Lab 6: SSO Security

>The main goal of this lab work is to develop an application to 
analyze the sensitive data that is sent to applications when using SSO.
Using SSO in an application represents a secure alternative to classical authentication using
login + passwords. On one hand it makes the life of the user much easier because they don’t need
to remember yet another password. On the other hand, the security savvy users can get worried
about what data is sent when using such logging systems. 

### Required features:

- Offer user authentication via SSO using at least 3 identity providers (e.g. Facebook,
Gmail, Twitter etc.);
- Configure SSO integration to get as much as possible data about the end-user;
- Output all data which was provided by the identity providers (e.g. user’s name, age,
gender, email etc.).

### Used Technologies:

- Windows 10 
- Python
- Flask

### Instructions:
**1. Install libraries from requirements.txt.**

**2. Fill data.env file with personal credentials:**

**Run server:**
```
python sso_server.py
```
