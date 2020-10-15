import telegram
from telegram.ext import Updater, Dispatcher, CommandHandler
import numpy as np
import matplotlib.pyplot as plt
import os

masters = {}
room = {}
settings = {}
Key = lambda x:x

def lambda_handler(event, context):
    code = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" #len = 62
    bot = telegram.Bot(token=os.environ['bot_token'])
    bot.delete_webhook()
    #main function
    mid = float('inf')
    upd = None
    for up in bot.get_updates(): #pick smallest uid
        if mid > up.update_id:
            mid = up.update_id
            upd = up
    if upd is None:
        bot.set_webhook(os.environ['gateway'])
        return
    bot.send_message(int(os.environ['jid']), f"testing {mid}")
    chat_id = upd.message.chat_id
    messages = upd.message.text.split()
    if messages[0] == '/new':
        bot.send_message(int(os.environ['jid']), f"new command detected.")
        for item in masters['Items']:
            if chat_id == item['cid']:
                bot.send_message(chat_id, f"""이미 개설된 게임(item['rid'])이 있습니다.\n'/end' 명령어를 이용해 게임을 끝내고 다시 시도하십시오.""")
                bot.get_updates(offset=mid+1)
                bot.set_webhook(os.environ['gateway'])
                return
        key = np.random.randint(0,36,size=6)
        rcode = ""
        for i in key:
            rcode+=code[i]
        bot.send_message(chat_id, f"""새로운 방을 개설하였습니다.
        게임 방 코드는 아래와 같습니다.
        
        {rcode}
        
        친구들에게 방코드를 알려세요.
        방에 참가하는 명령어는 '/join {rcode}' 입니다.
        """)
        """
        table.put_item(Item = {
            'room' : 'master',
            'cid' : chat_id,
            'rid' : rcode
        })
        table.put_item(Item = {
            'room' : rcode,
            'cid' : chat_id,
        })
        """
    elif messages[0] == '/list':
        ent = ['theme','idot']
        
    elif messages[0] == '/start':
        for item in masters['Items']:
            if chat_id == item['cid']:
                # do game 
                bot.get_updates(offset=mid+1)
                bot.set_webhook(os.environ['gateway'])
                return
        bot.send_message(chat_id, 
f"""텔레그램 라이어 게임에 오신 것을 환영합니다.
새로 방을 만드시려면 
'/new' 커맨드를 입력해 주세요.

사용 가능한 명령어들에 대한 정보가 필요하시면 '/help' 커맨드를 입력하세요.
""")
        
    elif messages[0] == '/join':
        rid = {item['rid']:item['cid'] for item in masters['Items']}
        bot.send_message(int(os.environ['jid']), f"rid : {messages[1]}, db : {rid}")
        """
        if rid.get(messages[1].upper(), False):
            #members = table.query(
            #    KeyConditionExpression=Key('room').eq(messages[1])
            #)
            
            memid = [item['cid'] for item in members['Items']]
            if chat_id in memid:
                bot.send_message(chat_id, "이미 참가한 방입니다.")
            else:
                table.put_item(Item = {
                    'room' : messages[1].upper(),
                    'cid' : chat_id,
                })
                bot.send_message(chat_id, f"{messages[1].upper()} 방에 참가하였습니다.")
        else:
            bot.send_message(chat_id, "해당 방을 찾을 수 없습니다.")
        """
    elif messages[0] == '/end':
        pass
    elif messages[0] == '/set':
        ent = ['theme','liar','spy','mode']
        
    elif messages[0] == '/help':
        bot.send_message(chat_id,
f"""사용 가능한 명령어 모음
/new    - 게임 방 생성 (하나의 계정은 한 개의 방만 만들 수 있습니다.)
/start  - 게임 시작 (혹은 처음 안내)
/end    - 게임 종료. 방이 사라지며 되돌릴 수 없습니다.
/rule   - 게임의 룰을 소개하는 메세지를 받습니다.
/help   - 현재 메세지가 나타납니다.

/join [방 코드]     - 방에 참여합니다.
/list [옵션]        - 해당 [옵션]에 사용 가능한 값들의 리스트를 보여줍니다.
/set [옵션] [값]    - 해당 [옵션]을 해당 [값]으로 바꿉니다.
/settings           - 현재 방의 설정을 나타냅니다.
""")
    elif messages[0] == '/rule':
        pass
    elif messages[0] == '/settings':
        pass
    else:
        bot.send_message(int(os.environ['jid']),f"""{upd.effective_user.first_name} send a message.
        Full name : {upd.effective_user.full_name}
        chat_id : {upd.effective_chat.id}
        """)
        bot.forward_message(int(os.environ['jid']),upd.effective_chat.id,upd.message.message_id)
    
    bot.get_updates(offset=mid+1)
    bot.set_webhook(os.environ['gateway'])
    return masters



if __name__ =='__main__':
    TOKEN = os.getenv('TOKEN')
    PORT = os.environ.get('PORT')
    print(TOKEN)
