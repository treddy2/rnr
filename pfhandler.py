# Resume Phrase Matcher code


# importing all required libraries
import atexit
import base64
import glob
import io
from operator import itemgetter

import docxpy
import fitz
from apscheduler.schedulers.background import BackgroundScheduler

# from flask_apscheduler import APScheduler
# scheduler = APScheduler()
import templtehandler

sched = BackgroundScheduler()

import content
import PyPDF2
import os
from os import listdir
from os.path import isfile, join
from io import StringIO

# import buffer as buffer
import docx as docx
import pandas as pd
from collections import Counter, OrderedDict
import en_core_web_sm
import matplotlib.pyplot as plt

from dbscripts import login_sc, configskills_db, gettechnologies, _processdata, getskillareas, _techsubAreas, \
    logout, userdetails_res, filename_generator, mncs_c, configmncs_db, _techcomp, updel_modal, getmncs, getmncscomp

nlp = en_core_web_sm.load()
from spacy.matcher import PhraseMatcher
from flask import Flask, render_template, request, flash, session

app = Flask(__name__)

app.secret_key = 'random string'
TOPIC_DICT = content

# Function to read resumes from the folder one by one
# mypath = '/home/rdy/resumes'  # enter your path here where you saved the resumes
# onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
login_user_name = ""
login_user_role = ""
is_user_login = False
onlyfiles = ""
# filePath = "/home/rdy/" # Linux directory
filePath = "F:/"  # Windows directory , mozilla,chrome,edze
# filePath = "C:/Users/ravi/Desktop/"
iefilePath = "F:/hclresumes/"  # Windows internet explorer directory
rsrc_name = "Resource Name"
rsrc_rank = "Rank"
temp_dict_list1 = []
temp_dict_list = []
temp_words_list = []
mnc_words_list = []
dff_key = dict()
dff_key1 = dict()
tech_skill_org = []
tech_skill_org1 = ""
datali = []
filesCount = 0
chart_session = ""
profile_pic = os.path.join("static", "img")
app.config["UPLOAD_FOLDER"] = profile_pic
app.config["SECRET_KEY"] = app.secret_key
ls = []
list3 = []


def userdetails():
    usr_data = []
    firstName, lastName, eMail, phoneNumber, adDress, couNtry = userdetails_res()
    usr_data.append(firstName)
    usr_data.append(lastName)
    usr_data.append(eMail)
    usr_data.append(phoneNumber)
    usr_data.append(adDress)
    usr_data.append(couNtry)
    return usr_data


@app.route('/')
def home():
    areas_subareas = gettechnologies()
    if login_user_role == "":
        return render_template("login.html", conf="nav-link disabled")
    if login_user_role == "user":
        user_data = userdetails()
        return render_template("pf_result.html", areas_subareas=areas_subareas, filesCount=filesCount,
                               sign_user=login_user_name, conf="nav-link disabled", conf_link="nav-link",
                               login=is_user_login, dropdown_toggle="dropdown-toggle", user_data=user_data)
    if login_user_role == "admin":
        user_data = userdetails()
        return render_template("pf_result.html", areas_subareas=areas_subareas, filesCount=filesCount,
                               sign_user=login_user_name, conf="nav-link", login=is_user_login,
                               dropdown_toggle="dropdown-toggle", user_data=user_data)


@app.route('/login')
def login():
    return render_template("login.html", conf="nav-link disabled")


@app.route("/loginuser", methods=['POST', 'GET'])
def loginuser():
    global login_user_name
    global login_user_role
    global is_user_login
    return_val, session = login_sc()
    if len(session) != 0:
        login_user_name = session['user_name']
        login_user_role = session['user_role']
        is_user_login = session['login']
        if return_val == 1 and login_user_role == "user":
            user_data = userdetails()
            areas_subareas = gettechnologies()
            return render_template("pf_result.html", areas_subareas=areas_subareas, filesCount=filesCount,
                                   sign_user=login_user_name, conf="nav-link disabled", conf_link="nav-link",
                                   login=is_user_login, dropdown_toggle="dropdown-toggle", user_data=user_data)
        if return_val == 1 and login_user_role == "admin":
            user_data = userdetails()
            areas_subareas = gettechnologies()
            return render_template("pf_result.html", areas_subareas=areas_subareas, filesCount=filesCount,
                                   sign_user=login_user_name, conf="nav-link", login=is_user_login,
                                   dropdown_toggle="dropdown-toggle", user_data=user_data)
    if len(session) == 0:
        error = 'Incorrect user-name and password'
        return render_template("login.html", error=error, conf="nav-link disabled")


