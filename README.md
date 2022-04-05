"# LITReview" 

# How to run the site on a local environment (Example of Python 3) :


Extract the repository's files in a folder of your choosing

### Setup the virtual environment :


In your command bash/shell go in the folder containing the files

Type :  
Windows :
```
py -m venv env
```
Unix/mac :
```
python3 -m venv env
```


You then need to activate the virtual environment :  
Windows :
```
.\env\Scripts\activate
```
Unix/mac :  
```
source env/bin/activate
```
(venv) should now be displayed to the left of your command line :
```
(venv) C:\>
```

### Install the libraries required to run the script :

In the virtual environment (command bash/shell) type : 
```
pip(3) install -r requirements.txt
```



You can now run the server (still in the virtual environment) :  

```
(python3) manage.py runserver

```

The site will be accessible at the following URL : http://localhost:8000