from passlib.context import CryptContext

#To tell the passLib library which algorithm we are using such as bcrypt in this case
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hash(password : str) :
    return pwd_context.hash(password)

def verify_pswd(plain_pswd, hashed_pswd) :
    return pwd_context.verify(plain_pswd,hashed_pswd) 