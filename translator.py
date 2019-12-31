from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities as DC
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import win32clipboard as wc
import win32con
import time
# * Selenium APIS: https://selenium.dev/selenium/docs/api/py/api.html
# Chrome driver and chrome executable path
# Set absolute path or leave it be(will search in $PATH)
CHROME_PATH = r'chrome'
# Set absolute path or leave it be(will search in $PATH)
CHROME_DRIVER_PATH = r'chromedriver'
REFRESH_RATE = 10  # Clipboard refresh rate, in Hz(times per second)
SLICE_THRESHOLD = 4000
WINDOW_POSITION = (-7, 0)
WINDOW_SIZE = (530, 1057)
translators = {
    "google": "https://translate.google.cn",
    "baidu": "https://fanyi.baidu.com",
    "bing": "https://cn.bing.com/translator?to=zh-Hans",
}
selectors = {
    "google": "#source",
    "baidu": "#baidu_translate_input",
    "bing": "#tta_input_ta",
}
copiers = {
    "google": "copybutton"
}
output = {
    "google": "translation"
}
input_id = {
    "google": "source"
}
ENGINE = "google"
TRANSLATE_SERVER_URL = translators[ENGINE]
TRANSLATE_INPUTBOX_CSS_SELECTOR = selectors[ENGINE]
TRANSLATE_OUTPUTBOX_CLASS_NAME = output[ENGINE]
TRANSLATE_COPIER_BUTTON_CLASS_NAME = copiers[ENGINE]
TRANSLATE_INPUT_ID = input_id[ENGINE]


def readyToBeginActions(self):
    # Returns whether the desired element is found.
    # Used when trying to begin action while your page is not fully loaded
    # Can be easily modified to search for multiple css elements
    try:
        self.find_element_by_css_selector(TRANSLATE_INPUTBOX_CSS_SELECTOR)
        return True
    except:
        return False


def readyToCopiedTranslated(self):
    # Returns whether the desired element is found.
    # Used when trying to begin action while your page is not fully loaded
    # Can be easily modified to search for multiple css elements
    try:
        self.find_element_by_class_name(TRANSLATE_OUTPUTBOX_CLASS_NAME)
        return True
    except:
        return False


