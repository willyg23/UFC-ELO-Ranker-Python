class FightEntity:
    def __init__(self, fight_id=None, r_fighter_string=None, b_fighter_string=None,
                 winner=None, draw=None, finish=None, r_odds=None, b_odds=None,
                 r_age=None, b_age=None, b_fighter_entity=None, r_fighter_entity=None,
                 weight_class=None, year=None, month=None, day=None):

        self.fight_id = fight_id
        self.r_fighter_string = r_fighter_string
        self.b_fighter_string = b_fighter_string
        self.winner = winner
        self.draw = draw 
        self.finish = finish  
        self.r_odds = r_odds
        self.b_odds = b_odds
        self.r_age = r_age
        self.b_age = b_age
        self.b_fighter_entity = b_fighter_entity
        self.r_fighter_entity = r_fighter_entity
        self.weight_class = weight_class
        self.year = year
        self.month = month
        self.day = day
