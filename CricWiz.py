from pycricbuzz import Cricbuzz
import argparse
from tabulate import tabulate
import sys
from time import sleep
import subprocess as s


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--livescore", required=True, help="Show the liveScore")
    args = vars(parser.parse_args())

    if args['livescore']:
        liveScore()
        sleep(1)
        choice = input("\nDo you want to see the full Scorecard or commentary of any match?(y/n)")

        if choice.lower() == "y":
            sleep(1)
            ans = input("\nWhat do you want to get?\n\
            1. Full scorecard\n\
            2. Commentary\n\
            3. Both\n\
            Enter your choice: ")
            sleep(1)

            if ans == "1":
                match_id = (input("\nEnter the Match ID of that match: "))
                scoreCard(match_id)
            elif ans == "2":
                match_id = (input("\nEnter the Match ID of that match: "))
                commentary(match_id)
            elif ans == "3":
                match_id = (input("\nEnter the Match ID of that match: "))
                scoreCard(match_id)
                commentary(match_id)
            else:
                print(colors("\nWrong choice!Please select a valid choice!", 31))
        else:
            sys.exit()


def liveScore():
    """To fetch the live score for a match using the cricbuzz object"""

    c = Cricbuzz()
    matches = c.matches()
    counter = 0
    headers = ["S.No", "Id", "Head", "Teams", "MatchType", "Status"]
    my_data = []
    for match in matches:
        game = c.livescore(match['id'])
        idey = game['matchinfo']['id']
        head = game['matchinfo']['srs']
        teams = game['matchinfo']['mchdesc']
        matchType = game['matchinfo']['type']
        status = game['matchinfo']['status']
        counter = counter + 1
        my_data.append([counter, idey, head, teams, matchType, status])
    print(colors(tabulate(my_data, headers=headers, tablefmt="grid"), 32))

    for match in matches:
        if status.lower() == "inprogress":
            notified = input("Hey there, {} is live do you want to get notified about this match?(y/n)".format(teams))
            if notified.lower() == "y":
                print(colors("You will be notified!", 32))
                sendmessage("{} - {} / {}({} Ovs)".format(batteam, runs, wickets, overs))


def commentary(mid):
    """ To Fetch commentary of the match"""

    c = Cricbuzz()
    matches = c.matches()
    for match in matches:
        if match['id'] == mid:
            commentary = c.commentary(match['id'])['commentary']
            print("\n--COMMENTARY--")
            for index in commentary:
                print(colors(index, 32))


def scoreCard(mid):
    """ To Fetch scorecard of a match"""

    c = Cricbuzz()
    matches = c.matches()
    counter = 0
    my_data = []
    for match in matches:
        if match['id'] == mid:
            game = c.scorecard(match['id'])
            for i in range(2):
                wickets = game['scorecard'][i]['wickets']
                runs = game['scorecard'][i]['runs']
                bowlteam = game['scorecard'][i]['bowlteam']
                overs = game['scorecard'][i]['overs']
                batteam = game['scorecard'][i]['batteam']
                runrate = game['scorecard'][i]['runrate']
                print("\n{}st INNINGS! )".format(2 - i))
                print(colors("{} - {} / {}({} Ovs)".format(batteam, runs, wickets, overs), 32))
                sleep(1)
                print("\n--Batting Card--")
                battCard(game, i)
                sleep(1)
                print("\n--Bowling Card--")
                bowlCard(game, i)
                sleep(1)

            squad(game)


def bowlCard(game, i):
    """ A function to print the bowling card in a tabular form, which contains:
              Name of the Bowler
              Maidens bowled by the bowler
              Overs bowled by the bowler
              Runs conceded by the bowler
              Wickets taken by the bowler
    """

    header = ["Name", "Maidens", "Overs", "Runs", "Wickets"]
    my_data = []
    try:
        for j in range(11):
            maidens = game['scorecard'][i]['bowlcard'][j]['maidens']
            overs = game['scorecard'][i]['bowlcard'][j]['overs']
            runs = game['scorecard'][i]['bowlcard'][j]['runs']
            name = game['scorecard'][i]['bowlcard'][j]['name']
            wickets = game['scorecard'][i]['bowlcard'][j]['wickets']
            my_data.append([name, maidens, overs, runs, wickets])
    except IndexError:
        pass
    finally:
        print(colors(tabulate(my_data, headers=header, tablefmt="grid"), 32))


def battCard(game, i):
    """ A function to print the batting card in a tabular form, which contains:
              Name of the Batsmen
              Runs scored by the batsmen
              Balls faced by the batsmen
              Sixs hit by the batsmen
              fours hit by the batsmen
              Dismissal
    """

    header = ["Name", "runs", "balls", "six", "fours", "dismissal"]
    my_data = []
    try:
        for j in range(11):
            name = game['scorecard'][i]['batcard'][j]['name']
            runs = game['scorecard'][i]['batcard'][j]['runs']
            balls = game['scorecard'][i]['batcard'][j]['balls']
            six = game['scorecard'][i]['batcard'][j]['six']
            fours = game['scorecard'][i]['batcard'][j]['fours']
            dismissal = game['scorecard'][i]['batcard'][j]['dismissal']
            my_data.append([name, runs, balls, six, fours, dismissal])
    except IndexError:
        pass
    finally:
        print(colors(tabulate(my_data, headers=header, tablefmt="grid"), 32))


def squad(game):
    """ To display the squad for the individual teams available for the match"""

    header = ["S.no", "Player"]
    for i in range(2):
        my_data = []
        counter = 1
        squad = game['squad'][i]['members']
        sq_team = game['squad'][i]['team']
        print(colors("\n--{} Squad--\n".format(sq_team), 32))
        for member in game['squad'][i]['members']:
            my_data.append([counter, member])
            counter += 1
        print(tabulate(my_data, headers=header, tablefmt="plain"))
        print("\n")
        sleep(1)


def sendmessage(message):
    """ To send the notification about the live score update"""

    s.call(['notify-send', message])
    sleep(60)


def colors(string, color):
    """A function to make the things look magical"""

    return("\033[%sm%s\033[0m" % (color, string))


if __name__ == '__main__':
    main()