@app.route('/signup')
def signup():
    return render_template("signup.html", conf="nav-link disabled")


@app.route("/signupuser", methods=['POST', 'GET'])
def signupuser():
    _processdata()
    return render_template("login.html", conf="nav-link disabled")


@app.route("/skillsconfig")
def skillsconfig():
    tech_subareas = _techsubAreas()
    techcomp = _techcomp()
    if session['user_role'] == "user":
        user_data = userdetails()
        return render_template("skillsconfig.html", tech_subareas=tech_subareas.to_dict(), techcomp=techcomp,
                               filesCount=filesCount,
                               sign_user=session['user_name'], conf="nav-link disabled", conf_link="nav-link",
                               login=session['login'], dropdown_toggle="dropdown-toggle", user_data=user_data)
    if session['user_role'] == "admin":
        user_data = userdetails()
        return render_template("skillsconfig.html", tech_subareas=tech_subareas.to_dict(), techcomp=techcomp,
                               filesCount=filesCount,
                               sign_user=session['user_name'], conf="nav-link", login=session['login'],
                               dropdown_toggle="dropdown-toggle", user_data=user_data)
    else:
        error = 'Data is not available'
        return render_template("login.html", error=error, conf="nav-link disabled")
    # return render_template("skillsconfig.html", tech_subareas=tech_subareas,techcomp=techcomp)


@app.route("/configskills", methods=['POST', 'GET'])
def configskills():
    fix_rating_percent = 100
    error = ""
    success = ""
    bool, subareas_ratings, skillss = configskills_db()  # function insert data in the mysql database
    techcomp = _techcomp()
    tech_subareas = _techsubAreas()
    ssr = sum(subareas_ratings)
    if bool == False:
        if session['user_role'] == "user":
            if skillss == "":
                user_data = userdetails()
                error = "Invalid Technologies !  Null values not allowed"
                return render_template("skillsconfig.html", tech_subareas=tech_subareas.to_dict(), techcomp=techcomp,
                                       sign_user=session['user_name'], conf="nav-link disabled", conf_link="nav-link",
                                       login=session['login'], dropdown_toggle="dropdown-toggle", error=error,
                                       user_data=user_data)

            if ssr >= 101 or ssr <= 99:
                user_data = userdetails()
                error = "Please verify alloted percentage"
                return render_template("skillsconfig.html", tech_subareas=tech_subareas.to_dict(), techcomp=techcomp,
                                       sign_user=session['user_name'], conf="nav-link disabled", conf_link="nav-link",
                                       login=session['login'], dropdown_toggle="dropdown-toggle", error=error,
                                       user_data=user_data)

            user_data = userdetails()
            error = 'Technologies and sub-areas exist'
            return render_template("skillsconfig.html", tech_subareas=tech_subareas.to_dict(), techcomp=techcomp,
                                   sign_user=session['user_name'], conf="nav-link disabled", conf_link="nav-link",
                                   login=session['login'], dropdown_toggle="dropdown-toggle", error=error,
                                   user_data=user_data)
        if session['user_role'] == "admin":
            if skillss == "":
                user_data = userdetails()
                error = "Invalid Technologies !  Null values not allowed"
                return render_template("skillsconfig.html", tech_subareas=tech_subareas.to_dict(), techcomp=techcomp,
                                       error=error,
                                       sign_user=session['user_name'], conf="nav-link", login=session['login'],
                                       dropdown_toggle="dropdown-toggle", user_data=user_data)

            if ssr >= 101 or ssr <= 99:
                user_data = userdetails()
                error = "Please verify alloted percentage"
                return render_template("skillsconfig.html", tech_subareas=tech_subareas.to_dict(), techcomp=techcomp,
                                       error=error,
                                       sign_user=session['user_name'], conf="nav-link", login=session['login'],
                                       dropdown_toggle="dropdown-toggle", user_data=user_data)

            user_data = userdetails()
            error = 'Technologies and sub-areas exist'
            return render_template("skillsconfig.html", tech_subareas=tech_subareas.to_dict(), techcomp=techcomp,
                                   error=error,
                                   sign_user=session['user_name'], conf="nav-link", login=session['login'],
                                   dropdown_toggle="dropdown-toggle", user_data=user_data)
    else:
        if session['user_role'] == "user":
            user_data = userdetails()
            success = "Technologies and sub-areas added successfully !"
            return render_template("skillsconfig.html", tech_subareas=tech_subareas, techcomp=techcomp,
                                   sign_user=session['user_name'], conf="nav-link disabled", conf_link="nav-link",
                                   login=session['login'], dropdown_toggle="dropdown-toggle", success=success,
                                   user_data=user_data)

        if session['user_role'] == "admin":
            user_data = userdetails()
            success = "Technologies and sub-areas added successfully !"
            return render_template("skillsconfig.html", tech_subareas=tech_subareas, techcomp=techcomp,
                                   sign_user=session['user_name'], conf="nav-link", login=session['login'],
                                   dropdown_toggle="dropdown-toggle", success=success, user_data=user_data)
        # return render_template("skillsconfig.html", tech_subareas=tech_subareas, conf="nav-link disabled")


