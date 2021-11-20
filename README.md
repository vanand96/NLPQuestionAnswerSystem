# NLP Question Answer System
This application will display the real estate housing information. If the user has any questions it will display the answers using the BERT model

## Python packages
* The following python packages needs to be installed before running this
    * pip install webdriver-manager
    * pip install bs4
    * pip install requests
    * pip install selenium
    * pip install wget
    * pip install pandas
    * pip install django
    * pip install tensorflow==1.13.0rc1
    * pip install python-Levenshtein
    * pip install statsmodel
    * pip install sklearn
    
## The following commands needs to be run to start the server, bert model
* python manage.py runserver
* python manage.py startapp bert
* bert-serving-start -model_dir cased_L-12_H-768_A-12 -num_worker=4 -max_seq_len=75
