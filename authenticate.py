users = {'admin': 'admin'}


def check_user(usr, pwd):
    usr = usr.lower()
    for user in users.items():
        if user[0] == usr and user[1] == pwd:
            return True, user[0]
    else:
        return False, 0