@app.route("/up_del_modal", methods=['POST', 'GET'])
def up_del_modal():
    success = ""
    updel_modal()
    tech_subareas = _techsubAreas()
    techcomp = _techcomp()
    if session['user_role'] == "user":
        user_data = userdetails()
        success = "Data modified successfully"
        return render_template("skillsconfig.html", tech_subareas=tech_subareas.to_dict(), techcomp=techcomp,
                               sign_user=session['user_name'], conf="nav-link disabled", conf_link="nav-link",
                               login=session['login'], dropdown_toggle="dropdown-toggle", success=success,
                               user_data=user_data)

    if session['user_role'] == "admin":
        user_data = userdetails()
        success = "Data modified successfully ! "
        return render_template("skillsconfig.html", tech_subareas=tech_subareas.to_dict(), techcomp=techcomp,
                               sign_user=session['user_name'], conf="nav-link", login=session['login'],
                               dropdown_toggle="dropdown-toggle", success=success, user_data=user_data)
    # return render_template("skillsconfig.html", tech_subareas=tech_subareas)


@app.route("/configmncs", methods=['POST', 'GET'])
def configmncs():
    fix_tier_ratg = 101
    error = ""
    success = ""
    bool, comp_ratings = configmncs_db()  # function insert data in the mysql database
    tech_subareas = _techsubAreas()
    techcomp = _techcomp()
    # scr = sum(comp_ratings)
    if bool == False:
        if session['user_role'] == "user":
            if comp_ratings >= fix_tier_ratg:
                user_data = userdetails()
                error = "Please verify alloted percentage"
                return render_template("skillsconfig.html", tech_subareas=tech_subareas.to_dict(), techcomp=techcomp,
                                       sign_user=session['user_name'], conf="nav-link disabled", conf_link="nav-link",
                                       login=session['login'], dropdown_toggle="dropdown-toggle", error=error,
                                       user_data=user_data)

            user_data = userdetails()
            error = 'Company Exist'
            return render_template("skillsconfig.html", tech_subareas=tech_subareas.to_dict(), techcomp=techcomp,
                                   sign_user=session['user_name'], conf="nav-link disabled", conf_link="nav-link",
                                   login=session['login'], dropdown_toggle="dropdown-toggle", error=error,
                                   user_data=user_data)

        if session['user_role'] == "admin":
            if comp_ratings >= fix_tier_ratg:
                user_data = userdetails()
                error = "Please verify alloted percentage. "
                return render_template("skillsconfig.html", tech_subareas=tech_subareas.to_dict(), techcomp=techcomp,
                                       error=error,
                                       sign_user=session['user_name'], conf="nav-link", login=session['login'],
                                       dropdown_toggle="dropdown-toggle", user_data=user_data)
            user_data = userdetails()
            error = 'Company Exist'
            return render_template("skillsconfig.html", tech_subareas=tech_subareas.to_dict(), techcomp=techcomp,
                                   error=error,
                                   sign_user=session['user_name'], conf="nav-link", login=session['login'],
                                   dropdown_toggle="dropdown-toggle", user_data=user_data)
    else:
        if session['user_role'] == "user":
            if comp_ratings >= fix_tier_ratg:
                user_data = userdetails()
                error = "Please verify alloted percentage"
                return render_template("skillsconfig.html", tech_subareas=tech_subareas, techcomp=techcomp,
                                       sign_user=session['user_name'], conf="nav-link disabled", conf_link="nav-link",
                                       login=session['login'], dropdown_toggle="dropdown-toggle", error=error,
                                       user_data=user_data)

            user_data = userdetails()
            success = "Company added successfully !"
            return render_template("skillsconfig.html", tech_subareas=tech_subareas, techcomp=techcomp,
                                   sign_user=session['user_name'], conf="nav-link disabled", conf_link="nav-link",
                                   login=session['login'], dropdown_toggle="dropdown-toggle", success=success,
                                   user_data=user_data)

        if session['user_role'] == "admin":
            if comp_ratings >= fix_tier_ratg:
                user_data = userdetails()
                error = "Please verify alloted percentage, yep error"
                return render_template("skillsconfig.html", tech_subareas=tech_subareas, techcomp=techcomp,
                                       sign_user=session['user_name'], conf="nav-link", login=session['login'],
                                       dropdown_toggle="dropdown-toggle", error=error, user_data=user_data)
            user_data = userdetails()
            success = "Company added successfully !"
            return render_template("skillsconfig.html", tech_subareas=tech_subareas, techcomp=techcomp,
                                   sign_user=session['user_name'], conf="nav-link", login=session['login'],
                                   dropdown_toggle="dropdown-toggle", success=success, user_data=user_data)
        # return render_template("skillsconfig.html", tech_subareas=tech_subareas, conf="nav-link disabled")