class Chrome(object):
    # Chrome webdriver class
    def __init__(self):
        options = webdriver.ChromeOptions()
        # This capability is needed if you want to use the wait until function of the driver
        capabilities = DC.CHROME
        capabilities["pageLoadStrategy"] = "none"
        # * These commented lines forbids chrome to load pictures(which might be a performance boost)
        # * A lot of other things can also be achieved by this preference
        # prefs = {
        #     'profile.default_content_setting_values': {
        #         'images': 2
        #     }
        # }
        # options.add_experimental_option('prefs', prefs)

        # Changing this so that previous chrome options may not be corrupted
        # and this line make sure that the argument exists
        # options._arguments = [] if options._arguments is None else options._arguments
        # it is not recommended to forceably add arguments since the arguments are protected
        extensions = [
            r"~\AppData\Local\Google\Chrome\User Data\Default\Extensions\google_translate.crx",
        ]
        arguments = [
            # * Chrome options can be found here: https://peter.sh/experiments/chromium-command-line-switches/ (China available too)
            # * or here: https://chromium.googlesource.com/chromium/src/+/master/chrome/common/chrome_switches.cc (Don't think this is available in China hahaha)
            # * or here: https://sites.google.com/a/chromium.org/chromedriver/capabilities
            # "--headless", # headless is one of our favorite options

            # The window properties are set by myself using
            "--lang=zh_CN",
            "--window-size="+str(WINDOW_SIZE[0])+","+str(WINDOW_SIZE[1]),
            "--window-position=" + \
            str(WINDOW_POSITION[0])+","+str(WINDOW_POSITION[1]),
            "--disable-infobars",  # this one is supposed to disable the "Chrome is controlled by automated test software. but it doesn't work haha..."
            "--disable-gpu",  # Google recommends using this to avoid unwanted errors
            "--no-sandbox",  # not pretty sure what this one is for

            # When this folder is already in use, be sure not to set it here
            # It crashes
            # Of course you can always try to handle this exception
            # It's called: selenium.common.exceptions.InvalidArgumentException: Message: invalid argument: user data directory is already in use, please specify a unique value for --user-data-dir argument, or don't use --user-data-dir
            # r"--user-data-dir=C:\\Users\\56295\AppData\\Local\\Google\\Chrome\\User Data\Default",
        ]
        for argument in arguments:
            options.add_argument(argument)
        # Add desired extension here
        for extension in extensions:
            options.add_extension(extension)
        # You know, I've tried to use one sentence to do the following which is like options_arguments = ...
        # It works, of course, but it doesn't feel quite right
        # Well, eventually I used the one sentence version
        self.driver = webdriver.Chrome(
            options=options, executable_path=CHROME_DRIVER_PATH, desired_capabilities=capabilities)  # initialize chrome and chrome driver
        self.waiter = WebDriverWait(self.driver, 30)
        try:
            self.driver.get(TRANSLATE_SERVER_URL)
            # waiter.until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, r'#source')))
            self.waiter.until(readyToBeginActions)
            # self.driver.refresh()
            # waiter.until(readyToBeginActions)
            # self.driver.execute_script("window.stop();")
        except exceptions.TimeoutException as e:
            print(
                "Check you internet connection. Or maybe I used the wrong css selector.")
            print(e)

    def __del__(self):
        self.driver.close()

    def translate(self):
        try:
            input_box = self.driver.find_element_by_css_selector(TRANSLATE_INPUTBOX_CSS_SELECTOR)
            input_box.click()
            input_box.clear()
            input_box.send_keys(Keys.CONTROL, "v")
        except BaseException as e:
            print("Something went wrong...")
            print(e)

    def translate_large_content(self, content):
        # length of content is guaranteed to be larger than SLICE_THRESHOLD
        # so the loop will at least be executed once
        slices = []
        length = len(content)
        offset = 0
        while length > SLICE_THRESHOLD:
            length -= SLICE_THRESHOLD
            slices.append(content[offset:offset+SLICE_THRESHOLD])
            offset += SLICE_THRESHOLD
        slices.append(content[offset:-1])
        translated = []
        input_box = self.driver.find_element_by_css_selector(TRANSLATE_INPUTBOX_CSS_SELECTOR)
        input_box.click()
        input_box.clear()
        for slc in slices:
            # input_box.send_keys(slc)
            input_box.clear()
            input_box.send_keys(Keys.CONTROL, "a")
            input_box.send_keys(Keys.BACKSPACE)
            try:
                self.driver.execute_script("document.getElementById('%s').value=%s" % (TRANSLATE_INPUT_ID, repr(slc)))
            except:
                input_box.send_keys('\\\r\n'.join(slc.replace('\'', '\"').split("\r\n")).replace("\\\\", "\\ \\"))
            self.waiter.until(readyToCopiedTranslated)
            output_box = self.driver.find_element_by_class_name(TRANSLATE_OUTPUTBOX_CLASS_NAME)
            translated.append(output_box.text)
            print(translated[-1])
        # print(''.join(translated))


def main():
    chrome = Chrome()
    # last stores what you've got from the clipboard in the last refresh
    last = get_copy_text()
    while True:
        # current content of the clipboard
        current = get_copy_text()
        if current != last:
            try:
                # if the content is too large, you cannot let google translate it all at once
                # TODO: Slice large content into small parts and translate the one by one
                # Make the user notice nothing
                if len(current) > SLICE_THRESHOLD:
                    chrome.translate_large_content(current)
                else:
                    # Using keyboard shortcut Ctrl+V here so no param passing is needed here
                    chrome.translate()
            except BaseException as error:
                print(
                    "\n\nTranslation failed. Have you selected too much content? One step at a time please.", flush=True)
                print(error)
                last = current
                time.sleep(1/REFRESH_RATE)
                continue
        last = current
        # Sleep for 100ms, or you cannot get the correct data from acrobat DC
        # Refresh rate 10Hz
        time.sleep(1/REFRESH_RATE)


def quite_execute(func, global_vars=None, local_vars=None):
    try:
        exec(func, global_vars, local_vars)
    except BaseException as e:
        print(e)
# This get-copy-content function occasionally fails
# Try every step for robustness


def get_copy_text():
    local_vars = {"copy_text": ""}
    copy_text = ""
    # damn it
    # tried to search for a more elegant way to do this but they're all quite confusing
    quite_execute(r"wc.OpenClipboard()")
    quite_execute(r"copy_text = wc.GetClipboardData()", local_vars=local_vars)
    copy_text = local_vars["copy_text"]
    quite_execute(r"wc.CloseClipboard()")
    # wc.OpenClipboard()
    # copy_text = wc.GetClipboardData()
    # wc.CloseClipboard()
    return copy_text


main()
