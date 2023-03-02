from scan import current_moment, get_link, handling
from parsing import check_link
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from send import errormsg, make_mistake, startmsg
from selenium.common import exceptions
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_argument('--mute-audio')
browser = webdriver.Chrome(options=options)
browser.get("https://www.basketball24.com/")
switch_to_live = browser.find_element(By.CSS_SELECTOR, "div.filters__tab:nth-child(2) > div:nth-child(2)")
switch_to_live.click()
sleep(1)

period1_list = set()
period2_list = set()
winstreak_list3 = set()
winstreak_list4 = set()

def try_it_out(line):
    if line[0]>line[1] and line[2]>line[3]:
        if  line[4]>line[5]:
            print("TEAM1 WON THREE PERIODS IN ROW")
            return 111
        print('TEAM1 WON TWO PERIODS IN ROW')
        return 11

    if line[0]<line[1] and line[2]<line[3]:
        if line[4]<line[5]:
            print("TEAM2 WON THREE PERIODS IN ROW")
            return 222
        print('TEAM2 WON TWO PERIODS IN ROW')
        return 22
    else:
        return "***** ORDINARY MATCH... *****"

def take_it_higher3(line):
    normalize, qwt_1, qwt_2, values_list  = range(32,40), sum(line[:2]), sum(line[2:4]), list()
    for value in normalize:
        if qwt_1 <= value and qwt_2 <= value:
            print('TWO QWT LESS OR EQUAL:: ', value)
            values_list.append(value)

    return min(values_list) if len(values_list) != 0 else False

while True:
    try:
        matches = browser.find_elements(By.CSS_SELECTOR,"[id^='g_3']")
        for i in matches:
            try:
                time,score_one,score_two,score_line = handling(i)
                period,minute = current_moment(time)
                print()
                current_first = sum(score_line[:2])
                current_second = sum(score_line[2:4])
                current_third = sum(score_line[4:6])
                current_fourth = sum(score_line[6:])
                current_score = score_one + score_two
                print('PERIOD TO CHECK: ',period)
                print('MINUTE TO CHECK: ',minute)
                print('1ST: ',current_first,score_line[0],score_line[1])
                print('2ND: ',current_second,score_line[2],score_line[3])
                print('3RD: ', current_third,score_line[4],score_line[5])
                print('4TH: ',current_fourth,score_line[6],score_line[7])
                print("CURRENT : ", current_first,current_second,current_third,current_fourth)
                print("EACH : ", score_line[0],score_line[1],score_line[2],score_line[3],score_line[4],score_line[5],score_line[6],score_line[7])
                print()

                if  period == 5:
                    continue

                if period == 1  and ((current_score < 9 and minute >= 4) or (minute >= 5 and current_score < 12)
                    or (current_score < 15 and minute >=6)):
                    link = (get_link(i), minute)
                    print("1"*50)
                    if link in period1_list:
                        continue
                    period1_list.add(link)
                    checker = 1
                    check_link(link[0], time, score_one, score_two, period, minute, checker, score_line)
                    continue

                if period == 2 and ((current_second < 8 and minute >=4) or (current_second<11 and minute>=5)
                    or (current_score < 15 and minute >=6)):
                    link2 = (get_link(i), minute)
                    print("2"*50)
                    if link2 in period2_list:
                        continue
                    period2_list.add(link2)
                    checker = 2
                    check_link(link2[0], time, score_line[2], score_line[3], period, minute, checker, score_line)
                    continue


                if period == "HT" or period == 4 or (period == 3 and minute == 10):
                    winstreak_ = try_it_out(score_line)
                    print('WINSTREAK: ', winstreak_)

                    if winstreak_ == 11 and period == 'HT':
                        link11 = get_link(i)
                        if link11 in winstreak_list3:
                            continue
                        winstreak_list3.add(link11)
                        checker = 11
                        check_link(link11, time, score_one, score_two, period, minute, checker, score_line)

                    if winstreak_ == 111:
                        link111 = get_link(i)
                        if link111 in winstreak_list4:
                            continue
                        winstreak_list4.add(link111)
                        checker = 111
                        check_link(link111, time, score_one, score_two, period, minute, checker, score_line)

                    if winstreak_ == 22 and period == 'HT':
                        link22 = get_link(i)
                        if link22 in winstreak_list3:
                            continue
                        winstreak_list3.add(link22)
                        checker = 22
                        check_link(link22, time, score_one, score_two, period, minute, checker, score_line)

                    if winstreak_ == 222:
                        link222 = get_link(i)
                        if link222 in winstreak_list4:
                            continue
                        winstreak_list4.add(link222)
                        checker = 222
                        check_link(link222, time, score_one, score_two, period, minute, checker, score_line)

                # totalsteak_up = take_it_higher3(score_line)
                # print('TOTALSTREAK UP: ', totalsteak_up)
                # if period == "HT" and type(totalsteak_up) == int:
                #     print('TRUE TRUE TREU')
                #     linkUp = get_link(i)
                #     if linkUp in totalstreak_up3:
                #         continue
                #     totalstreak_up3.add(linkUp)
                #     checker = 777
                #     check_link(linkUp, time, score_one, score_two, period, minute, totalsteak_up, score_line)


            except Exception as fail:
                print(fail)
                print("SOME FilTH IN PARSING...")
                continue
        print("CURRENT TIME:: ",datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    except Exception as fail:
        print(fail)
        print('Another mistake...')
        continue


    sleep(10)


