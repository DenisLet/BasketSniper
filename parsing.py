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
            "href") + "/results/"
    team_away = browser.find_elements(By.CSS_SELECTOR, "a.participant__participantName")[1].get_attribute(
            "href") + "/results/"
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
        waste = ["W", "U18", "U20", "U21", "U23"]  # WASTE - U20 and another juniors and woman champs//
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
            scorelines.append(scoreline)

        return scorelines

    def results(scores,loc,timeline):
        team_scored = []
        team_conceded = []
        if period == "total":
            x, y = 0, 1
        if period == "first":
            x, y = 2, 3
        if period == "second":
            x, y = 4, 5
        if period == "third":
            x, y = 6, 7
        if period == "fourth":
            x, y = 8, 9


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

    ave_first = round(((first_t1 + first_t2) / 2), 1)
    ave_second = round(((second_t1 + second_t2) / 2), 1)
    ave_third = round(((third_t1 + third_t2) / 2), 1)
    ave_fourth = round(((fourth_t1 + fourth_t2) / 2), 1)

    mean_first = round(mean(team1_2q + team2_2q),1)
    mean_second = round(mean(team1_2q + team2_2q),1)
    mean_third = round(mean(team1_3q + team2_3q), 1)
    mean_fourth = round(mean(team1_4q + team2_4q), 1)

    mean_1q_t1 = round(mean(team1_1q))
    mean_1q_t2 = round(mean(team2_1q))

    print(ave_first)

    print(first_t1)
    print(first_t2)
    current_score = f"{score_one}:{score_two}"

    def nice_to_over(score_one,score_two,data1,data2,ave):
        mean_total = round(mean(data1+data2),1)
        score = score_one+score_two
        if ave < 20:
            print("ave- ", ave)
            return False
        if ave <= 25 and score > 6:
            print('ave- ',ave,'score',score)
            return False
        if ave - sorted(data1)[0] > 10 or ave - sorted(data2)[0] > 10 :
            print('difference 1>>2:: ', ave - sorted(data1)[0],ave - sorted(data2)[0] )
            return False
        else:
            print('All is fine!!!')
            return True



    def win_one_of4(data,loc):
        line = get_scores(data)
        win, loss, count = 0, 0, 0
        if loc == 'home':
            for qwt in line:
                if qwt[2] > qwt[3] or qwt[4] > qwt[5] or qwt[6] > qwt[7] or qwt[8] > qwt[9]:
                    win += 1
                else:
                    loss += 1
                count += 1
            print("HOME RESULT(WIN/percentage)", f"{win}/{count}")

        if loc  == 'away':
            for qwt in line:
                if qwt[2] < qwt[3] or qwt[4] < qwt[5] or qwt[6] < qwt[7] or qwt[8] < qwt[9]:
                    win += 1
                else:
                    loss += 1
                count += 1
            print("AWAY RESULT(WIN/percentage)",f"{win}/{count}")
        if count == 0 :
            count = 1
        if count >= 15 and count - win <2: return True
        else: return False


    def win_all_of4(data,loc):
        line = get_scores(data)
        win, loss, count = 0, 0, 0
        if loc == 'home':
            for qwt in line:
                if qwt[2] >= qwt[3] and qwt[4] >= qwt[5] and qwt[6] >= qwt[7] and qwt[8] >= qwt[9]:
                    win += 1
                else:
                    loss += 1
                count += 1
            print("HOME RESULT(WIN/percentage)", f"{win}/{count}")

        if loc  == 'away':
            for qwt in line:
                if qwt[2] <= qwt[3] and qwt[4] <= qwt[5] and qwt[6] <= qwt[7] and qwt[8] <= qwt[9]:
                    win += 1
                else:
                    loss += 1
                count += 1
            print("AWAY RESULT(WIN/percentage)",f"{win}/{count}")

        if count == 0:
            count = 1
        if count >= 15 and win <2: return True
        else: return False

    def win_one_of3(data, loc):
        line = get_scores(data)
        win, loss, count = 0, 0, 0
        if loc == 'home':
            for qwt in line:
                if qwt[2] > qwt[3] or qwt[4] > qwt[5] or qwt[6] > qwt[7]:
                    win += 1
                else:
                    loss += 1
                count += 1
            print("HOME RESULT (WIN ONE OF 3Q) ", f"{win}/{count}")

        if loc == 'away':
            for qwt in line:
                if qwt[2] < qwt[3] or qwt[4] < qwt[5] or qwt[6] < qwt[7]:
                    win += 1
                else:
                    loss += 1
                count += 1
            print("AWAY RESULT(WIN ONE OF 3Q) ", f"{win}/{count}")

        if count == 0:
            count = 1
        if count >= 15 and count - win <2:
            return  True
        else: return False

    def win_all_of3(data, loc):
        line = get_scores(data)
        win, loss, count = 0, 0, 0
        if loc == 'home':
            for qwt in line:
                if qwt[2] >= qwt[3] and qwt[4] >= qwt[5] and qwt[6] >= qwt[7]:
                    win += 1
                else:
                    loss += 1
                count += 1
            print("HOME RESULT(WIN ALL OF 3Q) ", f"{win}/{count}")

        if loc == 'away':
            for qwt in line:
                if qwt[2] <= qwt[3] and qwt[4] <= qwt[5] and qwt[6] <= qwt[7]:
                    win += 1
                else:
                    loss += 1
                count += 1
            print("AWAY RESULT(WIN ALL OF 3Q) ", f"{win}/{count}")

        if count == 0:
            count == 1
        if count >= 15 and win < 2:
            return  True, round(win * 100 / count,1)
        else: return False

    condition3_team1, condition3_team2 = False, False
    condition4_team1, condition4_team2 = False, False


    t1h_win_one3 = win_one_of3(team1_home, loc = 'home')
    t1a_win_one3 = win_one_of3(team1_away, loc = 'away')
    t1h_win_all3 = win_all_of3(team1_home, loc = 'home')
    t1a_win_all3 = win_all_of3(team1_away, loc = 'away')
    print('-'*50)
    t2h_win_one3 = win_one_of3(team2_home, loc = 'home')
    t2a_win_one3 = win_one_of3(team2_away, loc = 'away')
    t2h_win_all3 = win_all_of3(team2_home, loc = 'home')
    t2a_win_all3 = win_all_of3(team2_away, loc = 'away')
    print()
    t1h_win_one4 = win_one_of4(team1_home, loc = 'home')
    t1a_win_one4 = win_one_of4(team1_away, loc = 'away')
    t1h_win_all4 = win_all_of4(team1_home, loc = 'home')
    t1a_win_all4 = win_all_of4(team1_away, loc = 'away')
    print('-'*50)
    t2h_win_one4 = win_one_of4(team2_home, loc = 'home')
    t2a_win_one4 = win_one_of4(team2_away, loc = 'away')
    t2h_win_all4 = win_all_of4(team2_home, loc = 'home')
    t2a_win_all4 = win_all_of4(team2_away, loc = 'away')


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




    def compare_quarter(previous,data1,data2,sum_mean,ave,quarter):

        """  compare previous quarter result and futher quarter
            and return bool for condition and meaning to display """


        more_mean, less_mean = 0, 0
        more_ave, less_ave = 0, 0
        count_mean, count_ave = 0, 0
        count1 = 0
        if quarter == 2:
            previous_quarter = sum(previous[:2])
            for i in data1:
                previous_quarter_was = sum(map(int, i[2:4]))
                second_qwt = sum(map(int,i[4:6]))
                if previous_quarter_was >= previous_quarter:
                    count1 += 1
                    if sum(map(int,i[4:6])) >= sum_mean:
                        more_mean += 1
                        count_mean += 1
                    if second_qwt >= ave:
                        more_ave += 1
                        count_ave += 1

            for i in data2:
                previous_quarter_was = sum(map(int, i[2:4]))
                second_qwt = sum(map(int,i[4:6]))
                if previous_quarter_was >= previous_quarter:
                    count1 += 1
                    if sum(map(int,i[4:6])) >= sum_mean:
                        more_mean += 1
                        count_mean += 1
                    if second_qwt >= ave:
                        more_ave += 1
                        count_ave += 1

        if quarter == 3:
            previous_quarter1 = sum(previous[:2])
            previous_quarter2 = sum(previous[2:4])
            for i in data1:
                previous_quarter1_was = sum(map(int, i[2:4]))
                previous_quarter2_was = sum(map(int, i[4:6]))
                third_qwt = sum(map(int,i[6:8]))
                if previous_quarter1_was >= previous_quarter1 and previous_quarter2_was >= previous_quarter2:
                    count1 += 1
                    if sum(map(int,i[6:8])) >= sum_mean:
                        more_mean += 1
                        count_mean += 1
                    if third_qwt >= ave:
                        more_ave += 1
                        count_ave += 1

            for i in data2:
                previous_quarter1_was = sum(map(int, i[2:4]))
                previous_quarter2_was = sum(map(int, i[4:6]))
                third_qwt = sum(map(int,i[6:8]))
                if previous_quarter1_was >= previous_quarter1 and previous_quarter2_was >= previous_quarter2:
                    count1 += 1
                    if sum(map(int,i[6:8])) >= sum_mean:
                        more_mean += 1
                        count_mean += 1
                    if third_qwt >= ave:
                        more_ave += 1
                        count_ave += 1

    def up_to(value, matches):
        prev_list = list()
        more3 = 0
        more4 = 0
        for i in matches:
            qwt1, qwt2, qwt3, qwt4 = sum(map(int, i[2:4])), sum(map(int, i[4:6])), sum(map(int, i[6:8])), sum(
                map(int, i[8:]))
            if qwt1 > value or qwt2 > value or qwt3 > value:
                more3 += 1
            if qwt1 > value or qwt2 > value or qwt3 > value or qwt4 > value:
                more4 += 1
            else:
                print(i)
        print('MORE IN 3 QWT:: ', more3)
        print('MORE IN 4 QWT:: ', more4)
        print('ALL:: ', len(matches))
        return more3, more4, len(matches)


        print("COUNT BOTH: ", count1)
        print("COUNT MORE MEAN: ", count_mean)
        print("COUNT MORE AVE: ", count_ave)
        print("MEAN SCORES: ", sum_mean)


        if count1 > 25 and count_ave * 100 / count1 >= 90:
            return (True, f'{count_mean}/{count_ave}/{count1}')
        else:
            return (False, f'{count_mean}/{count_ave}/{count1}')



    if [t1h_win_one3, t1a_win_one3, t2h_win_all3, t2a_win_all3].count(True) > 2:
        condition3_team1 = True

    if [t2h_win_one3, t2a_win_one3, t1h_win_all3, t1a_win_all3].count(True) > 2:
        condition3_team2 = True

    if [t1h_win_one4, t1a_win_one4, t2h_win_all4, t2a_win_all4].count(True) > 2:
        condition4_team1 = True

    if [t2h_win_one4, t2a_win_one4, t1h_win_all4, t1a_win_all4].count(True) > 2:
        condition4_team2 = True


    print()
    print("POSITIVE CONDITION FOR TEAM1 (3Q to WIN): ", condition3_team1)
    print("POSITIVE CONDITION FOR TEAM1 (4Q to WIN): ", condition4_team1)
    print("POSITIVE CONDITION FOR TEAM2 (3Q to WIN): ", condition3_team2)
    print("POSITIVE CONDITION FOR TEAM2 (4Q to WIN): ", condition4_team2)



    # print(nice_to_over(score_one,score_two,team1_1q,team2_1q,mean_first))





    def bet_string(list):
        part1 = sorted(list)[:5]
        part2 = sorted(list)[-5:]
        return f'{part1}<{round(mean(list), 1)}>{part2}'

    if checker == 1 and nice_to_over(score_one,score_two,team1_1q,team2_1q,ave_first) == True:
        bet = (title,"TIME :"+str(time),"SCORE: "+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
            "1 QUARTER >>>",
            "1:" + bet_string(team1_1q),
            "2:" + bet_string(team2_1q),
            "lowAve:: " + str(ave_first)
                )
        bet_siska(bet)

    if checker == 2:
        add_info = show_comparison(ave_second, mean_second, prior_quater)
        bet = (title,"TIME:"+str(time),"SCORE: " + ' '.join(map(str,sl))+ "(" + current_score+ ")",
            ' '.join(map(str,team1_name)),
            ' '.join(map(str,team2_name)),
            "2 QUARTER >>>",
            "1:" + bet_string(team1_2q),
            "2:" + bet_string(team2_2q),
            "lowAve:: " + str(ave_second),
            "Add. info:: "+ add_info
                )
        bet_siska(bet)

    if checker == 3:
        add_info = compare_quarter(sl,get_scores(games[0]), get_scores(games[1]), mean_third, ave_third, quarter = 3 )[1]
        bet = (title,"TIME:"+str(time),"SCORE:" + ' '.join(map(str,sl))+ "(" + current_score+ ")",
            ' '.join(map(str,team1_name)),
            ' '.join(map(str,team2_name)),
            "3 QUARTER >>>",
            "1:" + bet_string(team1_3q),
            "2:" + bet_string(team2_3q),
            "lowAve:: " + str(ave_third),
            "Add. info:: " + add_info
                )
        bet_siska(bet)

    if checker == 4:
        bet = (title,"TIME:"+str(time),"SCORE:"+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
            "4 QUARTER >>>",
            "1:" + bet_string(team1_4q),
            "2:" + bet_string(team2_4q),
            "lowAve:: " + str(ave_fourth)
                )
        bet_siska(bet)


    if checker == 11 and condition3_team2 == True:
        bet = (title,"TIME:"+str(time),"SCORE:"+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
                ' TEAM2(AWAY) TO WIN 3 QUARTER '
                )
        bet_siska(bet)

    if checker == 111 and condition4_team2 == True:
        bet = (title,"TIME:"+str(time),"SCORE:"+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
                ' TEAM2(AWAY) TO WIN 4 QUARTER '
                )
        bet_siska(bet)

    if checker == 22 and condition3_team1 == True:
        bet = (title,"TIME:"+str(time),"SCORE:"+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
                ' TEAM1(HOME) TO WIN 3 QUARTER '
                )
        bet_siska(bet)

    if checker == 222 and condition4_team1 == True:
        bet = (title,"TIME:"+str(time),"SCORE:"+current_score, ' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
                ' TEAM1(HOME) TO WIN 4 QUARTER '
                )
        bet_siska(bet)

    if checker in range(32,40):

        add_info1 = up_to(checker, get_scores(results_1))
        add_info2 = up_to(checker, get_scores(results_2))

        add_info = f'Value:{checker} 3Q: {add_info1[0]}/{add_info1[2]}  {add_info2[0]}/{add_info2[2]}'
        bet = (title, "TIME:" + str(time), "SCORE:" + ' '.join(map(str, sl)) + "(" + current_score + ")",
               ' '.join(map(str, team1_name)),
               ' '.join(map(str, team2_name)),
               "3 QUARTER >>>",
               "1:" + bet_string(team1_3q),
               "2:" + bet_string(team2_3q),
               "lowAve:: " + str(ave_third),
               add_info
               )
        bet_siska(bet)


    print("End of iteration...", checker)
    print()








