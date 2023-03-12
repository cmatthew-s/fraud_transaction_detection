
import Data as dt

class Account():

    def __init__(self):
        self.data = dt.Data()

    def check_accounts(self, database, user_data):
        isCheck = self.data.get_login_info(database, user_data)

        if isCheck:
            return True

        else:
            return False

