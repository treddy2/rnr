import operator
from operator import itemgetter

import PyPDF2
import glob, os

import docx
import docxpy
import fitz
import mysql
from pdfrw import PdfReader

import dbcon

file = 'C:/Users/ravi/Desktop/Resumes/Manu.docx'

def pdfextract():
    fileReader = PyPDF2.PdfFileReader(open('C:/Users/ravi/Desktop/Resumes/Abishek.pdf', 'rb'),strict=False)
    print('filereader-->', fileReader.documentInfo,fileReader.getNumPages())
    countpage = fileReader.getNumPages()
    print("number of pages", countpage)
    count = 0
    text = []
    while count < countpage:
        pageObj = fileReader.getPage(count)
        count += 1
        t = pageObj.extractText()
        text.append(t)
    print(text)
    return text


def pdfrwdemo():
    x = PdfReader(file)
    #print(x.keys())


def docextract(file):
    doc = docx.Document(file)
    text = []
    for x in doc.paragraphs:
        text.append(x.text)
    print('\n'.join(text))
    return ('\n'.join(text))

def docxpydemo():
    text = docxpy.process(file)
    print(text)

def fitzdemo():
    filepath = "C:/Users/ravi/Desktop/Resumes/Abishek.pdf"
    text = ''
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.getText()
    print(text)

comp_ratings = ['Tier-1(25)', 'Tier-2(15)', 'Tier-3(10)']
def tier_ratings():
    subareas = []
    subares_ratings = []
    #tech_subareas_list =  tech_subareas.split(",")
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
    print(subareas1.split(','),subares_ratings,sum(subares_ratings),"shiva")
    return subareas1,subares_ratings,subar_wtg_ratings

tier_type = ["Tier-1","Tier-2","Tier-3"]
tier_dict = {'Candidate Name': {0: 'Abishek', 1: 'Abishek'}, 'Subject': {0: 'Tier-1', 1: 'Tier-2', 2:'Tier-3',3: 'Java'}, 'keyword': {0: 'ibm',1: 'tcs', 2: 'accenture',3: 'spring '}, 'Count': {0: '1', 1: '2',2: '3',3:'5'}}


def get_key(val):
    k=[]
    tier1 = []
    tier2 = []
    tier3 = []
    for key, vale in tier_dict['Subject'].items():
         if val == vale:
             k.append(key)
             for t in k:
                 for value in tier_dict['Count'][t]:
                     if vale == "Tier-1":
                         tier1.append(int(value))
                     print(tier1, "tier-1 values")
                     if vale == "Tier-2":
                         tier2.append(int(value))
                     print(tier2, "tier-2 values")
                     if vale == "Tier-3":
                         tier3.append(int(value))
                     print(tier3, "tier-3 values")





#tiers_dict()
#for x in range(len(tier_type)):
    #get_key(tier_type[x])
#tier_ratings()
#docextract(file)
#pdfextract()
#docxpydemo()
#pdfrwdemo()
#fitzdemo()

def tst(tech):
    y = tech.strip(" ").find('{')
    z = tech.strip(" ").find('}')
    subareas = tech[:y]
    techsubareas_ratings = tech[y + 1:z]
    print(techsubareas_ratings)

tst("{ravi}")

list2 = [0.06888888888888889,0.06888888888888889,0.06666666666666667,0.044444444444444446,0.05777777777777778,0.100,1.2]

list3 = []

def find_rank(list2):
    list2.sort()
    print("sorted",list2)
    for x in range(len(list2)):
        list3.append(x+1)
    print(list3,"yes reversed")
    new_lst = list3[::-1]
    print(new_lst,"greate")


csv_mapping_list = [{'Candidate Name': {0: 'Kate_Win'}, 'Keywods Count': {'service cloud': ' ', 'trigger': ' ', 'lwc': 1, 'lightning': 1, 'visualforce page': ' ', 'sfdx': 1}, 'Candidate Rank': 0.06888888888888889, 'Tier-1': {0}, 'Tier-2': {2}, 'Tier-3': {0}}, {'Candidate Name': {0: 'Komali_s'}, 'Keywods Count': {'service cloud': ' ', 'trigger': ' ', 'lwc': ' ', 'lightning': 3, 'visualforce page': ' ', 'sfdx': ' '}, 'Candidate Rank':0.06666666666666667, 'Tier-1': {0}, 'Tier-2': {0}, 'Tier-3': {0}}, {'Candidate Name': {0: 'Madhukar'}, 'Keywods Count': {'service cloud': ' ', 'trigger': ' ', 'lwc': 1, 'lightning': 1, 'visualforce page': ' ', 'sfdx': ' '}, 'Candidate Rank': 0.044444444444444446, 'Tier-1': {0}, 'Tier-2': {0}, 'Tier-3': {0}}, {'Candidate Name': {0: 'Nandu_rd'}, 'Keywods Count': {'service cloud': 1, 'trigger': ' ', 'lwc': ' ', 'lightning': 1, 'visualforce page': ' ', 'sfdx': ' '}, 'Candidate Rank': 0.051111111111111114, 'Tier-1': {0}, 'Tier-2': {1}, 'Tier-3': {0}}]
csv_mapping_list.sort(key=itemgetter("Candidate Rank"),reverse=True)
print(csv_mapping_list,"sorted")
print(len(csv_mapping_list),"length")
for x in range(len(csv_mapping_list)):
    print(csv_mapping_list[x]["Candidate Rank"],x+1,"val")
    csv_mapping_list[x]["Candidate Rank"]=x+1

print(csv_mapping_list,"great")


"""size = len(csv_mapping_list)
print(size)
for i in range(size):
    min_index = i
    for j in range(i + 1, size):
        if csv_mapping_list[min_index]["Candidate Rank"] > csv_mapping_list[j]["Candidate Rank"]:
            min_index = j
    temp = csv_mapping_list[i]
    csv_mapping_list[i] = csv_mapping_list[min_index]
    csv_mapping_list[min_index] = temp
print(csv_mapping_list)"""

"""size = len(csv_mapping_list)
for i in range(size):
    min_index = i
    for j in range(i + 1, size):
        if csv_mapping_list[min_index]["Candidate Rank"] > csv_mapping_list[j]["Candidate Rank"]:
            min_index = j
    csv_mapping_list[i], csv_mapping_list[min_index] = csv_mapping_list[min_index], csv_mapping_list[i]
print(csv_mapping_list,"--")"""



