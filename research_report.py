import requests
def search():
    while True:
        keyword = input('请输入关键词:')
        param = {
            'keyWord':keyword,
            'maxNum':10
        }
        r = requests.post('http://www.cninfo.com.cn/new/information/topSearch/query',params=param)
        data = []
        for i in r.json():
            if i['category'] == 'A股':
                data.append(i)
        if len(data) == 0:
            print('无搜索结果,请重新输入关键词:')
            continue
        index = 1
        result_dict = {}
        for row in data:
            result_dict[str(index)] = row
            print('【序号-{}】 代码-{} 名称-{}'.format(index,row['code'],row['zwjc']))
            index += 1
        print('序号-0 【我想重新选择序号】\n')
        while True:
            choice = input('请输入序号:')
            if result_dict.get(choice) != None:
                return result_dict[choice]
            elif choice == '0':
                break
            else:
                print('输入无效的数字,请重新输入')
def select(code,orgid):
    while True:
        category_dict = {
            '1':'category_ndbg_szsh;',
            '2':'category_bndbg_szsh;',
            '3':'category_rcjy_szsh;'
        }
        number = input('请输入选择类型序号(1、年报 2、半年报 3、日常经营):')
        if category_dict.get(number) != None:
            category = category_dict[number]
            break
        else:
            print('未选择任何搜索类型，请重新输入\n')
    start = input('请输入搜索范围起始时间(例如 2021-01-01):')
    end = input('请输入搜索范围结束时间(例如 2022-01-01):')
    if code[0] == '6':
        column = 'sse'
        plate = 'sh'
    else:
        column = 'szse'
        plate = 'sz'
    page_num = 1
    pdf_list = []
    while True:
        data = {
            'stock':'{},{}'.format(code,orgid),
            'tabName':'fulltext',
            'pageSize':30,
            'column':column,
            'category':category,
            'plate':plate,
            'seDate':'{}~{}'.format(start,end),
            'searchkey':'',
            'secid':'',
            'sortName':'',
            'sortType':'',
            'isHLtitle':'true'
        }
        r = requests.post('http://www.cninfo.com.cn/new/hisAnnouncement/query',data=data)
        j_son = r.json()
        if j_son['announcements'] == None:
            print('无搜索结果')
            break
        for i in j_son['announcements']:
            pdf_list.append([i['announcementTitle'],i['adjunctUrl']])
        if j_son['hasMore'] != True:
            break
        page_num += 1
    return pdf_list
def download(pdf_list):
    for item in pdf_list:
        pdf_r = requests.get('http://static.cninfo.com.cn/{}'.format(item[1]))
        file_path = 'E:\python\Python爬虫\爬取的信息\PDF\研报/{}.pdf'.format(item[0])
        with open(file_path,'wb')as f:
            f.write(pdf_r.content)
        print('已完成{}的下载'.format(item[0]))
def main():
    info = search()
    pdf_list = select(info['code'],info['orgId'])
    download(pdf_list)
main()