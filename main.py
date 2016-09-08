#!/usr/local/bin/python
# coding: utf-8

from lxml import html
import requests, re, time
import email_me, utils, settings

# Iterate over all URLS from settings
for url in settings.URLS :
	# Load html page
	page = requests.get(settings.URLS[url])
	tree = html.fromstring(page.content)
	# Select all <a/> elements by class name
	links_el = tree.xpath('//a[@class="list_item clearfix trackable"]')

	### This algorithm is based on the date of the post
	### Also, I had to do lots of sketchy conditions to get the element I wanted
	### maybe there's a better way to scrap this data, feel free to improve it !
	try:
		# Read last alert time
		last_alert_time = utils.read_file('last_alert_'+ url +'.txt')
		for i, el in enumerate(reversed(links_el), start=0):
			# Get date element of classified ad
			date = el.xpath('.//p[@class="item_supp"]/text()')
			# Get link element of classified ad
			link = tree.xpath('.//a[@class="list_item clearfix trackable"]/@href')
			day_hour = ''
			for d in date:
				# Remove all useless char from html element
				day_hour = ''.join(map(lambda s: re.sub('\s+', '', s),d ))
			if day_hour != '':
				# We have now someting like : <day>,<hour>:<minute>
				# So we split the string
				splitted_day_hour = day_hour.split(',')
				day = splitted_day_hour[0]
				hour = splitted_day_hour[1]
				if len(splitted_day_hour) == 2:
					# If the classified ad is from today
					if day == "Aujourd'hui":
						# And is not the same and newer than the last
						if hour != last_alert_time and hour > last_alert_time:
							link = link[0][2:-8]
							# Here I'm sending an email but you can do whatever you want, for exemple connect it to IFTTT maker channel, or send you a tweet
							# Send the email
							# First param is the object of the mail, second param is his content
							email_me.send_email("Alerte "+ url +" !", "Nouvelle annonce detectée à : " + time.strftime('%H:%M:%S')+".\n" + link)
							# Save the new alert hour
							utils.write_to_file('last_alert_'+ url +'.txt', hour)
							print("email send, new last_alert_time : ", hour)
	# On first execution of the script, create the last_alert.txt files
	except FileNotFoundError:
		open('last_alert_'+ url +'.txt', 'a')
