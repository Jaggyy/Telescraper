from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import os, sys
import configparser
import random
import traceback
import csv
import time



class scraper:

    def heading(self):
        print(f"""{cy}Welcome to Telegram scraper""")
        print("\033[1;37m")
    
    def authorized(self , client):
        return client.is_user_authorized()


    def login(self):
        self.heading()
        try:   
            client.connect()
            if not self.authorized(client):
                client.send_code_request(phone_number)
                self.heading()
                client.sign_in(phone_number, input('[+] Enter the verification code: '))
                self.extractgroup()
            else:
                self.extractgroup()

        except KeyError:
            print("\033[91m[!] run \033[92mpython3 setup.py \033[91mfirst !!\n")
            print("\033[1;37m")

    def extractgroup(self):
        
        result =  client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash = 0
                ))
        chats.extend(result.chats)

        for chat in chats:
            try:
                if chat.megagroup== True:
                    groups.append(chat)
            except:
                continue
        
        print('[+] Choose a group to scrape members:')
        for i, g in enumerate(groups):
            print('['+str(i)+']' + ' - ' + g.title)
        print('')

        g_index = input("[+] Enter a Number: ")
        
        target_group= groups[int(g_index)]

        print('extracting data, please wait...')

        all_user = []
        all_user = client.get_participants(target_group)
        print('[+] Saving data in files...')
        with open("members.csv","w",encoding='UTF-8') as f:
            writer = csv.writer(f,delimiter=",",lineterminator="\n")
            writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
            for user in all_user:
                username = user.username or ""
                first_name = user.first_name or ""
                last_name = user.last_name or ""
                name= (first_name + ' ' + last_name).strip()
                writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])
        print('[+] Members scraped successfully!')

    def addusers(self):
        users = []
        with open(r"members.csv", encoding='UTF-8') as f:  #Enter your file name
            rows = csv.reader(f,delimiter=",",lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {
                    'username': row[0],
                    'id': int(row[1]),
                    'access_hash': int(row[2]),
                    'name': row[3],
                }

                users.append(user)
        print('Choose a group to add members: ')

        for i, group in enumerate(groups):
            print(str(i) + '- ' + group.title)

        g_index = input("Enter a Number: ")
        target_group = groups[int(g_index)]
        target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)
        
        n=0
        for user in users:
            n += 1
            if n % 80 == 0:
                time.sleep(60)
            try:
                print("Adding {}".format(user['id']))
                user_to_add = InputPeerUser(user['id'], user['access_hash'])
                client(InviteToChannelRequest(target_group_entity, [user_to_add]))
                stopforradomtime =random.randrange(60, 160)
                print(f"Waiting for {stopforradomtime} Seconds ..." ,)
                time.sleep(stopforradomtime)
            except PeerFloodError:
                print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
                print("Waiting {} seconds".format(100))
                time.sleep(100)
            except UserPrivacyRestrictedError:
                print("The user's privacy settings do not allow you to do this. Skipping ...")
                print("Waiting for 5 Seconds ...")
                time.sleep(random.randrange(0, 5))
            except:
                traceback.print_exc()
                print("Unexpected Error! ")
                continue


if __name__ =="__main__":
    # color code for command line
    cy="\033[1;36m"     
    # add your telegram api key here
    api_id = ''
    # add your telegram api hash here
    api_hash = ''
    # your phone number register for api key
    phone_number = '+919876543120'
    chats = []
    last_date = None
    chunk_size = 200
    groups=[]

    client = TelegramClient(phone_number, api_id, api_hash)
    scraper().login()

    if(input("Would you like to add people to your group: (y/n)")=="y"):
        scraper().addusers()
    
