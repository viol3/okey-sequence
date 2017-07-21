import random
import collections
import time
# developed by viol3
# special thanks to thewataru
# 04.07.2017
# generates logically ordered sequences from random generated Okey game(Gin Rummy) pieces.

ranks = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'okey']

suits = ['yellow', 'black', 'blue', 'red', '*']

def randomCard():
    return [ranks[int(random.random() * len(ranks))], suits[int(random.random() * len(suits))]]

def getDuplicates(liste):
    liste2 = liste[:]
    sonuc = []
    for a in liste:
        if a[0] == 'okey':
            continue
        if liste2.count(a) > 1:
            sonuc.append(a)
            liste2 = filter(lambda b: b != a, liste2)
            liste2.append(a)
    return sonuc, liste2



def decompile_cards(cards):
    sonuc = []
    for card in cards:
        if card[0] == 'okey':
            sonuc.append(52)
        else:
            aa = suits.index(card[1]) * 13 + ranks.index(card[0])
            sonuc.append(aa)
    
    return sonuc




def randomHand(hl):
    h = []
    while hl > 0:
        h.append(randomCard())
        hl -= 1
    return h

def lreversed(l):
    return [k for k in reversed(l)]

def rankOf(x):
    return x[0]

def isThere(x, l):
    return x in l;

def nextRankOf(x):
    if x[0] == 'king': return 'god'
    return ranks[ranks.index(x[0]) + 1]

def nextofnextRankOf(x):
    if x[0] == 'king' or x[0] == 'queen': return 'god'
    return ranks[ranks.index(x[0]) + 2]

def suitOf(x):
    return x[1]

def isOkey(x):
    return x[1] == '*'

def isThereOkey(l):
    return ['okey', '*'] in l

def scoreOf(x):
    if rankOf(x) == 'jack':
        return 11
    elif rankOf(x) == 'queen':
        return 12
    elif rankOf(x) == 'king':
        return 13
    elif rankOf(x) == 'okey':
        return 1
    elif rankOf(x) == 'ace':
        return 1
    else:
        return ranks.index(rankOf(x)) + 1


def trialScore(t):
    return t[0]


    

def verbose_automatch(L):

    LA = getDuplicates(L)
    result = automatch_iter([], [], LA[1], 0)
    yeni = LA[0] + result[3]

    result2 = automatch_iter2([], [], yeni, 0)
    artik = result2[3]

    
    artikA = getDuplicates(artik)
    print "----------------------------------"
    son = automatch_iter([], [], artikA[1], 0)
    son2 = automatch_iter2([], [], son[3], 0)
    return result2[1] + result[2] + son[2] + son2[1], son2[3] + artikA[0]



def automatch(L):
    return automatch_iter([], [], L, 0)

def automatch_iter(sets, runs, free, score):
    if free == []:
        return [score, sets, runs, free]

    maxScore = score
    maxKey = [score, sets, runs, free]


    l = free[:]
    l.sort(reverse=True, key=lambda u:  \
            suits.index(u[1]) * 20 + ranks.index(u[0]))
    streakStart = 0
    streakScore = 0
    for i in range(len(l)):

        if isOkey(l[i]):
            continue

        if i < 0  or suitOf(l[i-1]) != suitOf(l[i]) or nextRankOf(l[i]) != rankOf(l[i-1]):
            streakStart = i
            streakScore = 0

        streakScore += scoreOf(l[i])
        streakLength = i - streakStart + 1
        if streakLength >= 3:
            hazir =  [lreversed(l[streakStart : i + 1])]
            frees = l[0:streakStart] + l[i+1:]
            
            trial = automatch_iter(sets,    runs + hazir, frees, score + streakScore)
            if trialScore(trial) > maxScore:
                maxScore = trialScore(trial)
                maxKey = trial
        elif streakLength >= 2 and rankOf(l[streakStart]) == 'king' and isThere(['ace', suitOf(l[streakStart])], l):
            hazir =  [lreversed(l[streakStart : i + 1]) + [['ace', suitOf(l[streakStart])]]]
            frees = l[0:streakStart] + l[i+1:]
            frees.remove(['ace', suitOf(l[streakStart])])
            trial = automatch_iter(sets,    runs + hazir, frees, score + streakScore+ 1)
            if trialScore(trial) > maxScore:
                maxScore = trialScore(trial)
                maxKey = trial
        elif streakLength >= 1 and isThereOkey(l) and nextofnextRankOf(l[i]) == rankOf(l[i-1]) and suitOf(l[i-1]) == suitOf(l[i]):
            hazir = [lreversed([l[i-streakLength] + [['okey', '*']] +  [l[i]]])]
            frees = l[0:i-1] + l[i+1:]
            frees.remove(['okey', '*'])
            trial = automatch_iter(sets,    runs + hazir, frees, score + streakScore+ 1)
            if trialScore(trial) > maxScore:
                maxScore = trialScore(trial)
                maxKey = trial
        elif streakLength >= 2 and isThereOkey(l) and i + 1 < len(l) and nextRankOf(l[i]) != rankOf(l[i+1]) and suitOf(l[i-1]) == suitOf(l[i]):
            hazir = [lreversed([l[i-1]] +  [l[i]] + [['okey', '*']])]
            frees = l[0:i-1] + l[i+1:]
            frees.remove(['okey', '*'])
            trial = automatch_iter(sets,    runs + hazir, frees, score + streakScore+ 1)
            if trialScore(trial) > maxScore:
                maxScore = trialScore(trial)
                maxKey = trial
        

    

    return maxKey


def automatch_iter2(sets, runs, free, score):

    if free == []:
        return [score, sets, runs, free]

    maxScore = score
    maxKey = [score, sets, runs, free]

    l = free[:]
    l.sort(reverse=True, key=rankOf)

    streakStart = 0
    streakScore = 0

    for i in range(len(l)):
        if not (i > 0 and rankOf(l[i - 1]) == rankOf(l[i])):
            streakStart = i
            streakScore = 0

        streakScore += scoreOf(l[i])
        streakLength = i - streakStart + 1

        if streakLength == 5:
            streakLength = 0
            streakScore = scoreOf(l[i])

        if streakLength in [3,4,5]:
            trial = automatch_iter(sets + [lreversed(l[streakStart : i + 1])], runs, l[0:streakStart] + l[i+1:], score + streakScore)

            if trialScore(trial) > maxScore:
                maxScore = trialScore(trial)
                maxKey = trial

    return maxKey

lib = []

for j in range(53):
    lib.append(j)
    lib.append(j)
random.shuffle(lib)


millis1 = int(round(time.time() * 1000))
sonuc1 = []
deneme = []
for a in range(14):
    poppy = random.choice(lib)
    deneme.append(poppy)
    lib.remove(poppy)


for d in deneme:
    card = None
    if d == 52:
        card = ['okey', '*']
    else:
        card = [ranks[d % 13], suits[d / 13]]
    sonuc1.append(card)
hepsi = verbose_automatch(sonuc1)
hazirlanmis = hepsi[0]
boslar = hepsi[1]
bravo = []
for hazir in hazirlanmis:
    bravo.extend( decompile_cards(hazir) + [-1] )

bravo.extend(decompile_cards(boslar))
millis2 = int(round(time.time() * 1000))
print "Input : " + str(deneme)
print "Output : " + str(bravo)
print "Time elapsed : " + str(millis2 - millis1) + " ms"
