import random
import src.data as dt
from src.variables import Variables as Var

###################### CLASSSES AND FUNCTION RELATED TO QUERIES #####################


###################### CLASSSES  #####################

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


###################### FUNCTIONS #####################
    
def assign_child(stakeholders, num):
    '''
    Randomly picks a person from list of objects and assigns attribute .haschild to True
    Args:
        stakeholders(list): list of Objects
        num(int): number of employees to have kid
    
    Returns:
        stakeholders(list): updated list of Objects

    '''

    parents = 0
    random.seed(20)

    while parents < num:
        pick = random.choice(stakeholders)

        cond1 = issubclass(pick.__class__,Employee)
 
        cond2 = pick.has_child
        
        if  cond1 and (not cond2):
            pick.has_child = True
            parents += 1
        else:
            pass

    return stakeholders



def get_score(stakeholders, param):
    '''
    Returns value of score for a given requirement
    Args:
        stakeholders(list): list of Objects
        param(str): string key to a requirement

    Returns:
        score(int): total value of that requirement based on stakeholders

    '''
    score = 0
    for stakeholder in stakeholders:
        
        if param == 'design':
            cond = stakeholder.like_design
        elif param == 'school':
            cond = stakeholder.has_child
        elif param == 'tech':
            cond = stakeholder.like_tech
        elif param == 'starbucks':
            cond = stakeholder.like_starbucks
        elif param == 'airport':
            cond = stakeholder.need_travel
        elif param == 'club':
            cond = stakeholder.like_party
        elif param == 'vegan':
            cond = stakeholder.is_vegan
        elif param == 'basket':
            cond = stakeholder.like_basket
        elif param == 'dog':
            cond = stakeholder.need_groomer
            
        else:
            pass

        if cond:
            score += stakeholder.score
        else:
            pass
        
    return score


def create_stakeholders():
    
    '''
    Creates objects based on repo description 
    Args:

    Returns:
        stakeholders(list): list of Objects

    '''

    stakeholders = []
    #this could be parametrized in future
    number_stakeholders ={'Ceo': 1, 'Executive': 10, 'Account': 20, 'Developer': 15, 'Engineer': 20, 'Designer': 20, 'Bluecollar': 1, 'Dog': 1}

    for key, value in number_stakeholders.items():
        for _ in range(value):
            
            if key == 'Ceo':
                tmp = Ceo()
            elif key == 'Executive':
                tmp = Executive()
            elif key == 'Account':
                tmp = Account()
            elif key == 'Developer':
                tmp = Developer()
            elif key == 'Engineer':
                tmp = Engineer()
            elif key == 'Designer':
                tmp = Designer()
            elif key == 'Bluecollar':
                tmp = Bluecollar()
            elif key == 'Dog':
                tmp = Dog()
    
            stakeholders.append(tmp)

    return stakeholders




def get_all_scores(df, stakeholders):
    '''
    Based on fulfillment of requirement for each candidate given in a Dataframe, assigns scores for each requirement to each candidate
    Args:
        df(DataFrame): dataframe with number of matches per requirement
        stakeholders(list): list of Objects
    
    Returns:
        df_score(DataFrame): dataframe with all scores per requirement per candidate and total score


    '''

    df_score = df[['_id','name', 'location']].copy()

    df_score['design_score'] = df['Design company'].apply(lambda x: get_score(stakeholders,'design') if x > 0 else 0)

    df_score['school_score'] = df['preschools'].apply(lambda x: get_score(stakeholders,'school') if x > 0 else 0)

    threshold = df.tech_startup.quantile(0.75)

    df_score['tech_score'] = df['tech_startup'].apply(lambda x: get_score(stakeholders,'tech') if x >= threshold else 0)

    df_score['starbucks_score'] = df['Starbucks'].apply(lambda x: get_score(stakeholders,'starbucks') if x > 0 else 0)

    df_score['airport_score'] = df.apply(lambda x: dt.score_travel(x,Var.IDEAL_TIME_CAR, Var.IDEAL_TIME_TRANSPORT,Var.PRC_PEN_MIN,stakeholders), axis = 1)

    df_score['party_score'] = df['night_club'].apply(lambda x: get_score(stakeholders,'club') if x > 0 else 0)

    df_score['vegan_score'] = df['vegan_rest'].apply(lambda x: get_score(stakeholders,'vegan') if x > 0 else 0)

    df_score['basket_score'] = df['basket_stadium'].apply(lambda x: get_score(stakeholders,'basket') if x > 0 else 0)

    df_score['dog_score'] = df['pet groomer'].apply(lambda x: get_score(stakeholders,'dog') if x > 0 else 0)

    df_score['total'] = df_score['design_score']+df_score['school_score']+df_score['tech_score']+df_score['starbucks_score']+df_score['airport_score']+df_score['party_score']+df_score['vegan_score']+df_score['basket_score']+df_score['dog_score']

    df_score = df_score.sort_values('total', ascending = False)

    return df_score












