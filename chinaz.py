#! /usr/bin/env python3
# -*- coding:utf-8 -*-


'''
Author:YoungRichOG
Hacking Everything :-)
2020/07/17
'''

import requests,re,time,json


headers = {
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
}

def get_whois(domain):
	time.sleep(2)
	email_re = '(/reverse\?ddlSearchMode=1.*)">'
	domain_re = '(/reverse\?host=.*&ddlSearchMode=2)"'

	url = "http://whois.chinaz.com/{}".format(domain)
	r = requests.get(url=url,headers=headers)
	print('[*] 当前状态码:%s' %r.status_code)
	try:									
		email = re.findall(email_re,r.text)
		contacts = re.findall(domain_re,r.text)
	except Exception as e:
		print(e)
	if email == []:
		email = 'null'
	else:
		email = email[0]
	if contacts == []:
		contacts ='null'
	else:
		contacts = contacts[0]

	email = check_blacklist(email,contacts)
	return email,contacts

def get_email_info(email):
	domain = []
	if email != 'null':
		print('[*] 开始获取邮箱反查')
		for i in range(1,101):
			time.sleep(2)
			url = "http://whois.chinaz.com{}&st=&startDay=&endDay=&wTimefilter=$wTimefilter&page={}".format(email,i)
			domain_re = '<div class="listOther"><a href="/(.*?)" target="_blank">'
			r = requests.get(url=url,headers=headers)
			print('[*] 当前状态码:%s' %r.status_code)
			domain_res = re.findall(domain_re,r.text)
			try:
				current_page = re.findall('<span class="col-gray02">共(.*)页，到第</span>',r.text)[0]
			except:
				current_page = 0
			if int(current_page) > 10:
				break
			if '暂无相关数据' not in r.text:
				domain.append(re.findall(domain_re,r.text))
			else:
				break
	else:
		print('[*] 获取邮箱反查失败')

	if domain !=[]:
		return domain[0]
	else:
		return domain

def get_contacts_info(contacts):
	domain = []
	email_list = []
	bbb = []
	email = []
	if contacts != 'null':
		print('[*] 开始获取联系人反查')
		for i in range(1,101):
			time.sleep(2)
			print('[*] 第%s页' % i)
			domain_re = '<div class="listOther"><a href="/(.*?)" target="_blank">'
			email_re = '\?host=.*?&domain=.*?&ddlSearchMode=1' 
			url = "http://whois.chinaz.com{}&st=&startDay=&endDay=&wTimefilter=$wTimefilter&page={}".format(contacts,i)
			r = requests.get(url=url,headers=headers)
			domain_res = re.findall(domain_re,r.text)
			email_list.append(re.findall(email_re,r.text))


			try:
				current_page = re.findall('<span class="col-gray02">共(.*)页，到第</span>',r.text)[0]
			except:
				current_page = 0
			if int(current_page) > 10:
				break
			if '暂无相关数据' not in r.text:
				for tmp in domain_res:
					domain.append(tmp)
			else:
				break
	else:
		print('[*] 获取联系人反查失败')

	for ii in email_list:
		if ii != []:
			for ss in ii:
				oo = re.findall('\?host=(.*?)&',ss)
				for mm in oo:
					if mm not in email:
						email.append(mm)
						bbb.append(ss)

	contacts_reverse_list = contacts_reverse_query(bbb)
	for tmp in contacts_reverse_list:
		for jj in tmp:
			domain.append(jj)

	return domain

def get_icp_info(domain):
	domain_list = []
	url = "http://icp.chinaz.com/ajaxsync.aspx?at=beiansl&callback=jquery&host={}&type=host".format(domain)
	r = requests.get(url=url,headers=headers)
	domain_re = re.findall('MainPage:"(.*?)"',r.text)
	print('[*] 开始获取ICP备案反查')
	print('[*] 当前状态码:%s' %r.status_code)
	for i in domain_re:
		time.sleep(2)
		if ' ' in i:
			domain_list.append(i.replace(' ','\n{},'.format(domain)))
		else:
			domain_list.append(i)
	return domain_list

def contacts_reverse_query(bbb):
	domain = []
	for a in bbb:
		print('[*] 开始获取联系人邮箱反查')
		for i in range(1,101):
			time.sleep(2)
			print('[*] 第%s页' % i)
			domain_re = '<div class="listOther"><a href="/(.*?)" target="_blank">'
			url = "http://whois.chinaz.com/reverse{}&st=&startDay=&endDay=&wTimefilter=$wTimefilter&page={}".format(a,i)
			r = requests.get(url=url,headers=headers)
			print('[*] 当前状态码:%s' %r.status_code)
			domain_res = re.findall(domain_re,r.text)
			try:
				current_page = re.findall('<span class="col-gray02">共(.*)页，到第</span>',r.text)[0]
			except:
				current_page = 0
			if int(current_page) > 10:
				break
			if '暂无相关数据' not in r.text:
				domain.append(domain_res)
			else:
				break
	return domain


def check_blacklist(email,contacts):
	email_blacklist = [
		'xinnet.com','service.aliyun.com','35.cn','markmonitor.com','sfn.cn','brandma.co','ename.com','web.com'
		]

	email_re = 'host=(.*)&'
	try:
		email_res = re.findall(email_re,email)[0].split('@')[1]
		if email_res in email_blacklist:
			email = 'null'
	except:
		print('[*] 没有获取到邮箱')
		email = 'null'

	return email