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