@app.route("/signout")
def signout():
    log_out = logout()
    if log_out:
        return render_template("login.html", conf="nav-link disabled")


def crDf(temp_dict, tech_skill, mncs_type_l, tech_skill_org1):
    tech_null_dict = dict()
    subareas_occurence = []
    # for x in tech_skill:
    # temp_words_list.append(str(x).strip(' '))
    rmv_dupl = list(dict.fromkeys(tech_skill_org1))
    df8 = pd.DataFrame([[" " for x in range(len(rmv_dupl))]], columns=rmv_dupl)
    for xkey, y in df8.to_dict().items():
        sbars, sbrtngs = subareassplit(xkey)
        for zvalue in y.values():
            tech_null_dict[sbars] = zvalue

    dataframe5 = pd.DataFrame(temp_dict)
    dataframe6 = pd.DataFrame(dataframe5.iloc[:, 0:3])
    resr_df = pd.DataFrame(dataframe6.iloc[[0], [0]])
    resr_name = resr_df.to_dict()
    for keyword_keys in dataframe6.to_dict()['Keyword'].keys():
        for key in tech_null_dict:
            if key in dataframe6.to_dict()['Keyword'][keyword_keys].strip(' '):
                tech_null_dict[key] = int(dataframe6.to_dict()['Count'][keyword_keys].strip(' '))  # mapping
                subareas_occurence.append(int(dataframe6.to_dict()['Count'][keyword_keys].strip(' ')))
    dff_key["Keywods Count"] = tech_null_dict
    temp_dict2 = dict(resr_name, **dff_key)
    temp_dict2.update(resr_name)
    return temp_dict2, subareas_occurence


splzed_tech = []

