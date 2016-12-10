#!/usr/bin/python

import sys

f = open(sys.argv[1], 'r')

bots = {}
outputs = {}
fullBots = set()

def getBot(botId):
    if botId in bots:
        return bots[botId]
    else:
        bot = {
            'values': []
        }
        bots[botId] = bot
        return bot


def addValue(botId, value, botSet):
    bot = getBot(botId)
    values = bot['values']
    values.append(value)
    if len(values) == 2:
        botSet.add(botId)


def placeValue(target, value, botSet):
    if target[0] == 'bot':
        addValue(target[1], value, botSet)
    else:
        outputs[target[1]] = value

for line in f.readlines():
    parts = line.split()

    if parts[0] == 'value':
        value = int(parts[1])
        botId = int(parts[5])
        addValue(botId, value, fullBots)
    elif parts[0] == 'bot':
        botId = int(parts[1])
        bot = getBot(botId)
        bot['low'] = (parts[5], int(parts[6]))
        bot['high'] = (parts[10], int(parts[11]))

while len(fullBots):
    newFullBots = set()
    for botId in fullBots:
        bot = bots[botId]
        hi = reduce(max, bot['values'])
        lo = reduce(min, bot['values'])
        highTarget = bot['high']
        lowTarget = bot['low']

        if hi == 61 and lo == 17:
            print botId

        placeValue(highTarget, hi, newFullBots)
        placeValue(lowTarget, lo, newFullBots)

    fullBots = newFullBots

#for (botId, bot) in bots.items():
#    print botId, ':', bot

print outputs[0]*outputs[1]*outputs[2]
