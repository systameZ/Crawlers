import requests,lxml.html,json,time,csv
html=requests.get('https://shopsearch.taobao.com/'
                  'search?app=shopsearch&q=惠普打印机&imgfile=&commend=all&ssid=s5-e&search_type=shop&'
                  'sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20171008&loc=山东')
#链接中的q属性为搜索店铺的内容，loc为筛选的地区,至于其他的没有去研究= =
dic_all={}
def name(html):
    html_decode=html.content.decode('utf-8')
    tree=lxml.html.fromstring(html_decode)
    row  = tree.cssselect('script')#选取script标签
    global dic_all
    for con in row:
        if 'g_page_config' in con.text_content():
                print(con.text_content().split('g_srp_loadCss()')[0].split('=')[1][:-6])
            #try:
                js=json.loads(con.text_content().split('g_srp_loadCss()')[0].split('=')[1][:-6])#经过分析发现服务器返回的内容在script里面的一个字典里面。这一句为分割出该字典并且转换为json
            # except Exception as e:
            #     pass
    try:
        for i in range(len(js['mods']['shoplist']['data']['shopItems'])):#遍历这个字典里面的这个列表
            dic_all[js['mods']['shoplist']['data']['shopItems'][i]['title']] = js['mods']['shoplist']['data']['shopItems'][i]['shopUrl']#向我们的列表里面添加数据，K为title也就是店铺名称，value为shopUrl店铺链接
    except Exception as e:
        return ('OVER!')#如果遍历失败也就是不存在这个页面了返回一个结束标记。这里的容错是没做好的。。。
name(html)
for i in range(20,800,20):#第一页搜索出来之后是没有s属性的，从第二页开始有s属性从20开始。最多会有100页的搜索结果。这里我的搜索只有38页所以设置了800
    time.sleep(1)
    print(i)
    html_2 = requests.get('https://shopsearch.taobao.com/'
                        'search?app=shopsearch&q=惠普打印机&imgfile=&commend=all&ssid=s5-e&search_type=shop&'
                        'sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20171008&loc=山东&s='+str(i))
                        #这个地方的连接不同之处为最后的s属性，经过试验发现为页面的编号，间隔为20
    if name(html_2)=='OVER!':
        break
write=csv.writer(open('name.csv','w',newline=""))
for k,v in dic_all.items():
        write.writerow([k,v])
"""
多次请求不同页面，分析链接的不同。。
https://shopsearch.taobao.com/search?app=shopsearch&
q=%E6%83%A0%E6%99%AE&js=1&initiative_id=staobaoz_20171008&ie=utf8&loc=%E5%B1%B1%E4%B8%9C
https://shopsearch.taobao.com/search?app=shopsearch&q=%E6%83%A0%E6%99%AE&
js=1&initiative_id=staobaoz_20171008&ie=utf8&loc=%E5%B1%B1%E4%B8%9C&s=20
https://shopsearch.taobao.com/search?app=shopsearch&q=惠普&
js=1&initiative_id=staobaoz_20171008&ie=utf8&loc=山东
https://shopsearch.taobao.com/search?app=shopsearch&q=%E6%83%A0%E6%99%AE&js=1&initiative_id=staobaoz_20171008&ie=utf8&loc=%E5%B1%B1%E4%B8%9C&s=60&data-key=s&data-value=80
https://shopsearch.taobao.com/search?app=shopsearch&q=%E6%83%A0%E6%99%AE&js=1&initiative_id=staobaoz_20171008&ie=utf8&loc=%E5%B1%B1%E4%B8%9C&s=80&data-key=s%2Cps&data-value=60%2C1
"""