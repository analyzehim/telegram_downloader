from telegram_proto import Telegram, log_event
import time



def check_updates():
    parameters_list = telebot.get_updates()
    if not parameters_list:
        return 0
    for parameters in parameters_list:
        print parameters
        continue
        run_command(*parameters)

#
# def run_command(name, from_id, cmd, author_id, date):
#     global BOT_MODE
#     global EXIT_MODE
#     print 1
#     try:
#         add_user(from_id, name)
#     except:
#         add_user(from_id, from_id)
#     if cmd == '/help':
#         telebot.send_text(from_id, 'No help today. Sorry, %s' % name)
#
#     if cmd == '/start':
#         telebot.send_text(from_id, "Start!")
#         key, keyboard = get_keyboard()
#         put_user_answer(from_id, key)
#         try:
#             telebot.send_photo(from_id, 'words/'+key + '.png')
#         except:
#             telebot.send_photo(from_id, 'words/' + key + '.PNG')
#
#         telebot.send_text_with_keyboard(from_id, "_", keyboard)
#
#     else:
#         print 2
#         right_answer = get_user_answer(from_id)
#         print right_answer
#         if right_answer:
#             if right_answer == cmd.encode('utf-8'):
#                 telebot.send_text(from_id, "Right!")
#                 add_user_info(from_id, 1)
#             else:
#                 telebot.send_text(from_id, "False, right answer: {0}".format(right_answer))
#                 add_user_info(from_id, 0)
#         else:
#             telebot.send_text(from_id, "Start!")
#
#         key, keyboard = get_keyboard()
#         put_user_answer(from_id, key)
#     print 3
#     time.sleep(1)
#     path= 'words/' + key + '.png'
#     try:
#         telebot.send_photo(from_id, 'words/' + key + '.png')
#     except:
#         telebot.send_photo(from_id, 'words/' + key + '.PNG')
#     telebot.send_text_with_keyboard(from_id, "_", keyboard)

if __name__ == "__main__":
    telebot = Telegram()
    telebot.send_text(telebot.admin_id, "Run on {0}".format(telebot.host))
    while True:
        try:
            if check_updates() != 1:
                        time.sleep(telebot.Interval)
        except KeyboardInterrupt:
            print 'Interrupt by user..'
            break
        except Exception, e:
            log_event(str(e))