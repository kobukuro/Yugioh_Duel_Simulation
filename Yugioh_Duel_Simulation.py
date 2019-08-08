import random
from random import randint
import threading
import time
from operator import attrgetter
class Card():
    __type = ''
class MonsterCard(Card):
    __type = 'Monster'
    __subType = ''
    __name = ''
    __levelNum = 0
    __attackValue = 0
    __defenseValue = 0
    __effectList = []
    def __init__(self,name,levelNum=0,attackValue=0,defenseValue=0,effectList=[]):
        self.__name = name
        self.__levelNum = levelNum
        self.__attackValue = attackValue
        self.__defenseValue = defenseValue
        self.__effectList = effectList
    def getType(self):
        return self.__type
    def getName(self):
        return self.__name
    def getLevelNum(self):
        return self.__levelNum
    def getAttackValue(self):
        return self.__attackValue
    def getDefenseValue(self):
        return self.__defenseValue
class Effect():
    __name = ''
    __activatePhase = ''  # which phase the effect can be activated in
    def __init__(self,name,activatePhase):
        self.__name = name
        self.__activatePhase = activatePhase
    def getName(self):
        return self.__name
    def getActivatePhase(self):
        return self.__activatePhase
class Deck():
    __name = ''
    __normalCards = []
    __extraCards = []
    def __init__(self,name,normalCards,extraCards):
        self.__name = name
        self.__normalCards = normalCards
        self.__extraCards = extraCards
    def getDeckName(self):
        return self.__name
    def getNormalCards(self):
        return self.__normalCards
    def getExtraCards(self):
        return self.__extraCards
    def printNameOfNormalCards(self):
        cardNames = ''
        for card in self.__normalCards:
            cardNames += card.getName() + ', '
        print(cardNames[:-2])
            # print(card.getType()+' '+card.getName())
    def printNameOfExtraCards(self):
        cardNames = ''
        for card in self.__extraCards:
            cardNames += card.getName() + ', '
        print(cardNames[:-2])
class Player():
    def __init__(self,name):
        self.__name = name
        self.__decks = []
        self.__currDeck = 0
    def getName(self):
        return self.__name
    def getDeck(self):
        return self.__decks[self.__currDeck]
    def addDeck(self,deck:Deck):
        self.__decks.append(deck)
    # assign index of deck in use
    def changeDeckInUse(self,currDeck):
        self.__currDeck = currDeck
class Game():
    __type = ''
