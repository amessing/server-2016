import DataModel
import json
import time
import math
import numpy as np
import pdb
from StringIO import StringIO

########## Defining Util/Convenience Functions ############
''' If there were too many more of these, or if this 
were actual server code, I would make a module, but 
for fake database creation purposes it is not worth it'''


def sumStdDevs(stdDevs):
	return sum(map(lambda x: x ** 2 , filter(lambda s: s != None, stdDevs))) ** 0.5

def convertFirebaseBoolean(fbBool):
	return True if fbBool == 'true' else False

def rms(values):
	if len(values) == 0: return None
	return math.sqrt(np.mean(map(lambda x: x**2, values)))

def convertNoneToIdentity(x, identity):
	return identity if x == None else x

def dictOperation(dict1, dict2, dictOp, identity):
	newDict = {}
	map(lambda k: setDictionaryValue(newDict, k, dictOp(convertNoneToIdentity(dict1[k], identity), convertNoneToIdentity(dict2[k], identity))), dict1)
	return newDict

def dictSum(dict1, dict2):
	return dictOperation(dict1, dict2, lambda x, y: x + y, 0)

def dictDifference(dict1, dict2):
	return dictOperation(dict1, dict2, lambda x, y: x - y, 0)

def dictProduct(dict1, dict2):
	return dictOperation(dict1, dict2, lambda x, y: x * y, 1)

def dictQuotient(dict1, dict2):
	return dictOperation(dict1, dict2, lambda x, y: float(x) / float(y) if float(y) != 0.0 else None, 1.0)

def dictPercentage(dict1, dict2):
	return dictQuotient(dict1, dictSum(dict1, dict2))

def dictDivideConstant(d, constant):
	returnDict = {}
	[setDictionaryValue(returnDict, k, (float(v)/constant)) for k, v in d.iteritems()]
	return returnDict

def stdDictSum(dict1, dict2):
	return dictOperation(dict1, dict2, lambda x, y: sumStdDevs([x, y]))

def setDictionaryValue(dict, key, value):
	dict[key] = value

def makeMatchFromDict(d):
	match = DataModel.Match(**d) #I have no idea why this works
	if 'calculatedData' in d.keys():
		match.calculatedData = DataModel.CalculatedMatchData(**d['calculatedData'])
	return match

def makeTeamFromDict(d):
	team = DataModel.Team(**d) #I have no idea why this works
	if 'calculatedData' in d.keys():
		team.calculatedData = DataModel.CalculatedTeamData(**d['calculatedData'])
	return team

def makeTIMDFromDict(d):
	timd = DataModel.TeamInMatchData(**d) #I have no idea why this works
	if 'calculatedData' in d.keys():
		timd.calculatedData = DataModel.CalculatedTeamInMatchData(**d['calculatedData'])
	return timd

def makeTeamsFromDicts(dicts):
	return map(lambda v: makeTeamFromDict(v), dicts.values())

def makeMatchesFromDicts(dicts):
	return [makeMatchFromDict(m) for m in dicts if m != None]

def makeDictFromObject(o):
	if isinstance(o, dict): 
		[setDictionaryValue(o,k,v) for k,v in o.iteritems() if v.__class__ in [DataModel.CalculatedTeamData, DataModel.CalculatedMatchData, DataModel.CalculatedTeamInMatchData]]
		return o
	return dict((key, value) for key, value in o.__dict__.iteritems() if not callable(value) and not key.startswith('__'))

def readValueFromObjectDict(objectDict, key):
	return objectDict[key]

def makeDictFromTeam(t):
	d = makeDictFromObject(t)
	d['calculatedData'] = makeDictFromObject(d['calculatedData'])
	return d

def makeDictFromMatch(t):
	d = makeDictFromObject(t)
	d['calculatedData'] = makeDictFromObject(d['calculatedData'])
	return d

def makeDictFromTIMD(timd):
	d = makeDictFromObject(timd)
	d["calculatedData"] = makeDictFromObject(d['calculatedData'])
	return d

def makeDictFromCalculatedData(calculatedData):
	return calculatedData.__dict__

def makeTIMDsFromDicts(timds):
	return [makeTIMDFromDict(timd) for timd in timds.values() if timd != None]

def makeTeamObjectWithNumberAndName(number, name):
	team = Team()
	team.name, team.number = name, number
	return team

def makeTIMDFromTeamNumberAndMatchNumber(teamNumber, matchNumber):
	timd = DataModel.TeamInMatchData()
	timd.teamNumber, timd.matchNumber = teamNumber, matchNumber
	return timd

def setDataForMatch(match):
	m = DataModel.Match()
	f = lambda key: [match["alliances"]["red"][key], match["alliances"]["blue"][key]]
	m.number, m.redAllianceTeamNumbers, m.blueAllianceTeamNumbers = int(match["match_number"]), f("teams")[0], f("teams")[1]
	m.redScore, m.blueScore, m.TIMDs = f("score")[0], f("score")[1], []
	return m

def setDataForTeam(team):
	t = DataModel.Team()
	t.number, t.name, t.teamInMatchDatas = team["team_number"], team["nickname"], []
	return t

def printWarningForSeconds(numSeconds):
	print str(numSeconds) + ' SECONDS UNTIL FIREBASE WIPES'
	time.sleep(1)

def makeASCIIFromJSON(input):
    if isinstance(input, dict):
        return dict((makeASCIIFromJSON(k), makeASCIIFromJSON(v)) for (k, v) in input.iteritems())
    elif isinstance(input, list):
        return map(lambda i: makeASCIIFromJSON(i), input)
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input