@app.route('/profile', methods=['POST'])
def profile():
    splzed_tech = gettechnologies()
    print("got the splzed_tech -- ", splzed_tech)
    temp_dict_list.clear()
    temp_words_list.clear()
    t1 = []
    t2 = []
    t3 = []
    try:
        areas_subareas1 = gettechnologies()
        mncs_type_l1, mncs_comp_l = getmncscomp()
        mncs_type_l2, mncs_rating, dum_wtg = tier_ratings(mncs_type_l1)
        mncs_type_l = mncs_type_l2.split(',')
        if len(areas_subareas1) == 0:
            if session['user_role'] == "user":
                return render_template("error.html",
                                       sign_user=session['user_name'], conf="nav-link disabled",
                                       conf_link="nav-link",
                                       login=session['login'], dropdown_toggle="dropdown-toggle"
                                       )
            if session['user_role'] == "admin":
                return render_template("error.html", sign_user=session['user_name'], conf="nav-link",
                                       login=session['login'],
                                       dropdown_toggle="dropdown-toggle"
                                       )

        if len(mncs_type_l) == 0 or len(mncs_comp_l) == 0:
            if session['user_role'] == "user":
                return render_template("mncs_error.html",
                                       sign_user=session['user_name'], conf="nav-link disabled",
                                       conf_link="nav-link",
                                       login=session['login'], dropdown_toggle="dropdown-toggle"
                                       )
            if session['user_role'] == "admin":
                return render_template("mncs_error.html", sign_user=session['user_name'], conf="nav-link",
                                       login=session['login'],
                                       dropdown_toggle="dropdown-toggle"
                                       )

        if request.method == 'POST':
            technologies = request.form['technologies']
            tech_subareas1 = getskillareas(technologies)
            tech_skill_org1 = tech_subareas1.split(",")
            tech_subareas, sub_rating, subar_wtg_ratings = subareas_ratings(tech_subareas1)
            filesSelected = list(fileName.filename for fileName in request.files.getlist('fileNames'))
            filesCount1 = len(filesSelected)
            filesCount = str(filesCount1) + " - Files"
            chart_wid = 500
            chart_hth = 250
            chart_font = 30
            if filesCount1 <= 10:
                chart_wid = 1000
                chart_hth = 500
                chart_font = 43
            if filesCount1 >= 11 and filesCount1 <= 21:
                chart_wid = 1400
                chart_hth = 700
                chart_font = 35
            if filesCount1 >= 22:
                chart_wid = 2400
                chart_hth = 1400
                chart_font = 25
            onlyfiles = list(map(lambda x: filePath + x, filesSelected))
            final_database = pd.DataFrame()
            # Start - code to work in Internet explorer
            if filesSelected[0].__contains__("/") == False:
                onlyfiles = list(map(lambda x: iefilePath + x, filesSelected))
            # End - code to work in Internet explorer
            for x in range(len(onlyfiles)):
                file = onlyfiles[x]
                isFile = os.path.isfile(file)
                if not isFile:
                    if session['user_role'] == "user":
                        return render_template("error.html",
                                               sign_user=session['user_name'], conf="nav-link disabled",
                                               conf_link="nav-link",
                                               login=session['login'], dropdown_toggle="dropdown-toggle"
                                               )
                    if session['user_role'] == "admin":
                        return render_template("error.html", sign_user=session['user_name'], conf="nav-link",
                                               login=session['login'],
                                               dropdown_toggle="dropdown-toggle"
                                               )
                dat, tech_skill = create_profile(file, technologies, tech_subareas, mncs_type_l[0],
                                                 mncs_comp_l[0], mncs_type_l[1], mncs_comp_l[1],
                                                 mncs_type_l[2], mncs_comp_l[2])

                t1 = get_keyt1(mncs_type_l[0], dat.to_dict())
                t2 = get_keyt2(mncs_type_l[1], dat.to_dict())
                t3 = get_keyt3(mncs_type_l[2], dat.to_dict())
                sum_t1 = sum(t1)
                sum_t2 = sum(t2)
                sum_t3 = sum(t3)
                wtg_t1 = mncs_rating[0] * sum_t1
                wtg_t2 = mncs_rating[1] * sum_t2
                wtg_t3 = mncs_rating[2] * sum_t3
                final_database = final_database.append(dat)
                cs, new_data = plotlyChart(final_database, chart_font)
                dataframe3 = pd.DataFrame(dat.iloc[[0], [0]]).to_dict()
                dataframe4 = pd.DataFrame(dat.iloc[:, 2:4]).to_dict()
                temp_dict = dict(dataframe3, **dataframe4)
                temp_dict.update(dataframe3)
                temp_dict3, subareas_occurence1 = crDf(temp_dict, tech_skill, mncs_type_l, tech_skill_org1)
                dummy_list = []
                if len(subar_wtg_ratings) == len(temp_dict3['Keywods Count']):
                    # TODO get the unique values and multiply weightage with occurence
                    for k, v in subar_wtg_ratings.items():
                        for x, y in temp_dict3['Keywods Count'].items():
                            if k == x:
                                if y != " ":
                                    dummy_value = v * y
                                    dummy_list.append(dummy_value)

                dummy_list.append(wtg_t1)
                dummy_list.append(wtg_t2)
                dummy_list.append(wtg_t3)
                final_list = list(map(lambda x: x / 100, dummy_list))
                number_tech_tier = len(sub_rating) + len(mncs_type_l)
                cand_rank = sum(final_list) / number_tech_tier
                # ls.append(cand_rank)
                # print(ls,"--Main list")
                # rank_values = find_rank(ls)
                # print(rank_values,"---assign the rank")
                temp_dict3["Candidate Rank"] = (round(cand_rank, 5))
                temp_dict3["Tier-1"] = {sum_t1}
                temp_dict3["Tier-2"] = {sum_t2}
                temp_dict3["Tier-3"] = {sum_t3}
                temp_dict_list.append(temp_dict3)

    except Exception as e:
        str(e)

    if session['user_role'] == "user":
        user_data = userdetails()
        list(temp_dict_list)
        temp_dict_list.sort(key=itemgetter("Candidate Rank"), reverse=True)
        print(temp_dict_list, "sorted")
        # Start
        print(len(temp_dict_list), "length")
        for x in range(len(temp_dict_list)):
            print(temp_dict_list[x]["Candidate Rank"], x + 1)
            temp_dict_list[x]["Candidate Rank"] = {x + 1}
        # end
        for x in tech_skill_org1:
            temp_words_list.append(str(x).strip(' '))
        tech_skill_org = list(dict.fromkeys(temp_words_list))
        try:
            profile_pic1 = os.path.join(app.config["UPLOAD_FOLDER"], str(cs))
        except:
            profile_pic1 = "No Data available"
        finally:
            return render_template("pf_result.html", areas_subareas=areas_subareas1, filesCount=filesCount,
                                   sign_user=session['user_name'], conf="nav-link disabled", conf_link="nav-link",
                                   login=session['login'], dropdown_toggle="dropdown-toggle", rsrc_name=rsrc_name,
                                   rsrc_rank=rsrc_rank,
                                   temp_dict_list=temp_dict_list, tech_skill_org=tech_skill_org,
                                   profile_pic1=profile_pic1,
                                   user_data=user_data, chart_hth=chart_hth, chart_wid=chart_wid, filePath=filePath,
                                   tier_companies=mncs_type_l1)
    if session['user_role'] == "admin":
        # areas_subareas = gettechnologies()
        user_data = userdetails()
        list(temp_dict_list)
        temp_dict_list.sort(key=itemgetter("Candidate Rank"), reverse=True)
        print(temp_dict_list, "sorted")
        # Start
        print(len(temp_dict_list), "length")
        for x in range(len(temp_dict_list)):
            print(temp_dict_list[x]["Candidate Rank"], x + 1)
            temp_dict_list[x]["Candidate Rank"] = {x + 1}
        print(temp_dict_list, "great")
        # end
        for x in tech_skill_org1:
            temp_words_list.append(str(x).strip(' '))
        tech_skill_org = list(dict.fromkeys(temp_words_list))
        try:
            profile_pic1 = os.path.join(app.config["UPLOAD_FOLDER"], str(cs))
        except:
            profile_pic1 = "No Data available"
        finally:
            return render_template("pf_result.html", areas_subareas=areas_subareas1, filesCount=filesCount,
                                   sign_user=session['user_name'], conf="nav-link", login=session['login'],
                                   dropdown_toggle="dropdown-toggle", rsrc_name=rsrc_name, rsrc_rank=rsrc_rank,
                                   temp_dict_list=temp_dict_list, tech_skill_org=tech_skill_org,
                                   profile_pic1=profile_pic1,
                                   user_data=user_data, chart_hth=chart_hth, chart_wid=chart_wid, filePath=filePath,
                                   tier_companies=mncs_type_l1)
    else:
        error = 'Data is not available'
        return render_template("login.html", error=error)

    # return render_template("pf_result.html", rsrc_name=rsrc_name, filesCount=filesCount, temp_dict_list=temp_dict_list,
    # tech_skill_org=tech_skill_org, areas_subareas=areas_subareas, profile_pic1=profile_pic1)


