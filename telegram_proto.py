# -*- coding: utf-8 -*-
import requests
import time
import socket
import filecmp
import json
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# requests.packages.urllib3.disable_warnings()  # Подавление InsecureRequestWarning, с которым я пока ещё не разобрался
ADMIN_ID = 74102915  # My ID


def get_token():
    with open('token', 'r') as f:
        token = f.read()
        return token


class Telegram:
    def __init__(self, file="_"):
        self.file = file
        self.TOKEN = get_token()
        self.URL = 'https://api.telegram.org/bot'
        self.admin_id = ADMIN_ID
        self.offset = 0

        self.host = socket.getfqdn()
        self.Interval = 2
        log_event("Init " + str(self.file) + " completed, host: " + str(self.host))

    def get_updates(self):
        data = {'offset': self.offset + 1, 'limit': 5, 'timeout': 0}
        request = requests.post(self.URL + self.TOKEN + '/getUpdates', data=data, verify=False)
        if (not request.status_code == 200) or (not request.json()['ok']):
            return False

        if not request.json()['result']:
            return
        parametersList = []
        print request.json()
        for update in request.json()['result']:
            print "-------\n-------"
            print update
            if 'message' in update and 'photo' in update['message']:
                photo_info = update['message']['photo']
                file_id = self.get_file_id(photo_info)
                file_date = update['message']['forward_date']
                print "___", file_date, file_id
                file_info = self.get_file(file_id, file_date)
                #self.send_text(self.admin_id, file_info)
                time.sleep(1)
                self.offset = update['update_id']
                continue
            if 'message' in update and 'video' in update['message']:
                video_info = update['message']['video']
                print video_info
                print "  ____"
                #file_id = self.get_file_id(video_info)
                file_id = video_info['file_id']
                print file_id
                file_date = update['message']['forward_date']
                print "___", file_date, file_id
                file_info = self.get_file(file_id, file_date)
                #self.send_text(self.admin_id, file_info)
                time.sleep(1)
                self.offset = update['update_id']
                continue

            if 'message' not in update or 'text' not in update['message']:
                self.offset = update['update_id']
                continue
            if 'forward_from' in update['message']:
                print update['message']['forward_from']
            self.offset = update['update_id']



            from_id = update['message']['chat']['id']  # Chat ID
            author_id = update['message']['from']['id']  # Creator ID
            message = update['message']['text']
            date = update['message']['date']
            #print update
            name = from_id
            # try:
            #     name = update['message']['chat']['first_name']
            # except:
            #     name = update['message']['from']['first_name']
            parameters = (name, from_id, message, author_id, date)
            parametersList.append(parameters)
            try:
                log_event('from %s (id%s): "%s" with author: %s; time:%s' % parameters)
            except:
                pass
        return parametersList

    def send_text_with_keyboard(self, chat_id, text, keyboard):
            try:
                log_event('Sending to %s: %s; keyboard: %s' % (chat_id, text, keyboard))  # Logging
            except:
                log_event('Error with LOGGING')
            json_data = {"chat_id": chat_id, "text": text,
                         "reply_markup": {"keyboard": keyboard, "one_time_keyboard": True}}
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', json=json_data)  # HTTP request

            if not request.status_code == 200:  # Check server status
                return False
            return request.json()['ok']  # Check API

    def send_text(self, chat_id, text):
            try:
                log_event('Sending to %s: %s' % (chat_id, text))  # Logging
            except:
                log_event('Error with LOGGING')
            data = {'chat_id': chat_id, 'text': text}  # Request create
            #print text
            proxies = {'http':'socks5://161.35.70.249:1080', 'https':'socks5://161.35.70.249:1080'}
            print self.URL + self.TOKEN + '/sendMessage', data, proxies
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', data=data, verify=False)  # HTTP request
            print request.text
            if not request.status_code == 200:  # Check server status
                return False
            return request.json()['ok']  # Check API

    def send_text_markdown(self, chat_id, text):
            try:
                log_event('Sending to %s: %s' % (chat_id, text))  # Logging
            except:
                log_event('Error with LOGGING')
            data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}  # Request create
            #print text
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', data=data, verify=False)  # HTTP request
            print request.text
            if not request.status_code == 200:  # Check server status
                return False
            return request.json()['ok']  # Check API

    def get_file_id(self, photo_info):
        max_size = 0
        file_id = 0
        print 2
        for photo in photo_info:
            if photo['file_size'] >= max_size:
                file_id = photo['file_id']
        print 3
        return file_id


    def get_file(self, file_id, file_date):
        try:
            log_event('get file_id: %s' % (file_id))  # Logging
        except:
            log_event('Error with LOGGING')
        request = requests.post(self.URL + self.TOKEN + '/getFile?file_id={0}'.format(file_id), verify=False)  # HTTP request
        if not request.json()['ok']:
            print "ERRRORRRRR", file_id, file_date, request.text
            print "ERRRORRRRR", file_id, file_date, request.text
            print "ERRRORRRRR", file_id, file_date, request.text
            time.sleep(60)
            return
        print request.json()['result']['file_path']
        file_type = request.json()['result']['file_path'].split('.')[-1]
        self.download_file(request.json()['result']['file_path'], file_date, file_type)
        if not request.status_code == 200:  # Check server status
            return False
        return request.json()['ok']  # Check API

    def download_file(self, path, file_date, file_type):
        url = "https://api.telegram.org/file/bot" + self.TOKEN + '/' + path
        file_name = 'C:\Users\Raev_e\Downloads\{0}.{1}'.format(str(file_date), file_type)
        temp_name = 'C:\Users\Raev_e\Downloads\pemp.{0}'.format(file_type)

        request = requests.get(url, verify=False)
        print request.status_code, url
        with open(temp_name, 'wb') as f:
            f.write(request.content)

        while(True):
            if os.path.exists(file_name):
                print "File {0} already exist!".format(file_date)
                if filecmp.cmp(file_name, temp_name):
                    print "Cmp show identical file {0} already exist!".format(file_date)
                    os.remove(temp_name)
                    break
                else:
                    file_date += 1
                    file_name = 'C:\Users\Raev_e\Downloads\{0}.{1}'.format(str(file_date), file_type)
                    print "New file_name, {0}".format(file_date)
                    continue
            else:
                print "Create new file {0}".format(file_date)
                os.rename(temp_name, file_name)
                break
        return


    def send_photo(self, chat_id, imagePath):
        log_event('Sending photo to %s: %s' % (chat_id, imagePath))  # Logging
        data = {'chat_id': chat_id}
        files = {'photo': (imagePath, open(imagePath, "rb"))}
        requests.post(self.URL + self.TOKEN + '/sendPhoto', data=data, files=files, verify=False)
        request = requests.post(self.URL + self.TOKEN + '/sendPhoto', data=data, files=files, verify=False)  # HTTP request
        if not request.status_code == 200:  # Check server status
            return False

        return request.json()['ok']  # Check API

    def ping(self):
            log_event('Sending to %s: %s' % (self.chat_id, 'ping'))
            data = {'chat_id': self.chat_id, 'text': 'ping'}
            requests.post(self.URL + self.TOKEN + '/sendMessage', data=data, verify=False)  # HTTP request


def log_event(text):
        f = open('hebrew_log.txt', 'a')
        event = '%s >> %s' % (time.ctime(), text)
        print event + '\n'
        f.write(event + '\n')
        f.close()
        return