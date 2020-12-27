#IMPORTS
import csv
import pandas as pd
import re
import nltk
import os

#LOADING FILES INTO ONE DF
PBP_data = "../nflscrapR-data/play_by_play_data/regular_season"
dfs = []

for season_file in os.listdir(PBP_data):
    df = pd.read_csv(PBP_data + "/" + season_file, usecols=['desc', 'play_type', 'defteam', 'posteam']) #is this disjointing the lists?
    dfs.append(df)
    print(season_file + " loaded.")

df = pd.concat(dfs)
df = df[df["play_type"] == "kickoff"]

#EXTRACTING DATA, CREATING NEW DF
def make_DF(texts, kicking, receiving):
    #FIRST SENTENCE
    kicker = [] #String
    isTouchback = [] #bool
    isOutOfBounds = [] #bool
    isOnside = [] #bool
    isFairCatch = [] #bool
    kick_yards = [] #int
    kick_start = [] #int

    tb = re.compile("Touchback")
    oob = re.compile("out of bounds")
    fc = re.compile("fair catch")
    kck_dist1 = re.compile("kicks( onside)? -?[0-9]{1,2} yard(s)?") #if you want to sort onside kicks... do it here.
    kck_dist2 = re.compile("[0-9]+") #kicks from 0-anything
    kck_spot1 = re.compile("from ([A-Z]{2,3} )?[0-9]{1,3} to (([A-Z]{2,3} )?-?[0-9]{1,3}|end zone)")
    kck_spot2 = re.compile("-?[0-9]{1,3}") #ints, strings?

    #SECOND SENTENCE
    returners = [] #String
    tacklers = [] #String
    returnYards = [] #int
    returnSpot = [] #int
    isReturned = [] #bool
    isAdvanced = [] #bool
    isTouchdown = [] #bool

    return_sent = re.compile("(\w+\.\w+((\-| |')\w+)*\.?) (((\(didn't try to advance\) )?(to ([A-Z]{1,3} )?[0-9]{1,3} )?)|((ran|pushed) ob at ([A-Z]{1,3} )?[0-9]{1,3}) )for ((-)?[0-9]{1,3} yard(s)?|(no gain))( \(((\w+\.\w+((\-| |')\w+)*\.?)(;|,) )*(\w+\.\w+((\-| |')\w+)*\.?)\))?")
    returner_sent = re.compile("(\w+\.\w+((\-| |')\w+)*\.?) (((\(didn't try to advance\) )?(to ([A-Z]{1,3} )?[0-9]{1,3} )?)|((ran|pushed) ob at ([A-Z]{1,3} )?[0-9]{1,3}) )for ((-)?[0-9]{1,3} yard(s)?|(no gain))")
    tackler_sent = re.compile("(((\(didn't try to advance\) )?(to ([A-Z]{1,3} )?[0-9]{1,3} )?)|((ran|pushed) ob at ([A-Z]{1,3} )?[0-9]{1,3}) )for ((-)?[0-9]{1,3} yard(s)?|(no gain))( \(((\w+\.\w+((\-| |')\w+)*\.?)(;|,) )*(\w+\.\w+((\-| |')\w+)*\.?)\))?")
    advanced = re.compile("\(didn't try to advance\)")
    touchdown = re.compile("TOUCHDOWN")
    name = re.compile("(\w+\.\w+((\-| |')[A-Z]+[a-z]*)*\.?)")

    nullified_search = re.compile("NULLIFIED")
    return_spot = re.compile("to (([A-Z]{1,3} )?[0-9]{1,3} )?|((ran|pushed) ob at ([A-Z]{1,3} )?[0-9]{1,3}) ")
    return_yards = re.compile("for ((-)?[0-9]{1,3} yard(s)?|(no gain))")
    spot = re.compile("-?[0-9]{1,3}")
    yards = re.compile("-?[0-9]{1,3}") #probably didn't need both of these... oh well!

    #OTHER DATA
    muffs = [] #bool
    retainsMuff = [] #bool
    isPenalty = [] #bool
    penalizedPlayer = [] #String
    penaltyYards = [] #int
    penaltyType = [] #String
    penaltySpot = [] #int
    fumbles = [] #bool
    retainsFumble = [] #bool

    muff_search = re.compile("MUFFS")
    muff_recover_search = re.compile("RECOVERED")
    penalty_search = re.compile("PENALTY on [A-Z]{1,3}-(\w+\.\w+((\-| |')\w+)*\.?), \w+(( |-)\w+)*( \([0-9]{1,2} (Y|y)ards\))?, [0-9]{1,2} yards, enforced at [A-Z]{1,3} [0-9]{1,2}.")
    penalty_search2 = re.compile(", \w+(( |-)\w+)*( \([0-9]{1,2} (Y|y)ards\))?, [0-9]{1,2} yards,")
    penalty_search3 = re.compile("PENALTY on [A-Z]{1,3}-")
    penaltyType_search = re.compile("\w+(( |-)\w+)*")
    penaltySpot_search = re.compile("enforced at [A-Z]{1,3} [0-9]{1,2}.")
    fumble_search = re.compile("FUMBLES")
    recovers_search = re.compile("RECOVERED")

    i=0
    for text in texts: #this runs in polynomial time, don't care about optimizing
        #print(text, ":", kicking[i], ":", receiving[i])
        #FIRST SENTENCE
        #Kicker
        kicker.append(text.split(" kicks")[0])

        #Touchbacks
        tb_result = re.search(tb, text)
        if(tb_result != None):
            isTouchback.append(True)
        else:
            isTouchback.append(False)

        #Out of Bounds
        oob_result = re.search(oob, text)
        if(oob_result != None):
            isOutOfBounds.append(True)
        else:
            isOutOfBounds.append(False)

        #Onside Kick
        onside_result1 = re.search(kck_dist1, text)
        if(not onside_result1):
            print(text)
        onside_result2 = re.search("onside", onside_result1.group())
        if(onside_result2 == None):
            isOnside.append(False)
        else:
            isOnside.append(True)

        #Fair Catch
        fc_result = re.search(fc, text)
        if(fc_result != None):
            isFairCatch.append(True)
        else:
            isFairCatch.append(False)

        #Kick Distance
        kck_dist_result = re.search(kck_dist1, text)
        if(kck_dist_result == None):
            print("ERROR")
        else:
            kck_dist_result = re.search(kck_dist2, kck_dist_result.group())
            kick_yards.append(int(kck_dist_result.group()))

        #Kick Start
        ks_result1 = re.search(kck_spot1, text)
        if(ks_result1 != None):
            ks_result1 = re.sub("end zone", "00", ks_result1.group())

            ks_result2 = re.findall(kck_spot2, ks_result1) #two item list of yardlines

            if(ks_result2[0] == None):
                print("ERROR")
            else:
                kick_start.append(int(ks_result2[0]))

        #SECOND SENTENCE
        #Returner
        return_phrase = re.search(returner_sent, text)
        if(return_phrase == None):
            returners.append("no returner")
        else:
            returner = re.search(name, return_phrase.group())
            if(returner != None):
                returners.append(returner.group())
            else:
                returners.append("no returner")

        #Tackler(s)
        tackler_phrase = re.search(tackler_sent, text)
        if(tackler_phrase == None):
            tacklers.append("no tackler")
        else:
            tackler_list = re.findall(name, tackler_phrase.group())
            if(tackler_list != None):
                tacklers_ = []
                for tackler_items in tackler_list:
                    tacklers_.append(tackler_items[0])
                tacklers.append(tacklers_)
            else:
                tacklers.append("no tackler")

        #Return
        return_result = re.search(return_sent, text)
        if(return_result != None):
            isReturned.append(True)
        else:
            isReturned.append(False)


        #Advanced
        advanced_result = re.search(advanced, text)
        if(advanced_result != None):
            isAdvanced.append(False)
        else:
            isAdvanced.append(True)

        #Touchdown
        touchdown_result = re.search(touchdown, text)
        if(touchdown_result != None):
            nullified_result = re.search(nullified_search, text)
            if(nullified_result):
                isTouchdown.append(False)
            else:
                isTouchdown.append(True)
        else:
            isTouchdown.append(False)

        #Return Spot
        #kick_land - return_yards

        #Return Yards
        ry_result = re.search(return_yards, text)
        if(ry_result):
            ry = re.sub("no gain", "00", ry_result.group())
            ry = re.search(yards, ry)
            if(ry):
                returnYards.append(int(ry.group()))
            else:
                print("ERROR:", ry_result.group())
        else:
            returnYards.append(0)

        #OTHER DATA
        #Muffs
        muff_result = re.search(muff_search, text)
        if(muff_result):
            muffs.append(True)
            muff_recover_result = re.search(muff_recover_search, text)
            if(muff_recover_result):
                retainsMuff.append(False)
            else:
                retainsMuff.append(True)
        else:
            muffs.append(False)
            retainsMuff.append(True)

        #Penalty, Penalized Player, Penalty Yards, Penalty Type
        penalty_result = re.search(penalty_search, text)
        if(penalty_result):
            isPenalty.append(True)
            penalizedPlayer_result = re.search(name, penalty_result.group())
            if(penalizedPlayer_result):
                penalizedPlayer.append(penalizedPlayer_result.group())
            else:
                print("ERROR")
            penaltyYards_result = re.search(yards, penalty_result.group())
            if(penaltyYards_result):
                penalty_result3 = re.search(penalty_search3, penalty_result.group())
                #HERE IS WHERE YOU NEED TO MAKE +/- YARDS
                if(kicking[i] in penalty_result3.group()):
                    yds = -1*int(penaltyYards_result.group())
                    penaltyYards.append(yds)
                else:
                    yds = int(penaltyYards_result.group())
                    penaltyYards.append(yds)
            else:
                print("ERROR")
            penalty2_result = re.search(penalty_search2, text)
            if(penalty2_result):
                penaltyType_result = re.search(penaltyType_search, penalty2_result.group())
                if(penaltyType_result):
                    penaltyType.append(penaltyType_result.group())
                else:
                    print("ERROR")
            else:
                print("ERROR")
            penaltySpot_result = re.search(penaltySpot_search, text)
            if(penaltySpot_result):
                penaltySpot_result2 = re.search(spot, penaltySpot_result.group())
                if(penaltySpot_result2):
                    penaltySpot.append(100 - int(penaltySpot_result2.group()))
                else:
                    print("ERROR")
            else:
                print("ERROR")
        else:
            isPenalty.append(False)
            penalizedPlayer.append("no player")
            penaltyYards.append(0)
            penaltyType.append("no penalty")
            penaltySpot.append(0)

        #Fumbles
        fumbles_result = re.search(fumble_search, text)
        if(fumbles_result):
            fumbles.append(True)
            rf_result = re.search(recovers_search, text)
            if(rf_result):
                retainsFumble.append(False)
            else:
                retainsFumble.append(True)
        else:
            fumbles.append(False)
            retainsFumble.append(True)

        i+=1

    df = pd.DataFrame()

    #KICKING AND RECEIVING TEAMS
    df["kicking_team"] = kicking
    df["receiving_team"] = receiving

    #FIRST SENTENCE
    df["text"] = texts
    df["kicker"] = kicker
    df["isTouchback"] = isTouchback
    df["isOutOfBounds"] = isOutOfBounds
    df["isOnside"] = isOnside
    df["isFairCatch"] = isFairCatch
    df["kickYards"] = kick_yards
    df["kickStart"] = kick_start
    df["kickLand"] = df["kickStart"] + df["kickYards"]

    #SECOND SENTENCE
    df["returner"] = returners
    df["tacklers"] = tacklers
    df["returnYards"] = returnYards
    df["returnSpot"] = df["kickLand"] - df["returnYards"]
    df["isReturned"] = isReturned
    df["isAdvanced"] = isAdvanced
    df["isTouchdown"] = isTouchdown

    #OTHER DATA
    df["isMuff"] = muffs
    df["retainsMuff"] = retainsMuff
    df["isPenalty"] = isPenalty
    df["penalizedPlayer"] = penalizedPlayer
    df["penaltyYards"] = penaltyYards
    df["penaltyType"] = penaltyType
    df["penaltySpot"] = penaltySpot
    df["isFumble"] = fumbles
    df["retainsFumble"] = retainsFumble

    #Final Spot Calculation
    #penalty
    pen_set = df[df["isPenalty"] == True]
    pen_set["finalSpot"] = df["penaltySpot"] + df["penaltyYards"]

    #non-penalty
    nonpen_set = df[df["isPenalty"] == False]
    nonpen_set["finalSpot"] = df["returnSpot"]

    return pen_set.append(nonpen_set)

#CHECKING FOR BAD ENTRIES
df = df[~df['desc'].str.contains("play under review", na=False)]

print("creating dataframe...")
df = make_DF(list(df["desc"]), list(df["defteam"]), list(df["posteam"]))

print(df.head())
df.to_csv("kickoff_dataset.csv")