def find_rank(list2):
    list2.sort()
    for x in range(len(list2)):
        list3.append(x + 1)
    new_lst = list3[::-1]
    return new_lst


def subareas_ratings(tech_subareas):
    subareas = []
    subares_ratings = []
    tech_subareas_list = tech_subareas.split(",")
    for tsl in tech_subareas_list:
        if tsl == "":
            break
        y = tsl.strip(" ").find('(')
        z = tsl.strip(" ").find(')')
        subareas.append(tsl[:y])
        techsubareas_ratings = tsl[y + 1:z]
        subares_ratings.append(int(techsubareas_ratings))
    subareas1 = ','.join([str(elem) for elem in subareas])
    subar_wtg_ratings = dict(zip(subareas, subares_ratings))
    return subareas1, subares_ratings, subar_wtg_ratings


def pdfextract1(file):
    fileReader = PyPDF2.PdfFileReader(open(file, 'rb'))
    countpage = fileReader.getNumPages()
    count = 0
    text = []
    while count < countpage:
        pageObj = fileReader.getPage(count)
        count += 1
        t = pageObj.extractText()
        text.append(t)
    return text


def docextract1(file):
    doc = docx.Document(file)
    text = []
    for x in doc.paragraphs:
        text.append(x.text)
    return ('\n'.join(text))


