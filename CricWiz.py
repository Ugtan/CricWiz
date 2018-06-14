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
        Rmatches()
        sleep(1)
        choice = input(colors("\nDo you want to get details of any of the above matches? (y/n) :", 36))

        if choice.lower() == "y":
            sleep(1)
            ans = input("\nWhat do you want to get?\n\
               1. Scorecard\n\
               2. Commentary\n\
               3. Squad\nEnter your choice: ")
            sleep(1)
            match_id = (input("\nEnter the Match ID of that match: "))
            ch = check(match_id)
            if ans == "1":
                if ch == "preview":
                    print(colors("\nMatch has not yet started!\n", 31))

                elif ch == "inprogress":
                    scoreCard(match_id)
                    notified = input("Hey there, This match is live do you want to get notified about this match?(y/n)")
                    if notified.lower() == "y":
                        print(colors("You will be notified!( Just press Ctrl + c to stop getting notifications)", 32))
                        try:
                            while True:
                                send(match_id)
                        except KeyboardInterrupt:
                            pass
                else:
                    scoreCard(match_id)

            elif ans == "2":
                if ch != "preview":
                    commentary(match_id)
                else:
                    print(colors("\nMatch has not yet started!\n", 31))
            elif ans == "3":
                if ch != "preview":
                    squad(match_id)
                else:
                    print(colors("\nMatch has not yet started!\n", 31))

            else:
                print(colors("\nWrong choice!Please select a valid choice!\n", 31))
        elif choice.lower() == "n":
            print(colors("\nThank You for using CricWiz, have a nice day!\n", 35))
            sys.exit()
        else:
            print(colors("\nWrong choice!Please select a valid choice!\n", 31))


def Rmatches():
    """To fetch the Recent matches held or upcoming or live matches using the cricbuzz object"""

    c = Cricbuzz()
    matches = c.matches()
    headers = ["S.No", "Id", "Head", "Teams", "MatchType", "Status"]
    my_data = []
    counter = 1
    for counter, match in enumerate(matches, start=1):
        try:
            idey = matches[counter - 1]['id']
            head = matches[counter - 1]['srs']
            teams = matches[counter - 1]['mchdesc']
            matchType = matches[counter - 1]['type']
            status = matches[counter - 1]['status']
            my_data.append([counter, idey, head, teams, matchType, status])
        except KeyError:
            pass
    print(colors(tabulate(my_data, headers=headers, tablefmt="fancy_grid"), 32))


def commentary(mid):
    """ To Fetch commentary of the match"""

    c = Cricbuzz()
    matches = c.matches()
    for match in matches:
        if match['id'] == mid:
            commentary = c.commentary(match['id'])['commentary']
            print("\n--COMMENTARY--\n")
            for index in commentary:
                print(colors(index, 32))
            print("\n")


def scoreCard(mid):
    """ To Fetch scorecard of a match"""

    c = Cricbuzz()
    matches = c.matches()
    my_data = []
    for match in matches:
        if match['id'] == mid:
            game = c.scorecard(match['id'])
            status = game['matchinfo']['status']
            desc = game['matchinfo']['mchdesc']
            state = game['matchinfo']['mchstate']
            print(colors("\n{} | {} | {}\n".format(desc, status, state), 33))
            try:
                for i in range(2):
                    wickets = game['scorecard'][i]['wickets']
                    runs = game['scorecard'][i]['runs']
                    bowlteam = game['scorecard'][i]['bowlteam']
                    overs = game['scorecard'][i]['overs']
                    batteam = game['scorecard'][i]['batteam']
                    runrate = game['scorecard'][i]['runrate']

                    print(colors("\n{} - {} / {}({} Ovs)".format(batteam, runs, wickets, overs), 32))
                    sleep(1)
                    print("\n--BATTING CARD--\n")
                    battCard(game, i)
                    sleep(1)
                    print("\n--BOWLING CARD--\n")
                    bowlCard(game, i)
                    sleep(1)
            except IndexError:
                pass


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
        print(colors(tabulate(my_data, headers=header, tablefmt="fancy_grid"), 32))


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
        print(colors(tabulate(my_data, headers=header, tablefmt="fancy_grid"), 32))


def squad(mid):
    """ To display the squad for the individual teams available for the match"""

    header = ["S.no", "Player"]
    c = Cricbuzz()
    game = c.scorecard(mid)
    try:
        for i in range(2):
            my_data = []
            squad = game['squad'][i]['members']
            sq_team = game['squad'][i]['team']
            print(colors("\n--{} Squad--\n".format(sq_team), 32))
            counter = 1
            for counter, member in enumerate(game['squad'][i]['members'], start=1):
                my_data.append([counter, member])
            print(tabulate(my_data, headers=header, tablefmt="fancy_grid"))
            print("\n")
            sleep(1)
    except KeyError:
        game = c.commentary(mid)
        try:
            for i in range(1, 4):
                print("\n" + game['commentary'][i])

        except (IndexError, KeyError):
            pass


def check(mid):
    """ To check is the match has already started or not"""

    c = Cricbuzz()
    matches = c.matches()
    for match in matches:
        if match['id'] == mid:
            return match['mchstate']
            break


def send(mid):
    """ To send the notification about the live score update"""

    c = Cricbuzz()
    game = c.scorecard(mid)
    try:
        for i in range(1):
            wickets = game['scorecard'][i]['wickets']
            runs = game['scorecard'][i]['runs']
            bowlteam = game['scorecard'][i]['bowlteam']
            overs = game['scorecard'][i]['overs']
            batteam = game['scorecard'][i]['batteam']
            runrate = game['scorecard'][i]['runrate']
            message = "{} - {} / {}( {} Ovs )".format(batteam, runs, wickets, overs)
    except IndexError:
        pass
    s.call(['notify-send', message])
    sleep(60)


def colors(string, color):
    """A function to make the things look magical"""

    return("\033[%sm%s\033[0m" % (color, string))


if __name__ == '__main__':
    main()
