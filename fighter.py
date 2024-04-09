class FighterEntity():
    def __init__(self, name=None, weight_classes=None, weight_class_rank=None,  
                 gender=None, current_win_streak=None, current_loss_streak=None,
                 avg_SIG_STR_landed=None, avg_SIG_STR_pct=None, avg_SUB_ATT=None,
                 avg_TD_landed=None, avg_TD_pct=None, total_rounds_fought=None,
                 total_title_bouts=None, wins_by_Decision_Majority=None, 
                 wins_by_Decision_Split=None, wins_by_Decision_Unanimous=None, 
                 wins_by_KO=None, wins_by_Submission=None, wins_by_TKO_Doctor_Stoppage=None,
                 height_cms=None, reach_cms=None, elo=None, fight_history=None, 
                 stance=None, wins=None, age=None, losses=None, fighterId=None):
        
        self.name = name
        self.weight_classes = weight_classes or []
        self.weight_class_rank = weight_class_rank or []
        self.gender = gender
        self.current_win_streak = current_win_streak
        self.current_loss_streak = current_loss_streak
        self.avg_SIG_STR_landed = avg_SIG_STR_landed
        self.avg_SIG_STR_pct = avg_SIG_STR_pct
        self.avg_SUB_ATT = avg_SUB_ATT
        self.avg_TD_landed = avg_TD_landed
        self.avg_TD_pct = avg_TD_pct
        self.total_rounds_fought = total_rounds_fought
        self.total_title_bouts = total_title_bouts
        self.wins_by_Decision_Majority = wins_by_Decision_Majority
        self.wins_by_Decision_Split = wins_by_Decision_Split
        self.wins_by_Decision_Unanimous = wins_by_Decision_Unanimous
        self.wins_by_KO = wins_by_KO
        self.wins_by_Submission = wins_by_Submission
        self.wins_by_TKO_Doctor_Stoppage = wins_by_TKO_Doctor_Stoppage
        self.height_cms = height_cms
        self.reach_cms = reach_cms
        self.elo = elo or []
        self.fighterEloHashMap = {}
        self.fight_history = fight_history or []
        self.stance = stance
        self.wins = wins
        self.age = age
        self.losses = losses
        self.fighterId = fighterId
