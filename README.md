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

```python -m venv .venv```

Activate Environment:                  Windows                  If error occurs due to execution policy

```. .venv/bin/activate```   ``` .venv/Scripts/activate```    ```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser```

Install Requirements (if needed):

```pip install -r requirements.txt```

Initialise Database: 

```flask db init```                                If error occurs (start from ```flask db init```  after making new directory in migration```

```flask db migrate -m "Initial migration"```    ```Remove-Item -Recurse -Force migrations```  ----> ```mkdir migrations```

Create tables:

```flask db upgrade```

Run Server:

```flask run```

## How to run the tests for the application