'''Draw Phase
Standby Phase
Main Phase 1
Battle Phase
	Start Step
	Battle Step
	Damage Step
	End Step
Main Phase 2
End Phase'''
class NormalGame(Game):
    __type = 'Normal'
    __phases = ['Draw','StandBy','Main','Battle','End']
    __whoFirst = ''
    __initLifePoints = 4000
    __initNumCardsInHand = 4
    __numGrid = 3
    __rangeOneLowerLimit = 1
    __rangeOneUpperLimit = 4
    __rangeTwoLowerLimit = 5
    __rangeTwoUpperLimit = 6
    __rangeThreeLowerLimit = 7
    __rangeThreeUpperLimit = 8
    __currentTurnNum = 1
    __currentPhaseNum = 0
    __currentPlayerIndex = 0
    __currentPlayer = ''
    __gameOver = False
    __winner = ''
    # stores information of each player
    __playersInfo = []
    # stores each part of the game
    __playerLifePoints = {}
    __playerDeck = {}
    __playerExtraDeck = {}
    __playerField = {}
    __playerGraveyard = {}
    __playerMonstersArea = {}
    __playerMagicTrapArea = {}
    __playerCardsInHand = {}
    __playerBannedArea = {}
    __playerSummonFlagThisTurn = {} # whether this player can summon monster this turn
    def __init__(self,playersInfo):
        # set turn number as turn 1
        self.__currentTurnNum = 1
        self.__currentPhaseNum = 0
        self.__playersInfo = playersInfo
        for player in self.__playersInfo:
            self.__playerLifePoints[player.getName()] = self.__initLifePoints
            # shuffle deck
            random.shuffle(player.getDeck().getNormalCards())
            self.__playerDeck[player.getName()] = player.getDeck().getNormalCards()
            # shuffle extra deck
            random.shuffle(player.getDeck().getExtraCards())
            self.__playerExtraDeck[player.getName()] = player.getDeck().getExtraCards()
            # draw cards
            self.__playerCardsInHand[player.getName()] = []  # create empty in hand
            self.__playerMonstersArea[player.getName()] = []  # create empty monster area
            self.__playerMagicTrapArea[player.getName()] = []  # create empty magic trap area
            self.__playerGraveyard[player.getName()] = []  # create empty graveyard
            for num in range(self.__initNumCardsInHand):
                self.__playerCardsInHand[player.getName()].append(self.__playerDeck[player.getName()][0])
                self.__playerDeck[player.getName()].pop(0)
        # decide who can go first
        self.__currentPlayerIndex = randint(0,len(self.__playersInfo)-1)
        self.__whoFirst = self.__playersInfo[self.__currentPlayerIndex].getName()
        self.__currentPlayer = self.__whoFirst
        lifePointsMessage = ''
        for player in self.__playersInfo:
            lifePointsMessage += player.getName() + ':' + \
                                 str(self.__playerLifePoints[player.getName()])+ ', '
        print(lifePointsMessage[:-2])
        for player in self.__playersInfo:
            print(player.getName()+': Deck: ', end='')
            print(self.getDeck(player.getName()))
            print(player.getName() + ': ExtraDeck: ', end='')
            print(self.getExtraDeck(player.getName()))
            print(player.getName() + ': CardsInHand: ', end='')
            print(self.getCardsInHand(player.getName()))
        print('WhoFirst : ' + self.__whoFirst)
    # return number of players
    def getNumPlayer(self):
        return len(self.__playersInfo)
    def getLifePoints(self,name):
        return self.__playerLifePoints[name]
    def getLifePoints(self):
        return self.__playerLifePoints
    def getDeck(self,name):
        contentCardNames = ''
        for card in self.__playerDeck[name]:
            contentCardNames += card.getName() + ', '
        return contentCardNames[:-2]
    def getExtraDeck(self,name):
        contentCardNames = ''
        for card in self.__playerExtraDeck[name]:
            contentCardNames += card.getName() + ', '
        return contentCardNames[:-2]
    def getCardObjectsInHand(self,playerName):
        return self.__playerCardsInHand[playerName]
    def getPlayersInfoObjects(self):
        return self.__playersInfo
    def getCardsInHand(self,name):
        contentCardNames = ''
        for card in self.__playerCardsInHand[name]:
            contentCardNames += card.getName() + ', '
        return contentCardNames[:-2]
    def getMonsterObjectsInMonsterArea(self,playerName):
        return self.__playerMonstersArea[playerName]
    def getCurrentPlayer(self):
        return self.__currentPlayer
    def getCurrentPhase(self):
        return self.__phases[self.__currentPhaseNum]
    def isMonsterAreaFull(self,playerName):
        answer = False
        if len(self.__playerMonstersArea[playerName]) >= self.__numGrid:
            answer = True
        return answer
    def goToNextPhase(self):
        # if current phase is not final phase
        if self.__currentPhaseNum != len(self.__phases)-1:
            # if current turn is turn one and next phase is battle phase, then skip battle phase
            if self.__currentTurnNum == 1 and self.__phases[self.__currentPhaseNum+1] == 'Battle':
                self.__currentPhaseNum += 2
            else:
                self.__currentPhaseNum += 1
        # if current phase is final phase
        else:
            self.__currentPhaseNum = 0
            self.changeCurrentPlayer()
            self.__currentTurnNum += 1
            # if there is monster at this player's monster area, then reset monsters' attack
            if len(self.__playerMonstersArea[self.getCurrentPlayer()]) != 0:
                for monster in self.__playerMonstersArea[self.getCurrentPlayer()]:
                    monster[3] = False
    def changeCurrentPlayer(self):
        if self.__currentPlayerIndex != len(self.__playersInfo)-1:
            self.__currentPlayerIndex += 1
        else:
            self.__currentPlayerIndex = 0
        self.__currentPlayer = self.__playersInfo[self.__currentPlayerIndex].getName()
    def drawCard(self,playerName,numCard):
        """
        Draw card(s)
        :param playerName: The player who draw card(s)
        :param numCard: The number of card(s) the player draws
        """
        # if the number of cards need to be drawn exceeds number of cards in deck, then game over
        if numCard > len(self.__playerDeck[playerName]):
            print(playerName + " is out of deck.")
            self.removePlayer(playerName)
            self.gameOverCheck()
        else:
            for num in range(numCard):
                self.__playerCardsInHand[playerName].append(self.__playerDeck[playerName][0])
                self.__playerDeck[playerName].pop(0)
            if numCard == 1:
                print(playerName + ' draws ' + str(numCard) + ' card.')
            else:
                print(playerName + ' draws ' + str(numCard) + ' cards.')
            print('Current ' + playerName + "'s Deck: " +self.getDeck(playerName))
            print('Current ' + playerName + "'s CardsInHand: " +self.getCardsInHand(playerName))
    def gameOverCheck(self):
        if len(self.__playersInfo) == 1:
            self.__gameOver = True
            self.__winner = self.__playersInfo[0].getName()
            print('Game Over')
            print('Winner is ' + self.__playersInfo[0].getName())
    def removePlayer(self,playerName):
        # remove this player
        indexNeedToRemove = 0
        for i in range(len(self.__playersInfo)):
            if self.__playersInfo[i].getName() == playerName:
                indexNeedToRemove = i
        self.__playersInfo.pop(indexNeedToRemove)
    def getMonsterAreaInfo(self,playerName):
        finalStr = ''
        for lst in self.__playerMonstersArea[playerName]:
            finalStr += lst[0].getName() + ' '
            for i in range(1,len(lst)):
                finalStr += str(lst[i]) + ' '
            finalStr = finalStr[:-1]
            finalStr += ', '
        return finalStr[:-2]
    def advancedSummon(self,playerName,monsterCard,tributeIndexList):
        cardsInHand = self.__playerCardsInHand[playerName]
        cardsNameInHand = []
        for card in cardsInHand:
            cardsNameInHand.append(card.getName())
        if monsterCard.getName() not in cardsNameInHand:
            raise Exception('Specified monster card does not exist in hand.')
        elif monsterCard.getLevelNum() < 5:
            raise Exception('The level of monster is less than five.')
        else:
            if 5 <= monsterCard.getLevelNum() <= 6:  # need to tribute one monster
                if len(tributeIndexList) == 0:
                    raise Exception("Didn't specify the monster need to be tributed.")
                elif len(tributeIndexList) == 1:
                    print(playerName + "'s Monster Area: " + self.getMonsterAreaInfo(playerName))
                    for i in range(len(self.__playerCardsInHand[playerName])):
                        if self.__playerCardsInHand[playerName][i].getName() == monsterCard.getName():
                            self.__playerCardsInHand[playerName].pop(i)
                            break
                    self.__playerGraveyard[playerName].append(self.__playerMonstersArea[playerName][tributeIndexList[0]][0])
                    self.__playerMonstersArea[playerName].pop(tributeIndexList[0])
                    self.__playerMonstersArea[playerName].append([])
                    self.__playerMonstersArea[playerName][-1].append(monsterCard)
                    self.__playerMonstersArea[playerName][-1].append('ATK')
                    self.__playerMonstersArea[playerName][-1].append('Front')
                    self.__playerMonstersArea[playerName][-1].append(False)
                    print(playerName + ' summons ' + monsterCard.getName() + ' successfully.')
                    print(playerName + "'s Monster Area: " + self.getMonsterAreaInfo(playerName))
                    print('Current ' + playerName + "'s CardsInHand: " + self.getCardsInHand(playerName))
                elif len(tributeIndexList) > 1:
                    raise Exception("The number of monsters need to be tributed is only one.")
            elif 7 <= monsterCard.getLevelNum() <= 8:  # need to tribute two monsters
                if len(tributeIndexList) <= 1:
                    raise Exception("The number of monsters need to be tributed is not enough.")
                elif len(tributeIndexList) == 2:
                    pass
                else:
                    raise Exception("The number of monsters need to be tributed is only two.")
    # for summoning monster whose level is less than 5
    def normalSummon(self,playerName,monsterCard):
        cardsInHand = self.__playerCardsInHand[playerName]
        cardsNameInHand = []
        for card in cardsInHand:
            cardsNameInHand.append(card.getName())
        # check if this player has the specified card in his hand
        if monsterCard.getName() not in cardsNameInHand:
            raise Exception('Specified monster card does not exist in hand.')
        elif len(self.__playerMonstersArea[playerName]) == self.__numGrid:
            raise Exception('There is no empty monster grid.')
        elif monsterCard.getLevelNum() >= 5:
            raise Exception('The level of monster is greater than four.')
        else:
            print(playerName + "'s Monster Area: " + self.getMonsterAreaInfo(playerName))
            for i in range(len(self.__playerCardsInHand[playerName])):
                if self.__playerCardsInHand[playerName][i].getName() == monsterCard.getName():
                    self.__playerCardsInHand[playerName].pop(i)
                    break
            self.__playerMonstersArea[playerName].append([])
            self.__playerMonstersArea[playerName][-1].append(monsterCard)
            self.__playerMonstersArea[playerName][-1].append('ATK')
            self.__playerMonstersArea[playerName][-1].append('Front')
            self.__playerMonstersArea[playerName][-1].append(False)  # this stands for whether executes attack or not
            print(playerName + ' summons ' + monsterCard.getName() + ' successfully.')
            print(playerName+"'s Monster Area: "+self.getMonsterAreaInfo(playerName))
            print('Current ' + playerName + "'s CardsInHand: " + self.getCardsInHand(playerName))
    def specialSummon(self,playerName,monsterCard):
        pass
    def fusionSummon(self,playerName):
        pass
    def setMonster(self,playerName,indexSelfMonsterInHand):
        card = self.getCardObjectsInHand(playerName)[indexSelfMonsterInHand]
        if card.getType() != 'Monster':
            raise Exception('The type of specified card is not monster.')
        else:
            levelOfMonster = card.getLevelNum()
            if 4 >= levelOfMonster >= 1:
                if len(self.__playerMonstersArea[playerName]) >= self.__numGrid:
                    raise Exception('There is no empty monster grid.')
                else:
                    print(playerName + "'s Monster Area: " + self.getMonsterAreaInfo(playerName))
                    self.__playerCardsInHand[playerName].pop(indexSelfMonsterInHand)
                    self.__playerMonstersArea[playerName].append([])
                    self.__playerMonstersArea[playerName][-1].append(card)
                    self.__playerMonstersArea[playerName][-1].append('DEF')
                    self.__playerMonstersArea[playerName][-1].append('Reverse')
                    self.__playerMonstersArea[playerName][-1].append(False)  # this stands for whether executes attack or not
                    print(playerName + ' sets ' + card.getName() + ' successfully.')
                    print(playerName + "'s Monster Area: " + self.getMonsterAreaInfo(playerName))
                    print('Current ' + playerName + "'s CardsInHand: " + self.getCardsInHand(playerName))
    def attackMonster(self,playerName,indexSelfMonster,targetPlayerName,indexTargetMonster):
        if self.__playerMonstersArea[playerName][indexSelfMonster][1] == 'DEF' or \
                self.__playerMonstersArea[playerName][indexSelfMonster][3]:
            raise Exception('This monster can not attack.')
        else:
            print(playerName + "'s Monster Area: " + self.getMonsterAreaInfo(playerName))
            print(targetPlayerName + "'s Monster Area: " + self.getMonsterAreaInfo(targetPlayerName))
            print(playerName+"'s ["+str(indexSelfMonster)+'] '+self.__playerMonstersArea[playerName][indexSelfMonster][0].getName() +' attacks '+
                  targetPlayerName + "'s [" + str(indexTargetMonster) + '] ' +self.__playerMonstersArea[targetPlayerName][indexTargetMonster][0].getName())
            self.__playerMonstersArea[playerName][indexSelfMonster][3] = True
            atkOfSelfMonster = self.__playerMonstersArea[playerName][indexSelfMonster][0].getAttackValue()
            targetPosition = self.__playerMonstersArea[targetPlayerName][indexTargetMonster][1]
            if targetPosition == 'ATK':
                atkOfTargetMonster = self.__playerMonstersArea[targetPlayerName][indexTargetMonster][0].getAttackValue()
                if atkOfSelfMonster > atkOfTargetMonster:
                    diff = atkOfSelfMonster - atkOfTargetMonster
                    self.__playerLifePoints[targetPlayerName] -= diff
                    print(targetPlayerName +"'s life points: "+str(self.__playerLifePoints[targetPlayerName]))
                    # target monster is moved to graveyard
                    self.__playerGraveyard[targetPlayerName].append(self.__playerMonstersArea[targetPlayerName][indexTargetMonster][0])
                    self.__playerMonstersArea[targetPlayerName].pop(indexTargetMonster)
                    print(targetPlayerName + "'s Monster Area: " + self.getMonsterAreaInfo(targetPlayerName))
                    if self.__playerLifePoints[targetPlayerName] <= 0:
                        self.removePlayer(targetPlayerName)
                        self.gameOverCheck()
                elif atkOfSelfMonster < atkOfTargetMonster:
                    diff = atkOfTargetMonster - atkOfSelfMonster
                    self.__playerLifePoints[playerName] -= diff
                    print(playerName + "'s life points: " + str(self.__playerLifePoints[playerName]))
                    # self monster is moved to graveyard
                    self.__playerGraveyard[playerName].append(
                        self.__playerMonstersArea[playerName][indexSelfMonster][0])
                    self.__playerMonstersArea[playerName].pop(indexSelfMonster)
                    print(playerName + "'s Monster Area: " + self.getMonsterAreaInfo(playerName))
                    if self.__playerLifePoints[playerName] <= 0:
                        self.removePlayer(playerName)
                        self.gameOverCheck()
                else:  # both monsters are moved to graveyard
                    self.__playerGraveyard[playerName].append(
                        self.__playerMonstersArea[playerName][indexSelfMonster][0])
                    self.__playerMonstersArea[playerName].pop(indexSelfMonster)
                    print(playerName + "'s Monster Area: " + self.getMonsterAreaInfo(playerName))
                    self.__playerGraveyard[targetPlayerName].append(
                        self.__playerMonstersArea[targetPlayerName][indexTargetMonster][0])
                    self.__playerMonstersArea[targetPlayerName].pop(indexTargetMonster)
                    print(targetPlayerName + "'s Monster Area: " + self.getMonsterAreaInfo(targetPlayerName))
            elif targetPosition == 'DEF':
                # flip up the reversed target monster
                self.__playerMonstersArea[targetPlayerName][indexTargetMonster][2] = 'Front'
                defOfTargetMonster = self.__playerMonstersArea[targetPlayerName][indexTargetMonster][0].getDefenseValue()
                if atkOfSelfMonster > defOfTargetMonster:
                    # target monster is moved to graveyard
                    self.__playerGraveyard[targetPlayerName].append(self.__playerMonstersArea[targetPlayerName][indexTargetMonster][0])
                    self.__playerMonstersArea[targetPlayerName].pop(indexTargetMonster)
                    print(targetPlayerName + "'s Monster Area: " + self.getMonsterAreaInfo(targetPlayerName))
                    # if inflict damage
                    if self.__playerLifePoints[targetPlayerName] <= 0:
                        self.removePlayer(targetPlayerName)
                        self.gameOverCheck()
                elif atkOfSelfMonster < defOfTargetMonster:
                    diff = defOfTargetMonster - atkOfSelfMonster
                    self.__playerLifePoints[playerName] -= diff
                    print(playerName + "'s life points: " + str(self.__playerLifePoints[playerName]))
                    if self.__playerLifePoints[playerName] <= 0:
                        self.removePlayer(playerName)
                        self.gameOverCheck()
                else:
                    print('ATK of '+playerName+"'s monster is equal to DEF of "+targetPlayerName+"'s monster.")
                    print(targetPlayerName + "'s Monster Area: " + self.getMonsterAreaInfo(targetPlayerName))
    def directAttack(self,playerName,indexSelfMonster,targetPlayerName):
        atkValue = self.__playerMonstersArea[playerName][indexSelfMonster][0].getAttackValue()
        self.__playerLifePoints[targetPlayerName] -= atkValue
        print(playerName +"'s ["+str(indexSelfMonster)+"] "+
              self.__playerMonstersArea[playerName][indexSelfMonster][0].getName()+" direct attacks")
        print(targetPlayerName + "'s life points: " + str(self.__playerLifePoints[targetPlayerName]))
        if self.__playerLifePoints[targetPlayerName] <= 0:
            self.removePlayer(targetPlayerName)
            self.gameOverCheck()
    def activateEffect(self,effect,paraList):
        if effect.getActivatePhase() != self.getCurrentPhase():
            raise Exception('The phase you want to activate effect is wrong.')
        else:
            if effect.getName() == 'EffectDestroyAllSelfOrOpponentMonstersDependOnCoin':
                # paraList[0] is targetPlayerName
                zeroOrOne = randint(0, 1)
                if zeroOrOne == 0:  # coin 裏 destroy all self monsters
                    self.__playerMonstersArea[self.getCurrentPlayer()] = []
                    print(effect.getName() + ' activates.')
                    print('coin 裏')
                    print(self.getCurrentPlayer()+"'s monsters are all destroyed.")
                else:  # coin 表 destroy all monsters of target player
                    self.__playerMonstersArea[paraList[0]] = []
                    print(effect.getName() + ' activates.')
                    print('coin 表')
                    print(paraList[0] + "'s monsters are all destroyed.")
    def isGameOver(self):
        return self.__gameOver
