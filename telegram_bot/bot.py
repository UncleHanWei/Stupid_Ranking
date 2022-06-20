from dotenv import load_dotenv
import os, threading
from time import sleep
import pymongo
import requests
from bson.objectid import ObjectId

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters


def button(update: Update, context: CallbackContext) -> None :
    global user_status, playList, user
    username = update.effective_user.username
    id = update.effective_user.id
    query = update.callback_query

    if username in user_status :
        # 處理被通報的資料
        report_list = user_status[username]
        handle = report_list[int(query.data)]
        user_status[username] = ['handle', handle]

        keyboard = [
            [KeyboardButton(text='confirm'), KeyboardButton(text='delete')],
            [KeyboardButton(text='cancel')]
        ]
        text = ''
        text += 'Telegram:' + handle['telegram'] + '\n'
        text += '姓名:' + handle['name'] + '\n'
        text += '事蹟:' + handle['deed'] + '\n'
        text += '分數:' + handle['point']
        query.edit_message_text(text)
        update.callback_query.message.reply_text('請選擇如何處置這則通報', reply_markup=ReplyKeyboardMarkup(keyboard=keyboard))


def msg(update: Update, context: CallbackContext) :
    global user_status, db
    username = update.effective_user.username
    id = update.effective_user.id
    msg = update.message.text
    if username in user_status :
        if user_status[username] == 'report' :
            data = msg.split('/')
            if len(data) != 4 :
                update.message.reply_text('格式錯誤')
                return
            if not data[0].startswith('@') :
                update.message.reply_text('格式錯誤')
                return

            data = {"telegram":data[0], "name":data[1], "deed":data[2], "point":data[3]}
            reports = db.reports
            res = reports.insert_one(data)
            if res.inserted_id :
                update.message.reply_text('成功')
        elif user_status[username][0] == 'handle' :
            keyboard = [
                        [KeyboardButton(text='/report'), KeyboardButton(text='/rank'), KeyboardButton(text='/list')],
                        [KeyboardButton(text='/start')]
                    ]
            if msg == 'confirm' :
                # 戳 API
                data = user_status[username][1]
                data = {"telegram":data['telegram'],
                        "name":data['name'],
                        "deed":data['deed'],
                        "point":data['point']
                    }
                r = requests.post('http://127.0.0.1:8787/api/add/deed', data=data)
                if r.status_code == 200 :
                    reports = db.reports
                    # print(user_status[username][1]['_id'])
                    res = reports.delete_one({'_id':user_status[username][1]['_id']})
                    # print(res.deleted_count, "個資料已刪除")
                    if update.message.chat.type == 'private' :
                        update.message.reply_text('操作成功', reply_markup=ReplyKeyboardMarkup(keyboard=keyboard))
                    else :
                        update.message.reply_text('操作成功')
                else :
                    if update.message.chat.type == 'private' :
                        update.message.reply_text('失敗，請聯絡系統管理員檢查', reply_markup=ReplyKeyboardMarkup(keyboard=keyboard))
                    else :
                        update.message.reply_text('失敗，請聯絡系統管理員檢查')

            elif msg == 'delete' :
                # 純刪除
                reports = db.reports
                res = reports.delete_one({'_id':user_status[username][1]['_id']})
                # print(res.deleted_count, "個資料已刪除")
                if update.message.chat.type == 'private' :
                    update.message.reply_text('操作成功', reply_markup=ReplyKeyboardMarkup(keyboard=keyboard))
                else :
                    update.message.reply_text('操作成功')
            elif msg == 'cancel' :
                if update.message.chat.type == 'private' :
                    update.message.reply_text('編輯取消', reply_markup=ReplyKeyboardMarkup(keyboard=keyboard))
                else :
                    update.message.reply_text('編輯取消')
            user_status[username] = None

def report_list(update: Update, context: CallbackContext) -> None :
    global uncle_id, db, user_status
    id = update.effective_user.id
    username = update.effective_user.username
    if id != uncle_id :
        update.message.reply_text('你不是管理員喔')
        return
    # 撈出所有 report
    reports = db.reports
    data = list(reports.find())
    user_status[username] = data
    reportList = []
    for i in range(len(data)) :
        text = ''
        text += 'Telegram:' + data[i]['telegram'] + '\n'
        text += '姓名:' + data[i]['name'] + '\n'
        text += '事蹟:' + data[i]['deed'] + '\n'
        text += '分數:' + data[i]['point']
        reportList.append(
            [InlineKeyboardButton(text=text, callback_data=i)]
        )
    update.message.reply_text('搜尋結果', reply_markup=InlineKeyboardMarkup(reportList))

def rank(update: Update, context: CallbackContext) -> None :
    global uncle_id
    id = update.effective_user.id
    rank_list = requests.get('http://127.0.0.1:8787/api/get/rank').json()
    update.message.reply_text('以下為目前排名')
    reply = ''
    for i in range(len(rank_list)) :
        reply += 'No.' + str(i+1) + ' ' + rank_list[i]['name'] + ' ' + str(rank_list[i]['stupid_point']) + ' 分\n'
    update.message.reply_text(reply)

def report(update: Update, context: CallbackContext) -> None :
    global uncle_id, user_status
    username = update.effective_user.username
    user_status[username] = 'report'
    reply = '請按照以下格式提供回報:\n'
    reply += '@誰 叫什麼名字 做了什麼 加幾分?\n'
    reply += '四個欄位中間用一個/隔開\n'
    reply += 'Ex:\n'
    reply += '@Stupid_Ranking_bot/笨蛋排行機器人/當機/+10'
    
    update.message.reply_text(reply)

def start(update: Update, context: CallbackContext) -> None :
    global uncle_id
    id = update.effective_user.id
    reply_str = '歡迎使用 Stupid Ranking Bot'
    keyboard = [
        [KeyboardButton(text='/report'), KeyboardButton(text='/rank')],
        [KeyboardButton(text='/start')]
    ]
    if id == uncle_id :
        keyboard = [
            [KeyboardButton(text='/report'), KeyboardButton(text='/rank'), KeyboardButton(text='/list')],
            [KeyboardButton(text='/start')]
        ]
    if update.message.chat.type == 'private' :
        update.message.reply_text(reply_str, reply_markup=ReplyKeyboardMarkup(keyboard=keyboard))
    else :
        update.message.reply_text(reply_str)
    


# global variables
admin = { 413549984: "uncle", 655770404: "庭" }
uncle_id = 413549984
user_status = dict()

if __name__ == "__main__" :
    try :
        load_dotenv()
        TOKEN = os.getenv("TOKEN")
        updater = Updater(TOKEN)
        # db setting
        DB_HOST = os.getenv("DB_HOST")
        db_client = pymongo.MongoClient(DB_HOST)
        db = db_client['Stupid_Ranking']
        
        # set handler
        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(CommandHandler('report', report))
        updater.dispatcher.add_handler(CommandHandler('rank', rank))
        updater.dispatcher.add_handler(CommandHandler('list', report_list))
        updater.dispatcher.add_handler(CallbackQueryHandler(button))
        updater.dispatcher.add_handler(MessageHandler(~Filters.command, msg))

        updater.start_polling()
        print('bot start listening...')
        updater.idle()
    finally :
        print('program stop.')