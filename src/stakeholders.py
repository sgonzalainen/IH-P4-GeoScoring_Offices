from random import choice

class Stakeholder():

    #let's initialize all attributes as False to assign all clases this
    has_child = False
    is_vegan = False
    like_starbucks = False
    need_travel = False
    like_tech = False
    like_design = False
    like_basket = False
    like_party = False
    need_groomer = False


class Employee(Stakeholder):
    def __init__(self):
        super().__init__()

    like_party = True


class Ceo(Employee):

    is_vegan = True
    score = 100

    def __init__(self):
        super().__init__()




class Executive(Employee):

    like_starbucks = True
    score = 50

    def __init__(self):
        super().__init__()




class Account(Employee):
    score = 25
    need_travel = True

    def __init__(self):
        super().__init__()


class Whitecollar(Employee):
    score = 15

    def __init__(self):
        super().__init__()

class Developer(Whitecollar):

    like_tech = True

    def __init__(self):
        super().__init__()



class Engineer(Whitecollar):
    def __init__(self):
        super().__init__()



class Designer(Whitecollar):

    like_design = True

    def __init__(self):
        super().__init__()


class Bluecollar(Employee):
    score = 10
    like_basket = True

    def __init__(self):
        super().__init__()

class Dog(Stakeholder):
    score = 5
    need_groomer = True

    def __init__(self):
        super().__init__()


    
def assign_child(stakeholders, num):

    parents = 0

    while parents < num:
        pick = choice(stakeholders)

        cond1 = issubclass(pick.__class__,Employee)
 
        cond2 = pick.has_child
        
        if  cond1 and (not cond2):
            pick.has_child = True
            parents += 1
        else:
            pass

    return stakeholders











CEO_NUM = 1
CEO_SCORE = 100
EXECUTIVES_NUM = 10
EXECUTIVES_SCORE = 50
ACCOUNT_MAN_NUM = 20
ACCOUNT_MAN_SCORE = 25