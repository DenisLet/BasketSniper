from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from functools import reduce
from itertools import chain
import time
from statistics import mean
from send import bet_siska


def check_link(url,time,score_one,score_two,period,minute,checker,sl):
    print(url)
    print("SCOREEEE",score_one,score_two)
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(desired_capabilities=caps,options=options)
    browser.get(url)
    browser.implicitly_wait(1)
    team_home = browser.find_elements(By.CSS_SELECTOR, "a.participant__participantName")[0].get_attribute(
            "href") + "results/"
    team_away = browser.find_elements(By.CSS_SELECTOR, "a.participant__participantName")[1].get_attribute(
            "href") + "results/"
    title = browser.find_element(By.CSS_SELECTOR, ".tournamentHeader__country").text
    print(title)
    def separator(matches):
        match_list = list()
        for i in matches:
            line = i.text
            # print(line)
            if "(" in line or "Awrd" in line or "Abn" in line or "WO" in line:
                continue
            if len([i for i in line.split() if i.isdigit()]) < 6:
                continue
            match_list.append(line.split())
        return match_list

    def get_data(browser,link):
        browser.get(link)
        dataset = browser.find_elements(By.CSS_SELECTOR, "[id^='g_3']")
        matches = separator(dataset)
        team = browser.find_element(By.CSS_SELECTOR, "div.heading__name").get_attribute("innerHTML")
        return matches,team

    def forming(browser, link1, link2):  # NEED ADD TYPE SPORT AND FIXABLE CSS SELECTOR
        match_list_home, team1 = get_data(browser,link1)
        match_list_away, team2 = get_data(browser,link2)
        return match_list_home, match_list_away, team1, team2

    games = forming(browser, team_home, team_away)

    team1_name = games[2].split()
    team2_name = games[3].split()

    def separation_home_away(team_, all_matches):
        home_matches = list()
        away_matches = list()
        waste = ["W", "U18","U19", "U20", "U21", "U23"]  # WASTE - U20 and another juniors and woman champs//
        for i in waste:
            if i in team_:
                team_ = [j for j in team_ if j not in waste]
        print(team_)
        for k in all_matches:
            i = [j for j in k[:len(k) - 1] if j not in waste] + k[-1:]
            x = i.index(team_[len(team_) - 1])
            if i[x + 1].isdigit():
                away_matches.append(i)
            elif "(" in i[x + 1] and i[x + 2].isdigit():
                away_matches.append(i)
            else:
                home_matches.append(i)
        return home_matches, away_matches

    team1_home, team1_away = separation_home_away(team1_name, games[0])
    team2_home, team2_away = separation_home_away(team2_name, games[1])

    results_1 = games[0]
    results_2 = games[1]

    def get_scores(results):
        scorelines = []
        for match in results:
            if len([ i for i in match if i.isdigit() ]) < 10:
                continue
            if "AOT" in match:
                scoreline = match[-13:-1]
            else:
                scoreline = match[-11:-1]
            scorelines.append(list(map(int,scoreline)))
        return scorelines

    def quater_one(scores):
        total = []
        for i in scores:
            total.append(sum( [ int(j) for j in i[2:4] ]) )
        return total

    def quater_two(scores):
        return [sum([int(j) for j in i[4:6]]) for i in scores]

    def quater_three(scores):
        return [sum([int(j) for j in i[6:8]]) for i in scores]

    def quater_four(scores):
        return [sum([int(j) for j in i[8:10]]) for i in scores]


    def total(scores):
        return [sum([int(j) for j in i[2:10]]) for i in scores]


    team1_1q = quater_one(get_scores(team1_home+team1_away))
    team2_1q = quater_one(get_scores(team2_home+team2_away))
    team1_2q = quater_two(get_scores(team1_home+team1_away))
    team2_2q = quater_two(get_scores(team2_home+team2_away))
    team1_3q = quater_three(get_scores(team1_home+team1_away))
    team2_3q = quater_three(get_scores(team2_home+team2_away))
    team1_4q = quater_four(get_scores(team1_home+team1_away))
    team2_4q = quater_four(get_scores(team2_home+team2_away))
    team1_total = total(get_scores(team1_home+team1_away))
    team2_total = total(get_scores(team2_home+team2_away))

    team1_1q_home = quater_one(get_scores(team1_home))
    team2_1q_away = quater_one(get_scores(team2_away))
    team1_2q_home = quater_two(get_scores(team1_home))
    team2_2q_away = quater_two(get_scores(team2_away))


    print("TEAM1 ave ::",sorted(team1_1q), len(team1_1q),'<-len', round(mean(team1_1q),1),'<-mean' )
    print("TEAM2 ave ::",sorted(team2_1q), len(team2_1q),'<-len', round(mean(team2_1q),1),'<-mean' )


    index1 = len(team1_1q) // 10
    index2 = len(team2_1q) // 10
    print('index1:: ',index1)
    print('index2::', index2)


    first_t1 = sorted(team1_1q)[index1]
    first_t2 = sorted(team2_1q)[index2]
    second_t1 = sorted(team1_2q)[index1]
    second_t2 = sorted(team2_2q)[index2]
    third_t1 = sorted(team1_3q)[index1]
    third_t2 = sorted(team2_3q)[index2]
    fourth_t1 = sorted(team1_4q)[index1]
    fourth_t2 = sorted(team2_4q)[index2]

    first_t1_home = sorted(team1_1q_home)[2]
    first_t2_away = sorted(team2_1q_away)[2]
    second_t1_home = sorted(team1_2q_home)[2]
    second_t2_away = sorted(team2_2q_away)[2]

    ave_first = round(((first_t1 + first_t2) / 2), 1)
    ave_second = round(((second_t1 + second_t2) / 2), 1)
    ave_third = round(((third_t1 + third_t2) / 2), 1)
    ave_fourth = round(((fourth_t1 + fourth_t2) / 2), 1)

    ave_first_real = round(((first_t1_home + first_t2_away) / 2), 1)
    ave_second_real = round(((second_t1_home + second_t2_away) / 2), 1)

    mean_first = round(mean(team1_2q + team2_2q),1)
    mean_second = round(mean(team1_2q + team2_2q),1)
    mean_third = round(mean(team1_3q + team2_3q), 1)
    mean_fourth = round(mean(team1_4q + team2_4q), 1)

    mean_1q_t1 = round(mean(team1_1q))
    mean_1q_t2 = round(mean(team2_1q))
    mean_common_quarter1 = round((mean_1q_t1 + mean_1q_t2) / 2, 1)

    mean_2q_t1 = round(mean(team1_2q))
    mean_2q_t2 = round(mean(team2_2q))
    mean_common_quarter2 = round((mean_2q_t1 + mean_2q_t2) / 2, 1)

    print(ave_first)

    print(first_t1)
    print(first_t2)
    current_score = f"{score_one}:{score_two}"

    def nice_to_over(score_one, score_two, mean_quarter, ave, time):

        per_min = mean_quarter / 10 # not for asian and us champs
        current = score_one + score_two
        remain = 10.5 - time
        remain_goals = remain * per_min

        if remain_goals + current - ave  <= 2:
            return True

        return False


    """WINSTREAK  PROCESSING"""""


    team1_results_home = get_scores(team1_home)
    team1_results_away = get_scores(team1_away)
    team2_results_home = get_scores(team2_home)
    team2_results_away = get_scores(team2_away)


    def home_win_one_of3(scores):
        win, matches = 0, len(scores)

        for data in scores:
            if data[2]>data[3] or data[4]>data[5] or data[6]>data[7]:
                win+=1
        return win, matches

    def away_win_one_of3(scores):
        win, matches = 0, len(scores)

        for data in scores:
            if data[3]>data[2] or data[5]>data[4] or data[7]>data[6]:
                win+=1
        return win, matches


    def home_win_all3(data):
        win, matches = 0, len(data)

        for match in data:
            if match[2]>match[3] and match[4] > match[5] and match[6] > match[7]:
                win += 1

        return win, matches


    def away_win_all3(data):
        win, matches = 0, len(data)

        for match in data:
            if match[3] > match[2] and match[5] > match[4] and match[7] > match[6]:
                win += 1

        return win, matches


    def home_lose_one_of3(data):
        lose, matches =0, len(data)

        for scores in data:
            if scores[2]<scores[3] or scores[4]<scores[5] or scores[6]<scores[7]:
                lose += 1
        return lose, matches


    def away_lose_one_of3(data):
        lose, matches =0, len(data)

        for scores in data:
            if scores[3] < scores[2] or scores[5] < scores[4] or scores[7] < scores[6]:
                lose += 1
        return lose, matches


    team1_win1of3_home, team1_win1of3_away = home_win_one_of3(team1_results_home), away_win_one_of3(team1_results_away)
    team1_win3of3_home, team1_win3of3_away = home_win_all3(team1_results_home), away_win_all3(team1_results_away)
    team1_lose1of3_home, team1_lose1of3_away = home_lose_one_of3(team1_results_home), away_lose_one_of3(team1_results_away)

    team2_win1of3_home, team2_win1of3_away = home_win_one_of3(team2_results_home), away_win_one_of3(team2_results_away)
    team2_win3of3_home, team2_win3of3_away = home_win_all3(team2_results_home), away_win_all3(team2_results_away)
    team2_lose1of3_home, team2_lose1of3_away = home_lose_one_of3(team2_results_home), away_lose_one_of3(team2_results_away)


    def case_3_home(data1, data2, data3, data4): # data1 =t1 win 1 of 3 home, data2 =t2 lose 1 of 3 away, data3 =t1 win 1 of 3 away, data4 = t2 lose 1 of 3 home
        if data1[1] - data1[0]<3 and data1[1]>18:
            if data2[1] - data2[0]<3 and data2[1]>15:
                print(url)
                print("TEAM1 WIN ONE OF 3 QWTS (INCLUDING LOSES OPPONENTS)")
                print(data1,data2)
                approx_win = round((data1[0]+data3[0]) / (data1[1] + data3[1]), 2) * 100
                approx_lose = round((data2[0] + data4[0]) / (data2[1] + data4[1]), 2) * 100

                msg = (f'Real disposal:{data1}{data2}',
                      f'Vice versa:{data3}{data4}',
                      f'win: {approx_win}%  lose: {approx_lose}%')

                return True, msg
        return False, '-'

    def case_3_away(data1, data2, data3, data4): # data1 =t2 win 1 of 3 away, data2 = t1 lose 1 of 3 home, data3 = t2 win 1 of 3 home, data4 = t1 lose 1 of 3 away
        if data1[1] - data1[0]<3 and data1[1]>18: # team win one of 3
            if data2[1] - data2[0]<3 and data2[1]>15: # team lose one of 3
                print(url)
                print("TEAM2 WIN ONE OF 3 QWTS (INCLUDING LOSES OPPONENTS)")
                print(data1,data2)
                approx_win = round((data1[0] + data3[0]) / (data1[1] + data3[1]), 2) * 100
                approx_lose = round((data2[0] + data4[0]) / (data2[1] + data4[1]), 2)* 100

                msg = (f'Real disposal:{data1}{data2}',
                      f'Vice versa:{data3}{data4}',
                      f'win: {approx_win}%  lose: {approx_lose}%')


                return True, msg
        return False, '-'



    def home_win_one_of4(scores):
        win, matches = 0, len(scores)

        for data in scores:
            if data[2]>data[3]+2 or data[4]>data[5]+2 or data[6]>data[7]+2 or data[8]>data[9]+2:
                win+=1
        return win, matches


    def away_win_one_of4(scores):
        win, matches = 0, len(scores)

        for data in scores:
            if data[3]>data[2]+2 or data[5]>data[4]+2 or data[7]>data[6]+2 or data[9]>data[8]+2:

                win+=1
        return win, matches

    def home_lose_one_of4(data):
        lose, matches =0, len(data)

        for scores in data:
            if scores[2]+2<scores[3] or scores[4]+2<scores[5] or scores[6]+2<scores[7] or scores[8]+2<scores[9]:
                lose += 1
        return lose, matches


    def away_lose_one_of4(data):
        lose, matches =0, len(data)

        for scores in data:
            if scores[3]+2 < scores[2] or scores[5]+2 < scores[4] or scores[7]+2 < scores[6] or scores[9]+2 < scores[8]:
                lose += 1
        return lose, matches


    def case_4_home(data1, data2, data3, data4):  # data1 =t1 win 1 of 3 home, data2 =t2 lose 1 of 3 away, data3 =t1 win 1 of 3 away, data4 = t2 lose 1 of 3 home
        if data1[1] - data1[0]<3 and data1[1]>18:
            if data2[1] - data2[0]<3 and data2[1]>=15:
                print(url)
                print("TEAM1 WIN ONE OF 4 QWTS")
                print('Normal :: ',data1, data2)
                print('Vise versa :: ', data3, data4)
                approx_win = round((data1[0]+data3[0]) / (data1[1] + data3[1]), 2) * 100
                approx_lose = round((data2[0] + data4[0]) / (data2[1] + data4[1]), 2) * 100

                msg = (f'REAL DISPOSAL::   {data1} {data2}',
                      f'VICE VERSA::  {data3} {data4}',
                      f'WIN::: {approx_win}%    LOSE::: {approx_lose}%')

                return True, msg
        return False, '-'

    def case_4_away(data1, data2, data3, data4): # data1 =t2 win 1 of 3 away, data2 = t1 lose 1 of 3 home, data3 = t2 win 1 of 3 home, data4 = t1 lose 1 of 3 away
        if data1[1] - data1[0]<3 and data1[1]>18:
            if data2[1] - data[2]<3 and data2[1]>=15:
                print(url)
                print("TEAM2 WIN ONE OF 4 QWTS")
                print('Normal :: ',data1, data2)
                print('Vise versa :: ', data3, data4)
                approx_win = round((data1[0]+data3[0]) / (data1[1] + data3[1]), 2) * 100
                approx_lose = round((data2[0] + data4[0]) / (data2[1] + data4[1]), 2) * 100

                msg = (f'REAL DISPOSAL::   {data1} {data2}',
                      f'VICE VERSA::  {data3} {data4}',
                      f'WIN:: {approx_win}%    LOSE:: {approx_lose}%')

                return True, msg
        return False, '-'

    team1_win1of4_home, team1_win1of4_away = home_win_one_of4(team1_results_home), away_win_one_of4(team1_results_away)
    team1_lose1of4_home, team1_lose1of4_away = home_lose_one_of4(team1_results_home), away_lose_one_of4(team1_results_away)
    team2_win1of4_home, team2_win1of4_away = home_win_one_of4(team2_results_home), away_win_one_of4(team2_results_away)
    team2_lose1of4_home, team2_lose1of4_away = home_lose_one_of4(team2_results_home), away_lose_one_of4(team2_results_away)


    occasionAtHome_3 = case_3_home(team1_win1of3_home, team2_lose1of3_away, team1_win1of3_away, team2_lose1of3_home)
    occasionAway_3 = case_3_away(team2_win1of3_away, team1_lose1of3_home, team2_win1of3_home, team1_lose1of3_away)

    occasionAtHome_4 = case_4_home(team1_win1of4_home, team2_lose1of4_away, team1_win1of4_away, team2_lose1of4_home)
    occasionAway_4 = case_4_home(team2_win1of4_away, team1_lose1of4_home, team2_win1of4_home, team1_lose1of4_away)

    print(occasionAtHome_3)
    print(occasionAway_3)

    print(occasionAtHome_4)
    print(occasionAway_4)

    def look_at_first(prev, data, mean_1q):
        previous_quarter = sum(prev[:2]) # current result of first quarter


        def get_enter(mean):
            """
            Sample : ([38, 44], [[34, 37], [45, 48]], [33, 49])
            """
            value = round(mean)
            normal = [value - 3, value + 3]
            deviation = [[normal[0] - 4, normal[0] - 1], [normal[1] + 1, normal[1] + 4]]
            exrtemum = [deviation[0][0] - 1, deviation[1][1] + 1]
            return normal, deviation, exrtemum

        normal, deviation, extremum = get_enter(mean_1q)
        normal_list, deviation_list_low, deviation_list_up,\
            extremum_list_up,extremum_list_low = list(), list(), list(), list(), list()
        print(normal, deviation, extremum)

        for match in data:
            quarter_was = sum(map(int, match[2:4]))
            second_quarter = sum(map(int, match[4:6]))

            if normal[0] <= previous_quarter <= normal[1]:
                if normal[0] <= quarter_was <= normal[1]:
                    normal_list.append(second_quarter)

            if  deviation[0][0] <= previous_quarter <= deviation[0][1]:
                if deviation[0][0] <= quarter_was <= deviation[0][1]:
                    deviation_list_low.append(second_quarter)

            if  deviation[1][0] <= previous_quarter <= deviation[1][1]:
                if deviation[1][0] <= quarter_was <= deviation[1][1]:
                    deviation_list_up.append(second_quarter)

            if  previous_quarter <= extremum[0]:
                if quarter_was <= extremum[0]:
                    extremum_list_low.append(second_quarter)

            if  previous_quarter >= extremum[1]:
                if quarter_was >= extremum[1]:
                    extremum_list_up.append(second_quarter)

        return extremum_list_low, deviation_list_low, normal_list, deviation_list_up, extremum_list_up


    rating_1 = look_at_first(sl[:2], get_scores(results_1), mean_1q_t1)
    rating_2 = look_at_first(sl[:2], get_scores(results_2), mean_1q_t2)

    prior_quater = sorted(list(chain.from_iterable(rating_1 + rating_2)))
    print(prior_quater)

    def show_comparison(ave, mean, prior):
        ave_more = 0
        mean_more = 0
        for i in prior:
            if i >= ave:
                ave_more += 1
                if i >= mean:
                    mean_more += 1
        return f'|Min:{min(prior)}| {mean_more} / {ave_more} / {len(prior)}'


    def bet_string(list):
        part1 = sorted(list)[:5]
        part2 = sorted(list)[-5:]
        return f'{part1}<{round(mean(list), 1)}>{part2}'

    if checker == 1 and nice_to_over(score_one, score_two, mean_common_quarter1, ave_first, minute) == True:
        bet = (title,"TIME :"+str(time),"SCORE: "+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
            "1 QUARTER >>>",
            "1:" + bet_string(team1_1q),
            "2:" + bet_string(team2_1q),
            "lowAve:: " + str(ave_first),
            'FOR HOME/AWAY::',
            "1:" + bet_string(team1_1q_home),
            "2:" + bet_string(team2_1q_away),
            "lowAve:: " + str(ave_first_real),
                )
        bet_siska(bet)

    if checker == 2 and nice_to_over(sl[2], sl[3], mean_common_quarter2, ave_second, minute) == True:
        add_info = show_comparison(ave_second, mean_second, prior_quater)
        bet = (title,"TIME:"+str(time),"SCORE: " + ' '.join(map(str,sl))+ "(" + current_score+ ")",
            ' '.join(map(str,team1_name)),
            ' '.join(map(str,team2_name)),
            "2 QUARTER >>>",
            "1:" + bet_string(team1_2q),
            "2:" + bet_string(team2_2q),
            "lowAve:: " + str(ave_second),
            "Add. info:: "+ add_info,
            'FOR HOME/AWAY::',
            "1:" + bet_string(team1_2q_home),
            "2:" + bet_string(team2_2q_away),
            "lowAve:: " + str(ave_second_real),
                )
        bet_siska(bet)


    if checker == 11 and occasionAway_3[0] == True:
        bet = (title,"TIME:"+str(time),"SCORE:"+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
                ' TEAM2(AWAY) TO WIN 3 QUARTER ',
               *occasionAway_3[1]
                )
        bet_siska(bet)

    if checker == 111 and occasionAway_4[0] == True:
        bet = (title,"TIME:"+str(time),"SCORE:"+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
                ' TEAM2(AWAY) TO WIN 4 QUARTER ',
               *occasionAway_4[1]
                )
        bet_siska(bet)

    if checker == 22 and occasionAtHome_3[0] == True:
        bet = (title,"TIME:"+str(time),"SCORE:"+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
                ' TEAM1(HOME) TO WIN 3 QUARTER ',
               *occasionAtHome_3[1]
                )
        bet_siska(bet)

    if checker == 222 and occasionAtHome_4[0] == True:
        bet = (title,"TIME:"+str(time),"SCORE:"+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
                ' TEAM1(HOME) TO WIN 4 QUARTER ',
               *occasionAtHome_4[1]
                )
        bet_siska(bet)

    print("End of iteration...", checker)
    print()








