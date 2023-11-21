Title - Expense Split system

This is expense split system that split expense between friends. 

Note - Except login all api require you to provide token in header

following are the api  end points and request response samples-

1) Login

url - http://127.0.0.1:8000/api/login/

Request - 

username:anju123
password:anju

Response:

{
    "token": "433e6f8ce8b3d3daf8710571326a6176ea2abca8"
}

2) Create Expense-

url - http://127.0.0.1:8000/api/expense/

Request:
{
    "split_type":"EXACT",
    "total_amount":100,
    "note":"light bill",
    "split":[{"user":"anju123","amt":200}]
}


Response:
{
    "status": "success",
    "message": "success"
}


3) Owns api 

url - http://127.0.0.1:8000/api/owns/

Response - 

{
    "data": [
        {
            "id": 7,
            "Debtor": 1,
            "Creditor": 4,
            "Debtor_username": "sanket",
            "Creditor_username": "anju123",
            "amount": 250.0,
            "simplified_amount": null
        }
    ]
}

4) Simplify 

url - http://127.0.0.1:8000/api/simplify/

Response: 
{
    "message": "Success"
}