def SimpleStrategy(playerName):
    def isExistMonster(playerName,location,minLevel,maxLevel):
        candidates = []
        answer = False
        if location == 'Hand':
            for card in ng.getCardObjectsInHand(playerName):
                if card.getType() == 'Monster' and minLevel <= card.getLevelNum() <= maxLevel:
                    candidates.append(card)
        elif location == 'MonsterArea':
            for card in ng.getMonsterObjectsInMonsterArea(playerName):
                if card[0].getType() == 'Monster' and minLevel <= card[0].getLevelNum() <= maxLevel:
                    candidates.append(card[0])
        if len(candidates) > 0:
            answer = True
        return answer
    def getIndexOfMonster(playerName,location,minLevel,maxLevel,maxOrMinATK,maxOrMinDEF):
        """
        :param playerName: The player who summon monster
        :param location: ex. 'Hand', 'MonsterArea'
        :param minLevel: summon monster whose level is equal and greater than
        :param maxLevel: summon monster whose level is equal and less than
        :param maxOrMinATK: choose monster whose ATK is highest(lowest)
        :param maxOrMinDEF: choose monster whose DEF is highest(lowest)
        """
        candidates = []
        atkValues = []
        cardName = ''
        index = 0
        if location == 'Hand':
            for card in ng.getCardObjectsInHand(playerName):
                if card.getType() == 'Monster' and minLevel <= card.getLevelNum() <= maxLevel:
                    candidates.append(card)
                    atkValues.append(card.getAttackValue())
            if maxOrMinATK == 'max':
                atkValue = max(atkValues)
                for card in candidates:
                    if card.getAttackValue() == atkValue:
                        cardName = card.getName()
            elif maxOrMinATK == 'min':
                pass
            for i in range(len(ng.getCardObjectsInHand(playerName))):
                if ng.getCardObjectsInHand(playerName)[i].getName() == cardName:
                    index = i
                    break
        elif location == 'MonsterArea':
            for card in ng.getMonsterObjectsInMonsterArea(playerName):
                if card[0].getType() == 'Monster' and minLevel <= card[0].getLevelNum() <= maxLevel:
                    candidates.append(card[0])
                    atkValues.append(card[0].getAttackValue())
            if maxOrMinATK == 'max':
                atkValue = max(atkValues)
                for card in candidates:
                    if card.getAttackValue() == atkValue:
                        cardName = card.getName()
            elif maxOrMinATK == 'min':
                atkValue = min(atkValues)
                for card in candidates:
                    if card.getAttackValue() == atkValue:
                        cardName = card.getName()
            for i in range(len(ng.getMonsterObjectsInMonsterArea(playerName))):
                if ng.getMonsterObjectsInMonsterArea(playerName)[i][0].getName() == cardName:
                    index = i
                    break
        return index
    def isExistDestroyMonsterPossibility(playerName):
        targetPlayerName = ''
        IndexOfSelfMonster = -1
        IndexOfTargetMonster = -1
        for player in ng.getPlayersInfoObjects():
            if player.getName() != playerName:
                targetPlayerName = player.getName()
                break
        allSelfMonsterObjects = ng.getMonsterObjectsInMonsterArea(playerName)
        allTargetMonsterObjects = ng.getMonsterObjectsInMonsterArea(targetPlayerName)
        for selfIndex in range(len(allSelfMonsterObjects)):
            if allSelfMonsterObjects[selfIndex][3] == False:
                selfATK = allSelfMonsterObjects[selfIndex][0].getAttackValue()
                for targetIndex in range(len(allTargetMonsterObjects)):
                    targetATK = allTargetMonsterObjects[targetIndex][0].getAttackValue()
                    if selfATK >= targetATK:
                        IndexOfSelfMonster = selfIndex
                        IndexOfTargetMonster = targetIndex
                        break
                break
        if IndexOfSelfMonster == -1:
            return -1
        else:
            return [targetPlayerName,IndexOfSelfMonster,IndexOfTargetMonster]
    def getAnotherPlayerName(playerName):
        targetPlayerName = ''
        for player in ng.getPlayersInfoObjects():
            if player.getName() != playerName:
                targetPlayerName = player.getName()
                break
        return targetPlayerName
    global ng
    while not ng.isGameOver():
        if ng.getCurrentPlayer() == playerName:
            if ng.getCurrentPhase() == 'Draw':
                print(ng.getCurrentPlayer() + ' ' + ng.getCurrentPhase())
                ng.drawCard(playerName, numDrawCard)
            elif ng.getCurrentPhase() == 'StandBy':
                print(ng.getCurrentPlayer() + ' ' + ng.getCurrentPhase())
                pass
            elif ng.getCurrentPhase() == 'Main':
                print(ng.getCurrentPlayer() + ' ' + ng.getCurrentPhase())
                normalSummonTimes = 0
                if normalSummonTimes == 0:
                    if isExistMonster(playerName,'Hand', 5, 6) and isExistMonster(playerName,'MonsterArea',1,4):
                        index = getIndexOfMonster(playerName, 'Hand',5, 6, 'max', None)
                        indexLowesrATKMonsterInMonsterArea = getIndexOfMonster(playerName,'MonsterArea',1, 8, 'min', None)
                        ng.advancedSummon(playerName,ng.getCardObjectsInHand(playerName)[index],[indexLowesrATKMonsterInMonsterArea])
                        normalSummonTimes += 1
                    elif not ng.isMonsterAreaFull(playerName) and isExistMonster(playerName,'Hand', 1, 4) and normalSummonTimes == 0:
                        index = getIndexOfMonster(playerName,'Hand' ,1, 4, 'max', None)
                        ng.normalSummon(playerName, ng.getCardObjectsInHand(playerName)[index])
                        normalSummonTimes += 1
                    elif ng.isMonsterAreaFull(playerName) and isExistMonster(playerName,'Hand', 1, 4) and normalSummonTimes == 0:
                        index = getIndexOfMonster(playerName, 'Hand', 1, 4, 'max', None)
                        ng.setMonster(playerName,index)
                        normalSummonTimes += 1
                for monster in ng.getMonsterObjectsInMonsterArea(playerName):
                    if monster[0].getName() == 'Time Magician' and monster[1] == 'ATK':
                        ng.activateEffect(effectA,[getAnotherPlayerName(playerName)])
            elif ng.getCurrentPhase() == 'Battle':
                print(ng.getCurrentPlayer() + ' ' + ng.getCurrentPhase())
                if len(ng.getMonsterObjectsInMonsterArea(playerName)) > 0:
                    selfMonsters = ng.getMonsterObjectsInMonsterArea(playerName)
                    for indexSelfMonster in range(len(selfMonsters)):
                        if selfMonsters[indexSelfMonster][1] == 'ATK' and \
                                selfMonsters[indexSelfMonster][3] == False:
                            targetPlayerName = getAnotherPlayerName(playerName)
                            targetMonsters = ng.getMonsterObjectsInMonsterArea(targetPlayerName)
                            if len(targetMonsters) > 0:
                                IndexTarget = 0
                                targetATKList = []
                                for indexTargetMonster in range(len(targetMonsters)):
                                    if selfMonsters[indexSelfMonster][0].getAttackValue() > targetMonsters[indexTargetMonster][0].getAttackValue():
                                        targetATKList.append(targetMonsters[indexTargetMonster][0].getAttackValue())
                                if len(targetATKList) > 0:
                                    for indexTargetMonster in range(len(targetMonsters)):
                                        if max(targetATKList) == targetMonsters[indexTargetMonster][0].getAttackValue():
                                            IndexTarget = indexTargetMonster
                                            break
                                    ng.attackMonster(playerName, indexSelfMonster, targetPlayerName,IndexTarget)

                            else:
                                ng.directAttack(playerName,indexSelfMonster,targetPlayerName)
                            if ng.isGameOver():
                                break


                # while isExistDestroyMonsterPossibility(playerName) != -1:
                #     targetPlayerName = isExistDestroyMonsterPossibility(playerName)[0]
                #     indexSelfMonster = isExistDestroyMonsterPossibility(playerName)[1]
                #     indexTargetMonster = isExistDestroyMonsterPossibility(playerName)[2]
                #     ng.attackMonster(playerName, indexSelfMonster, targetPlayerName, indexTargetMonster)
            elif ng.getCurrentPhase() == 'End':
                print(ng.getCurrentPlayer() + ' ' + ng.getCurrentPhase())
                pass
            ng.goToNextPhase()
        else:
            time.sleep(0.1)
