# Email Sender

### Usage
- Set Less secure app access option to ON in your google account
- Run this command to install the required library
```py
    pip install -r requirements.txt
```
- Change the constants in **email-sender.py** file as follow:
  - *SENDER_EMAIL* -> Your email to send the emails from
  - *SENDER_PASS* -> Your password
  - *SUBJECT* -> The email subject
  - *TEMPLATE_PATH* -> The file contains the email template (or put your template in the already exist file), using NAME and LINK as place holders
  - *DATA_PATH* -> The file contains the receivers data (or put your data in the already exist file)
  - *NAME_HEADER* -> The names column header in your datasheet
  - *EMAIL_HEADER* -> The emails column header in your data sheet
  - *LINK_HEADER* -> The links column header in your data sheet
- Run the script using
```py
python email-sender.py
```