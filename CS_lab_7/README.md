# Lab 7: Database Security

>The main goal of this lab work is to configure a MongoDB database so that it can store sensitive data securely.
First I pre-populated a MongoDB database with some data. Some of the data kept in the database should be considered 
sensitive (e.g. a user’s email), hence it needs to be encrypted via 2-way encryption. After populating and 
securing the database, I created an app that is be able to access the database and output on screen the 
decrypted version of the data stored.

### Required features:

- Create a MongoDB database which would contain some secured sensitive data (protected
via 2-way encryption);
- Create an application which would display the data contained in the database (both
common data and the decrypted sensitive data);
- Make sure that the sensitive data can only be accessed via your application (i.e. it is
secure).


### Used Technologies:

- Windows 10 
- Python
- Mongodb Enterprise
- OpenSSL


### Instructions:
**1. Run "mongod" and "mongocryptd" locally(requires MongoDB enterprise):**

**2. Create a local master key in the environment for testing**
*(it needs to be a 96 byte base64 encoded value, this could be generated with openssl):*

```
export LOCAL_MASTER_KEY="$(openssl rand -base64 96 | tr -d '\n')"
```

**3. Run "create_key.py" to generate a data key stored in the db.key_vault:**
```
python create_key.py
```

**4. Run "get_data.py" to populate the db.data and print results:**
```
python get_data.py
```
