# import necessary libraries
from selenium.webdriver import Chrome, ChromeOptions
import requests
from win10toast import ToastNotifier


# -------------------------------------------------------------------------

USERNAME = ''
PASSWORD = ''
NOTIFICATION_ICON_PATH = ''

# -------------------------------------------------------------------------


def notify(message):
    n = ToastNotifier()
    n.show_toast("Netaccess Authorisation Alert", message, duration = 5,
        icon_path=NOTIFICATION_ICON_PATH)


class AutoLogin:
    def __init__(self):
        self.url = "https://netaccess.iitm.ac.in/account/login"
        self.USR_NAME = USERNAME
        self.USR_PWD = PASSWORD

    def login(self):
        # notify commencement of login
        notify("Initiating Netaccess authorisation...")

        # options to run browser as headless
        options = ChromeOptions()
        options.add_argument("--headless")

        # driver instantiation
        driver = Chrome(options=options)
        driver.get(url=self.url)

        # initial netaccess login
        driver.find_element_by_id("username").send_keys(self.USR_NAME)
        driver.find_element_by_id("password").send_keys(self.USR_PWD)
        driver.find_element_by_id("submit").click()

        # approve button click
        driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/a/span").click()

        # setting up for 1 day use
        driver.find_element_by_id("radios-1").click()
        driver.find_element_by_id('approveBtn').click()

        # get IP
        IP = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/strong").text

        # get no of devices
        count = 0
        data = driver.find_element_by_tag_name('table')
        data = data.find_element_by_tag_name('tbody')
        for row in data.find_elements_by_tag_name('tr'):
            cols = row.find_elements_by_tag_name('td')
            if len(cols) == 6:
                if cols[4].text.strip() == 'Active':
                    count += 1
                else:
                    break
            else:
                pass

        # driver close
        driver.close()

        # notify
        notify(f"Netaccess authorisation Successful\nRegistered IP : {IP}\nNumber of devices : {count}")

        # exit program
        quit(0)

    def run(self):
        try:
            response = requests.get(self.url)
            if response.ok:
                self.login()
            else:
                notify("Unable to connect to Netaccess, manual authorisation is recommended")
                quit(0)
        except Exception as e:
            print(e)
            notify("Unable to connect to Netaccess, manual authorisation is recommended")
            quit(0)


def main():
    login_obj = AutoLogin()
    login_obj.run()


if __name__ == "__main__":
    main()