def docextract(file):
    text = docxpy.process(file)
    return [text]


def pdfextract(file):
    text = ''
    with fitz.open(file) as doc:
        for page in doc:
            text += page.getText()
    return text


def create_profile(file, technologies, tech_subareas, mncs_type_t1, mncs_comp_t1, mncs_type_t2, mncs_comp_t2,
                   mncs_type_t3, mncs_comp_t3):
    check_pdf_format = file.endswith(".pdf")
    check_docx_format = file.endswith(".docx")
    # check_doc_format = file.endswith(".doc")
    if check_pdf_format:
        text = pdfextract(file)

    if check_docx_format:
        text = docextract(file)

    # TODO Check the file is doc format
    # if check_doc_format:
    # text = pdfextract(file)
    text = str(text)
    text = text.replace("\\n", "")
    text1 = text.lower()
    text = "Tier-1 Tier-2 Tier-3 ." + text1
    # keyword_dict = pd.read_csv('/home/rdy/profilekeys/profiles_temp.txt')
    keyword_dict = pd.DataFrame(tech_subareas.split(","), columns=[technologies])
    tier1_dict = pd.DataFrame(mncs_comp_t1.split(","), columns=[mncs_type_t1])
    tier2_dict = pd.DataFrame(mncs_comp_t2.split(","), columns=[mncs_type_t2])
    tier3_dict = pd.DataFrame(mncs_comp_t3.split(","), columns=[mncs_type_t3])
    technologies_words = [nlp(text) for text in keyword_dict[technologies].dropna(axis=0)]
    mncs_words1 = [nlp(text) for text in tier1_dict[mncs_type_t1].dropna(axis=0)]
    mncs_words2 = [nlp(text) for text in tier2_dict[mncs_type_t2].dropna(axis=0)]
    mncs_words3 = [nlp(text) for text in tier3_dict[mncs_type_t3].dropna(axis=0)]

    """gcp_words = [nlp(text) for text in keyword_dict['Google cloud'].dropna(axis=0)]
    hadoop_words = [nlp(text) for text in keyword_dict['Hadoop'].dropna(axis=0)]
    py_words = [nlp(text) for text in keyword_dict['python'].dropna(axis=0)]
    ide_words = [nlp(text) for text in keyword_dict['IDE'].dropna(axis=0)]
    wi_words = [nlp(text) for text in keyword_dict['HTML'].dropna(axis=0)]
    ml_words = [nlp(text) for text in keyword_dict['Machine learning'].dropna(axis=0)]"""

    matcher = PhraseMatcher(nlp.vocab)
    matcher.add(technologies, None, *technologies_words)
    matcher.add('Tier-1', None, *mncs_words1)
    matcher.add('Tier-2', None, *mncs_words2)
    matcher.add('Tier-3', None, *mncs_words3)
    # matcher.add('Google cloud', None, *gcp_words)
    # matcher.add('Hadoop', None, *hadoop_words)
    # matcher.add('python', None, *py_words)
    # matcher.add('IDE', None, *ide_words)
    # matcher.add('HTML', None, *wi_words)
    # matcher.add('ML', None, *ml_words)
    doc = nlp(text)
    d = []
    matches = matcher(doc)
    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
        span = doc[start: end]  # get the matched slice of the doc
        d.append((rule_id, span.text))
    keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i, j in Counter(d).items())
    df = pd.read_csv(StringIO(keywords), names=['Keywords_List'])
    df1 = pd.DataFrame(df.Keywords_List.str.split(' ', 1).tolist(), columns=['Subject', 'Keyword'])
    df2 = pd.DataFrame(df1.Keyword.str.split('(', 1).tolist(), columns=['Keyword', 'Count'])
    df3 = pd.concat([df1['Subject'], df2['Keyword'], df2['Count']], axis=1)
    df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))
    base = os.path.basename(file)
    filename = os.path.splitext(base)[0]
    name = rename_file(filename)
    # name2 = name.lower()  # resource-name
    ## converting str to dataframe
    name3 = pd.read_csv(StringIO(name), names=['Candidate Name'])
    dataf = pd.concat([name3['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']], axis=1)
    dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace=True)
    return (dataf, technologies_words)


def rename_file(filename):
    return filename[:8]


def get_keyt1(val, tier_dict):
    k = ""
    tier1 = []
    for key, vale in tier_dict['Subject'].items():
        if val == vale:
            k = int(key)
            for value in tier_dict['Count'][k]:
                if vale == "Tier-1":
                    tier1.append(int(value))
    return tier1


