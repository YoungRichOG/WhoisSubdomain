#! /usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Author:YoungRichOG
Hacking Everything :-)
2020/07/17
'''

import chinaz


if __name__ == '__main__':
	with open('url.txt','r') as f:
		for i in f:
			print('[*] 当前任务:%s' %i.rstrip())
			get_whois = chinaz.get_whois(domain=i.rstrip())

			try:
				get_contacts_info = chinaz.get_contacts_info(contacts=get_whois[1])
				get_email_info = chinaz.get_email_info(email=get_whois[0])
				get_icp_info = chinaz.get_icp_info(domain=i.rstrip())
				print('[*] get_contacts_info模块:',get_contacts_info)
				print('[*] get_email_info模块:',get_email_info)
				print('[*] get_icp_info模块:',get_icp_info)
				new_list = get_email_info + get_contacts_info + get_icp_info
				count = 0
				for s in list(set(new_list)):
					count += 1
					with open('res.txt','a+') as ff:
						ff.write(i.rstrip()+','+s+'\n')
				print('[*] 共发现域名:%s个' % count)
				print('*' * 30 + i.rstrip() + '整体结束' + '*' * 30)
			except Exception as e:
				print('发生错误:',e)