
dict_values = {'Candidate Name': {0: 'ravi', 1: 'ravi'}, 'Subject': {0: 'Java', 1: 'Java'}, 'Keyword': {0: 'jsp ', 1: 'spring boot '}, 'Count': {0: '5', 1: '1'}}
test_tuple = ((4, 'Gfg', 10), (3, 'is', 8), (6, 'Best', 10))
final_list = [{'Candidate Name': {0: 'ravi', 1: 'ravi'}, 'Subject': {0: 'Java', 1: 'Java'}, 'Keyword': {0: 'jsp ', 1: 'spring boot '}, 'Count': {0: '5', 1: '1'}},{'Candidate Name': {0: 'hari'}, 'Subject': {0: 'Java'}, 'Keyword': {0: 'jsp '}, 'Count': {0: '1'}},{'Candidate Name': {0: 'Reshma'}, 'Subject': {0: 'Java'}, 'Keyword': {0: 'jsp '}, 'Count': {0: '1'}}]
#final_dict = dict()
#final_list = [{'Candidate Name': {0: 'ravi'}, 'Subject': {0: 'Java'}, 'Keyword': {0: 'jsp '}, 'Count': {0: '5'}},{'Candidate Name': {0: 'hari'}, 'Subject': {0: 'Java'}, 'Keyword': {0: 'jsp '}, 'Count': {0: '1'}}]

cnd_lengthList = []
def convert_dic():
    for x in range(len(final_list)):
        cnd_length = len(final_list[x]['Candidate Name'].keys()) #{0,1},{0},{0}
        cnd_lengthList.append(cnd_length) #[2,1,1] length of candidate keys
    list_indexes = fndIndex_list(cnd_lengthList) #[0,1,2] indices of candidate keys
    for x in range(len(final_list)):
        for i in list_indexes: # length is 3, so it will start from [0,1,2] index 0,1,2 with the values [2,1,1]
            couty = 1
            if cnd_lengthList[2] < cnd_lengthList[0]: # 1)i=0,2 < 2 = False,2)i=1,1 < 2 = True,3)i=2,1 < 2 = True,
                print("case 1 : --- if cnd_lengthList[0] < cnd_lengthList[1] ",cnd_lengthList[2])
                if x == 0:
                    final_list[x]['Candidate Name'][x + 1] = 'N/A'
                    final_list[x]['Keyword'][x + 1] = 'N/A'
                    final_list[x]['Count'][x + 1] = 'N/A'
            """if i > cnd_lengthList[0]:  # 1)i=0,2 > 2 = False,2)i=1,1 > 2 = False,3)i=2,1 > 2 = False,
                print("case 2 : --- if cnd_lengthList[0] < cnd_lengthList[1]",i)
                if x == 1:
                    final_list[x]['Candidate Name'][x + 1] = 'N/A'
                    final_list[x]['Keyword'][x + 1] = 'N/A'
                    final_list[x]['Count'][x + 1] = 'N/A'"""

    print("wow-",final_list)

def fndIndex_list(elemnts):
    #elemnts = [2,1,1]
    index_list = []
    splt_indx_list = []
    for x in elemnts:
        g = list((i for i, n in enumerate(elemnts) if n == x))
        index_list.append(g)
        for y in index_list:
            for x in y:
                splt_indx_list.append(x)
    print(index_list)
    print(list(dict.fromkeys(splt_indx_list))," got the indices for the elements")
    return list(dict.fromkeys(splt_indx_list))
convert_dic()


def savechart():
    import matplotlib.pyplot as plt

    names = ['alex', 'simon', 'beta']
    values = [10, 20, 30]

    plt.rcParams["figure.figsize"] = (15,3)
    plt.bar(names, values)
    plt.suptitle('Average Resale Price (SGD) vs Flat Model')

    plt.xticks(rotation='1.5')

    plt.savefig('foo9.png', dpi=10)
    plt.show()



#savechart()
