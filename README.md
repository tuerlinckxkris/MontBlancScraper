Create an .env file in this folder with the following structure :

`.env`
```
EMAIL_ADDRESS=<email>
EMAIL_APP_PASSWORD=<app password>

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

RECIPIENTS=<emails to send notification>
```

To run the script, first install the following packages 

```
pip install requests beautifulsoup4 python-dotenv
```

To monitor more websites add urls to the URLS parameter at the top of the script.
List of urls currently monitored :
```
URLS = [
    "https://montblanc.ffcam.fr/index.php?&_lang=GB&&_lang=GB",
    "https://montblanc.ffcam.fr/GB_home.html"
]
```

