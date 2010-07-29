
import time

class Logger:

    def __init__(self, debug_mode):
        self.ui = None
        self.debug_mode = debug_mode
        self.span_end = "</style>"
        
    def set_ui(self, ui):
        self.ui = ui

    def span_start(self, color):
        return "<span style=\"color:" + color + ";\">"
    
    def generate_timestamp(self):
        localtime = time.localtime()
        hour = localtime.tm_hour
        if hour < 10:
            hour = "0" + str(hour)
        minute = localtime.tm_min
        if minute < 10:
            minute = "0" + str(minute)
        second = localtime.tm_sec
        if second < 10:
            second = "0" + str(second)
        timestamp = "%s:%s:%s" % (hour, minute, second)
        return timestamp
        
    def join_message(self, msg, param):
        msg_join = msg + " %s" % param
        return msg_join  
        
    def warning(self, message, param = None):
        if param != None:
            message = self.join_message(message, param)
        timestamp = self.generate_timestamp()
        post_timestamp = " "
        category = "[WARNING]:"
        html_message = timestamp + post_timestamp + self.span_start("#cdbc2a") + category + " " + message + self.span_end
        self.log(html_message, timestamp, post_timestamp, category, message)
        
    def error(self, message, param = None):
        if param != None:
            message = self.join_message(message, param)
        timestamp = self.generate_timestamp()
        post_timestamp = " --"
        category = "[ERROR]:"
        html_message = timestamp + self.span_start("white") + post_timestamp + self.span_end + self.span_start("red") + category + " " + message + self.span_end
        self.log(html_message, timestamp, post_timestamp, category, message)
            
    def info(self, message, param = None):
        if param != None:
            message = self.join_message(message, param)
        timestamp = self.generate_timestamp()
        post_timestamp = " ---"
        category = "[INFO]:"
        html_message = timestamp + self.span_start("white") + post_timestamp + self.span_end + self.span_start("black") + category + " " + message + self.span_end
        self.log(html_message, timestamp, post_timestamp, category, message)
        
    def auth(self, message, param = None):
        if param != None:
            message = self.join_message(message, param)
        timestamp = self.generate_timestamp()
        post_timestamp = " ---"
        category = "[AUTH]:"
        html_message = timestamp + self.span_start("white") + post_timestamp + self.span_end + self.span_start("green") + category + " " + message + self.span_end
        self.log(html_message, timestamp, post_timestamp, category, message)

    def config(self, message, param = None):
        if param != None:
            message = self.join_message(message, param)
        timestamp = self.generate_timestamp()
        post_timestamp = " -"
        category = "[CONFIG]:"
        html_message = timestamp + self.span_start("white") + post_timestamp + self.span_end + self.span_start("purple") + category + " " + message + self.span_end
        self.log(html_message, timestamp, post_timestamp, category, message)
        
    def network(self, message, param = None):
        if param != None:
            message = self.join_message(message, param)
        timestamp = self.generate_timestamp()
        post_timestamp = " "
        category = "[NETWORK]:"
        html_message = timestamp + post_timestamp + self.span_start("blue") + category + " " + message + self.span_end
        self.log(html_message, timestamp, post_timestamp, category, message)

    def network_error(self, message, param = None):
        if param != None:
            message = self.join_message(message, param)
        timestamp = self.generate_timestamp()
        post_timestamp = " "
        category = "[NETWORK ERROR]:"
        html_message = timestamp + post_timestamp + self.span_start("red") + category + " " + message + self.span_end
        self.log(html_message, timestamp, post_timestamp, category, message)

    def sync(self, message, param = None):
        if param != None:
            message = self.join_message(message, param)
        timestamp = self.generate_timestamp()
        post_timestamp = " ---"
        category = "[SYNC]:"
        html_message = timestamp + self.span_start("white") + post_timestamp + self.span_end + self.span_start("blue") + category + " " + message + self.span_end
        self.log(html_message, timestamp, post_timestamp, category, message)
        
    def sync_error(self, message, param = None):
        if param != None:
            message = self.join_message(message, param)
        timestamp = self.generate_timestamp()
        post_timestamp = " "
        category = "[SYNC ERROR]:"
        html_message = timestamp + post_timestamp + self.span_start("red") + category + " " + message + self.span_end
        self.log(html_message, timestamp, post_timestamp, category, message)
        
    def transfer(self, message, param = None):
        if param != None:
            message = self.join_message(message, param)
        timestamp = self.generate_timestamp()
        post_timestamp = " "
        category = "[TRANSFER]:"
        html_message = timestamp + post_timestamp + self.span_start("blue") + category + " " + message + self.span_end
        self.log(html_message, timestamp, post_timestamp, category, message)

    def transfer_error(self, message, param = None):
        if param != None:
            message = self.join_message(message, param)
        timestamp = self.generate_timestamp()
        post_timestamp = " "
        category = "[TRANSFER ERROR]:"
        html_message = timestamp + post_timestamp + self.span_start("red") + category + " " + message + self.span_end
        self.log(html_message, timestamp, post_timestamp, category, message)
        
    def log(self, html_message, timestamp, post_timestamp, category, message):
        if self.ui != None:
            self.ui.console_ui.text_area.appendHtml(html_message)
        if self.debug_mode:
            print "%s%s%s %s" % (timestamp, post_timestamp, category, message)

