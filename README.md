# CITS3403
## Purpose of the application

### Design

### Use

## Team Members
| UWA ID | Name | Github Username |
| --------------- | --------------- | --------------- |
| 22848932 | Celyn Chew | CelynChew |
| 23641633  | Chuen Yui Lam  | Roy-Lam  |
| 23251142  | Benjamin Cooper | bc163836 |
|  |  |  |

## Architecture of the application

## How to launch the application
Create Virtual Environment:

```python3 -m venv .venv```

Activate Environment:                              

Mac ```. .venv/bin/activate```   

Windows ``` .venv/Scripts/activate```     IF ERROR ```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser```

Install Requirements (if needed):

```pip install -r requirements.txt```

Initialise Database: 

```flask db init```                                

```flask db migrate -m "Initial migration"```  

If error occurs (start from ```flask db init```  after making new directory in migration)
```Remove-Item -Recurse -Force migrations```
```mkdir migrations```

Create tables:

```flask db upgrade```

Run Server:

```flask run```

For mobile:

1. Connect your laptop to your phone's mobile hotspot
2. Run ```flask run --host=0.0.0.0``` and use the second link. 
## How to run the tests for the application
