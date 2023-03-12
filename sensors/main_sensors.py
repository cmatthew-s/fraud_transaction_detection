
import Account as acc
import Data as data
import os
from js import alert, document, console
from pyodide import create_proxy

account = acc.Account()
dt = data.Data()

login = dt.read_all_text('./login.txt')
Element('templates').write(login)

def check_path():
    files = os.listdir('.')
    for file in files:
        console.log(file)

def check_inputs(event):

    email = Element('email').value
    password = Element('password').value
    role = Element('role').value

    if email != '' and password != '' and role != '':
        
        user_data = {
            'email': email,
            'password': password,
            'role': role
        }

        is_exist = account.check_accounts('./data_account.db', user_data)

        if is_exist:
            
            if role == 'Machine Learning Developer':   
                mldev = dt.read_all_text('./mldev.txt')
                Element('templates').write(mldev)
                nav_setup()
                log_setup()
                ml_setup()
                # check_path()
                # setup()

            elif role == 'Data Management':
                data_management = dt.read_all_text('./datamanagement.txt')
                Element('templates').write(data_management)
                nav_setup()
                log_setup()

            elif role == 'Product Owner':
                product_owner = dt.read_all_text('./productowner.txt')
                Element('templates').write(product_owner)
                nav_setup()
                log_setup()
                owner_setup()

            elif role == 'Trainned Specialist':
                specialist = dt.read_all_text('./specialist.txt')
                Element('templates').write(specialist)
                nav_setup()
                log_setup()
                specialist_setup()
        
        else: 
            alert('User is not registered! ')
    
    else:
        alert('Please Fill in the forms')

def setup():
    element = document.getElementById('submit')
    submit = create_proxy(check_inputs)

    element.addEventListener('click', submit)
    check_path()

setup()