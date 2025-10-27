import pytest
import jwt
from app import schemas

from app.config import settings

# def test_root(client) :
#     res = client.get("/")
#     # print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World!'
#     assert res.status_code == 200



def test_create_user(client) :
    res = client.post("/users/", json={"email":"hello123@gmail.com","password":"pswd123"})
    #print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'hello123@gmail.com'
    assert res.status_code == 201

def test_login_user(client,test_user) :
    res = client.post("/login", data={"username":test_user['email'],"password":test_user['password']}) 
    #print(res.status_code)
    #print(res.text)
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200



@pytest.mark.parametrize("email,password,status_code",[
    ('menashi30@gmail.com','wrongPswd',403),
    ('wrongEmail@gmail.com','pswd123',403),
    ('wrongEmail@gmail.com','wrongPswd',403)
])
def test_incorrect_login(client,test_user,email,password,status_code) :
    res = client.post("/login/",data = {"username" :email,"password":password})
    
    #assert res.json().get('detail') == "Invalid Credentials"
    assert res.status_code == status_code

def test_none_username_login(client,test_user2) : 
    res = client.post("/login/",data = {"password":test_user2['password']})
    
    #assert res.json().get('detail') == "Invalid Credentials"
    assert res.status_code == 422

def test_none_password_login(client,test_user2) : 
    res = client.post("/login/",data = {"username":test_user2['email']})
    
    #assert res.json().get('detail') == "Invalid Credentials"
    assert res.status_code == 422

