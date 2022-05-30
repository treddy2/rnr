iefilePath = "F:/resumes/"
text_list = ["Kate_Winslet.pdf", 'Komali_sfdc.docx', 'Madhukar_sfdc.docx', 'Nandu_rdy.docx', 'pooja_Hedge_hyderabad.pdf', 'Prakash_sfdc.pdf', 'rajagopal_sfdc.docx', 'Rajani Polampalli_sfdc.docx', 'Ramana_Sinde.docx', 'Ravi_rdy.pdf', 'Roja_Velpuri_hyderabad.pdf', 'Sandeep Yalamanchili_sfdc.pdf', 'Shankar_siva.pdf', 'Srinivas Adepu_sfdc.docx', 'Tallaiva_pro_sfdc.docx', 'Tom_Cruise.pdf', 'V Venkat_sfdc.docx', 'Vellu_hyderabad (another copy).pdf']
print(text_list[0].__contains__("/"))

def ie_comptble(text_list):
    onlyfiles = list(map(lambda x: iefilePath + x, text_list))
    print(onlyfiles)




if text_list[0].__contains__("/") == False:
    ie_comptble(text_list)


#ie_comptble(text_list)