limitNumOfSameCard =10
numDrawCard = 1  # The number of card which need to be drawn every turn
ThousandDragon = MonsterCard('Thousand Dragon',7,2400,2000)
DarkMagician = MonsterCard('Dark Magician',7,2500,2100)
DarkMagicianGirl = MonsterCard('Dark Magician Girl',6,2000,1700)
BabyDragon = MonsterCard('Baby Dragon',3,1200,700)
effectA = Effect('EffectDestroyAllSelfOrOpponentMonstersDependOnCoin','Main')
effectList=[]
effectList.append(effectA)
TimeMagician = MonsterCard('Time Magician',2,300,400,effectList)
cards = []
for n in range(limitNumOfSameCard):
    # cards.append(DarkMagician)
    cards.append(DarkMagicianGirl)
    cards.append(BabyDragon)
    cards.append(TimeMagician)
deckA = Deck('A',cards,[])
# copy the content of cards to cardsB
cardsB = cards[:]
# cardsB = []
# for n in range(limitNumOfSameCard):
#     # cards.append(DarkMagician)
#     cardsB.append(DarkMagicianGirl)
#     cardsB.append(BabyDragon)
#     cardsB.append(TimeMagician)
deckB = Deck('B',cardsB,[])

playerA = Player('YamiYugi')
playerB = Player('Rex')
playerA.addDeck(deckA)
playerB.addDeck(deckB)
playerList = [playerA,playerB]
ng = NormalGame(playerList)
t1 = threading.Thread(target=SimpleStrategy,args=('YamiYugi',))
t2 = threading.Thread(target=SimpleStrategy,args=('Rex',))
t1.start()
t2.start()