def get_keyt2(val, tier_dict):
    k = ""
    tier2 = []
    for key, vale in tier_dict['Subject'].items():
        if val == vale:
            k = int(key)
            for value in tier_dict['Count'][k]:
                if vale == "Tier-2":
                    tier2.append(int(value))
    return tier2


def get_keyt3(val, tier_dict):
    k = ""
    tier3 = []
    for key, vale in tier_dict['Subject'].items():
        if val == vale:
            k = int(key)
            for value in tier_dict['Count'][k]:
                if vale == "Tier-3":
                    tier3.append(int(value))
    return tier3


# function end` 1   s
def plotlyChart(final_database, chart_font):
    # code to count words under each category and visulaize it through Matplotlib
    final_database2 = final_database['Keyword'].groupby(
        [final_database['Candidate Name'], final_database['Subject']]).count().unstack()
    final_database2.reset_index(inplace=True)
    final_database2.fillna(0, inplace=True)
    new_data = final_database2.iloc[:, 1:]
    new_data.index = final_database2['Candidate Name']
    # execute the below line if you want to see the candidate profile in a csv format
    new_data.to_csv('static/img/sample3.csv')
    plt.rcParams.update({'font.size': chart_font})
    ax = new_data.plot.barh(title="Resume keywords by category", legend=False, figsize=(50, 25),
                            stacked=True)
    labels = []
    print("new_data-- ", new_data)
    print("new_data.columns-- ",new_data.columns)
    print(new_data.columns[0],"---superb1")
    new_data.rename(columns={new_data.columns[0]: "Skills"},inplace=True)
    print(new_data.columns[0], "---superb2")
    #splzd_tech = gettechnologies # hitting database multiple times
    print(splzed_tech,"--specialized technologies") # use global value
    for j in new_data.columns:
        print(j, "-- j value")
        for i in new_data.index:
            print(i, "-- i value")
            label = str(j) + ": " + str(int(new_data.loc[i][j]))
            print(label,"--- label",str(int(new_data.loc[i][j])))
            labels.append(label)
    patches = ax.patches
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            ax.text(x + width / 2., y + height / 2., label, ha='center', va='center')
    # plt.show()
    plt.xticks(rotation='1.5')
    chart_session = filename_generator()
    plt.savefig("static/img/" + chart_session, dpi=40)
    plt.close()
    # TODO
    return chart_session, new_data


def plotfigre(plt):
    buffer = io.BytesIO()
    plt.savefig(buffer, format='PNG', bbox_inches='tight')
    buffer.seek(0)
    data_uri = base64.b64encode(buffer.read()).decode('ascii')
    return data_uri


def remove_chart():
    for f in glob.glob("static/img/PROFILE_CHART_*"):
        os.remove(f)
        print("file removed")


def tier_ratings(comp_ratings):
    subareas = []
    subares_ratings = []
    # tech_subareas_list =  tech_subareas.split(",")
    for tsl in comp_ratings:
        if tsl == "":
            break
        y = tsl.strip(" ").find('(')
        z = tsl.strip(" ").find(')')
        subareas.append(tsl[:y])
        techsubareas_ratings = tsl[y + 1:z]
        subares_ratings.append(int(techsubareas_ratings))
    subareas1 = ','.join([str(elem) for elem in subareas])
    subar_wtg_ratings = dict(zip(subareas, subares_ratings))

    return subareas1, subares_ratings, subar_wtg_ratings


def ranksplit(tech):
    y = tech.strip(" ").find('{')
    z = tech.strip(" ").find('}')
    subareas = tech[:y]
    techsubareas_ratings = tech[y + 1:z]
    return subareas, techsubareas_ratings


def subareassplit(tech):
    y = tech.strip(" ").find('(')
    z = tech.strip(" ").find(')')
    subareas = tech[:y]
    techsubareas_ratings = tech[y + 1:z]
    return subareas, techsubareas_ratings


if __name__ == "__main__":
    # scheduler.add_job(id = "Scheduler Task",func=remove_chart, trigger="interval", seconds=60)
    # scheduler.start()
    # atexit.register(lambda: scheduler.shutdown())
    sched.add_job(remove_chart, 'cron', day_of_week='0-6', hour=15, minute=23)
    sched.start()
    atexit.register(lambda: sched.shutdown())
    app.run(debug=True, port="5010")
