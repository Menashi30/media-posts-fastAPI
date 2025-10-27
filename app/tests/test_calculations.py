import pytest
from app.calculations import add,subtract, multiply, divide,BankAccount,InsufficientFunds


@pytest.fixture
def default_bank_account() :
  print("creating an empty bank account")
  return BankAccount()

@pytest.fixture
def bank_account() :
 return BankAccount(50)

@pytest.mark.parametrize("num1,num2,expected",[
 (5,7,12),
 (1,9,10),
 (20,30,50)
])
def test_add(num1,num2,expected) :
 print ("testing add function")
 assert add(num1,num2) == expected

def test_subtract() :
 assert subtract(9,5) == 4

def test_multiply() :
 assert multiply(3,2) == 6

def test_divide() :
 assert divide(20,5) == 4


def test_bank_set_initial_amount(bank_account) :
#bank_account = BankAccount(50)
 assert bank_account.balance == 50

def test_bank_default_value(default_bank_account) :
 print("testing bank account set to default value")
 #bank_account = BankAccount()
 assert default_bank_account.balance == 0

def test_withdraw(bank_account) :
 #bank_account = BankAccount(50)
 bank_account.withdraw(20)
 assert bank_account.balance == 30

def test_deposit(bank_account) :
 #bank_account = BankAccount(50)
 bank_account.deposit(30)
 assert bank_account.balance == 80

def test_collect_interest(bank_account) :
 #bank_account = BankAccount(10)
 bank_account.collect_interest()
 assert round(bank_account.balance,5) == 55


@pytest.mark.parametrize("deposited,withdrew,expected",[
 (200,100,100),
 (50,10,40),
 (1200,1000,200)
])
def test_bank_transaction(default_bank_account,deposited,withdrew,expected) :
  default_bank_account.deposit(deposited)
  default_bank_account.withdraw(withdrew)
  assert default_bank_account.balance == expected


def test_insufficient_funds(bank_account) :
 with pytest.raises(InsufficientFunds) :
  bank_account.withdraw(100)