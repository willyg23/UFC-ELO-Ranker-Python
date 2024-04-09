import math

class EloCalculator:
  """
  Notes:

  gameResult == 1.0  // win
  gameResult == 0.5  // draw
  gameResult == 0.0  // loss
  fighterElo is the elo of who the function is currently be appplied to, not their opponent

  winnerEntity.elo![winnerEntity.elo!.length - 1]
  and
  loserEntity.elo![loserEntity.elo!.length - 1]
  both get the most recent elo rating that the fighter has had
  """

  def __init__(self):
      # You might want to initialize your fighterHashMap here, if you're 
      # keeping that concept.
      pass

  # pretty sure this currently doesn't work properly. becuase we don't check to see what manner the fight was won in.
  # so you could get a knockout win, but if subModifier was set to 5.0, the winner would still get sub bonus. and actually I think the loser does too.
  def calculateNewRating(self, gameResult, expectedScore, kFactor, fighterElo, fighter, modifierList):
      """Calculates a new Elo rating.

      Args:
          gameResult (float): 1.0 for win, 0.5 for draw, 0.0 for loss.
          expectedScore (float): The expected score of the fighter.
          kFactor (float): The K-factor for the Elo calculation.
          fighterElo (int): The fighter's current Elo rating.
          fighter (FighterEntity): The fighter entity.
          modifierList (list[float]): Modifiers for specific fight outcomes.

      Returns:
          int: The new Elo rating.
      """

      newRating = fighterElo + (kFactor * (gameResult - expectedScore)).toInt()

      # even with subInput (in main) set to 1.0, it still seems to have way to much of an impact for my math / logic to be correct. as it increases all the top ranking by ~300 elo. can't tell how accurate.
      # expected charles oliveira to be #1, but the top 3 is Donald Cerrone, Dustin Poirier, and Charles Oliveira. Which is plausible I guess? More concerned about the +300 in elo for almost everyone. that seems wrong.
      # and brev how tf is donald cerrone the goat.
      for item in modifierList:

          # need to check if the item is null. if it is, we set it to 1.0
          if item is None:
              newRating = newRating  # I think this is redundant

          else:
              # use fighter elo instead of newRating. because we want a % increase on the math that is occuring on their old rating. applying it to their new rating would give them a bigger buff that isn't accurate.
              newRating += (fighterElo * (item / 100)).toInt()  # /100 is so that users can input "5" and have a modifier of 5 percent

      return newRating

  def getExpectedScore(self, opponentRating, fighterElo):
      """Calculates the expected score for a fighter.

      Args:
          opponentRating (int): The opponent's Elo rating.
          fighterElo (int): The fighter's Elo rating.

      Returns:
          float: The expected score.
      """

      return 1.0 / (1.0 + math.pow(10.0, ((opponentRating - fighterElo) / 400.0)))
  

  
  def setNewRating(self, winner, r_fighter, b_fighter, fighterHashMap, modifierList, dateOfFight):
      """
      Sets new Elo ratings for winner and loser.

      Args:
          winner (str): "Red" or "Blue" indicating the winner.
          r_fighter (str): The name of the red fighter.
          b_fighter (str): The name of the blue fighter.
          fighterHashMap (dict): A dictionary mapping fighter names to FighterEntity objects.
          modifierList (list[float]): Modifiers for specific fight outcomes.
          dateOfFight (str): The date of the fight.
      """

      kFactor = 20.0
      expectedScore = 0.0
      winnerNewRating = 0
      loserNewRating = 0

      # Determine winner and loser strings
      winnerStr = r_fighter if winner == "Red" else b_fighter
      loserStr = b_fighter if winner == "Red" else r_fighter

      # Strings for fighterEloHashMap keys
      winnerEloHashMapString = f"{winnerStr}-{dateOfFight}"
      loserEloHashMapString = f"{loserStr}-{dateOfFight}"

      # Retrieve fighter entities
      winnerEntity = fighterHashMap[winnerStr]
      loserEntity = fighterHashMap[loserStr]

      # Update records
      winnerEntity.wins = (winnerEntity.wins or 0) + 1 
      loserEntity.losses = (loserEntity.losses or 0) + 1   
      fighterHashMap[winnerStr] = winnerEntity
      fighterHashMap[loserStr] = loserEntity

      # Setting new rating for winner
      kFactor = 15.0 if winnerEntity.elo[-1] > 2500 else 20.0  # Access the last Elo
      expectedScore = self.getExpectedScore(loserEntity.elo[-1], winnerEntity.elo[-1])
      winnerNewRating = self.calculateNewRating(1.0, expectedScore, kFactor, winnerEntity.elo[-1], winnerEntity, modifierList)

      # Setting new rating for loser
      kFactor = 15.0 if loserEntity.elo[-1] > 2500 else 20.0  # Access the last Elo 
      expectedScore = self.getExpectedScore(winnerEntity.elo[-1], loserEntity.elo[-1])
      loserNewRating = self.calculateNewRating(0.0, expectedScore, kFactor, loserEntity.elo[-1], loserEntity, modifierList)

      # Add new ratings and update fighterEloHashMap
      winnerEntity.elo.append(winnerNewRating)
      loserEntity.elo.append(loserNewRating)
      winnerEntity.fighterEloHashMap[winnerEloHashMapString] = winnerNewRating
      loserEntity.fighterEloHashMap[loserEloHashMapString] = loserNewRating
