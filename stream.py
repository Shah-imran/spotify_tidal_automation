from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from threading import Thread
import time
import string, random, zipfile
import var
import db


class bot():
    def __init__(self, ip, id):
        self.id = id
        PROXY_HOST = ip
        PROXY_PORT = var.proxy_port
        PROXY_USER = var.proxy_user
        PROXY_PASS = var.proxy_pass
        print(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%(host)s",
                    port: parseInt(%(port)d)
                },
                bypassList: ["foobar.com"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%(user)s",
                    password: "%(pass)s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % {
            "host": PROXY_HOST,
            "port": PROXY_PORT,
            "user": PROXY_USER,
            "pass": PROXY_PASS,
        }

        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        co = Options()
        co.add_argument("--start-maximized")
        co.add_extension(pluginfile)

        self.timeOut = 30
        self.spotify_link = "https://accounts.spotify.com/en/login/"
        self.tidal_link = "https://listen.tidal.com/login"
        self.test_link = "http://lumtest.com/myip.json"

        # ----- without image ----- (uncomment this)
        prefs = {"profile.managed_default_content_settings.images": 2}
        co.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=co)

        self.driver.get(self.test_link)
        Thread(target=self.stop,daemon=True).start()
        Thread(target=self.stop_all,daemon=True).start()
        WebDriverWait(self.driver, self.timeOut).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
        
        self.driver.maximize_window()

    def login_spotify(self, email, password):
        count = 0
        while count<10:
            try:
                count+=1
                self.driver.get(self.spotify_link)

                WebDriverWait(self.driver, self.timeOut).until(EC.visibility_of_element_located((By.ID, "login-username"))) 

                self.driver.find_element_by_id("login-username").send_keys(email + Keys.TAB + password + Keys.ENTER)

                WebDriverWait(self.driver, self.timeOut).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
                time.sleep(10)
                break
            except:
                continue

    def stream_spotify(self, link, id):
        try:
            self.driver.get(link)
            time.sleep(var.time_duration+5)

            conn = db.db_ceate()
            conn.update_count(id)
            conn.close()
        except Exception as e:
            print("Exeception occured at stream {} :{} ".format(self.id, e))

    def login_tidal(self, email, password):
        count = 0
        while count<10:
            try:
                count+=1
                self.driver.get(self.tidal_link)
                WebDriverWait(self.driver, self.timeOut).until(EC.visibility_of_element_located((By.CLASS_NAME, "login-facebook")))
                self.driver.find_element_by_class_name("login-facebook").click()
                
                WebDriverWait(self.driver, self.timeOut).until(EC.visibility_of_element_located((By.ID, "email")))
                self.driver.find_element_by_id("email").send_keys(email + Keys.TAB + password + Keys.ENTER)
                WebDriverWait(self.driver, self.timeOut).until(EC.visibility_of_element_located((By.TAG_NAME, "body"))) 

                time.sleep(10)
                break
            except:
                continue
    def stream_tidal(self, link, id):
        try:
            self.driver.get(link)
            xpath = "/html/body/div[2]/div/div/div/div[1]/div[2]/main/div[1]/div[2]/div/div[1]/span/div/header/div[2]/div[2]/button[1]"
            WebDriverWait(self.driver, self.timeOut).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            self.driver.find_element_by_xpath(xpath).click()
            time.sleep(2)
            time.sleep(var.time_duration+5)

            conn = db.db_ceate()
            conn.update_count(id)
            conn.close()
        except Exception as e:
            print("Exeception occured at stream {} :{} ".format(self.id, e))

    def stop(self):
        while True:
            time.sleep(1)
            if var.stop == True and self.id in var.stop_list:
                try:
                    print("Stop - {}".format(self.id))
                    self.driver.quit()
                except Exception as e:
                    print("Exeception occured at stop :{}".format(e))
                finally:
                    break

    def stop_all(self):
        while True:
            time.sleep(1)
            if var.stop_all == True:
                try:
                    print("Stop All - {}".format(self.id))
                    self.driver.quit()
                except Exception as e:
                    print("Exeception occured at stop all :{}".format(e))
                finally:
                    break
                

def main(id, username, password, playlist, proxy_ip, site):
    stream = bot(proxy_ip, id)
    conn = db.db_ceate()
    songs = conn.get_playlist(playlist)
    conn.close()
    if site == "spotify":
        stream.login_spotify(username, password)
        while True:
            try:
                print("big loop {}".format(id))
                for item in songs:
                    print("lil loop {}".format(id))
                    if (var.stop_all == True) or (var.stop == True and id in var.stop_list):
                        break
                    else:
                        print(id, username, proxy_ip, item[2])
                        stream.stream_spotify(item[2], item[0])
                if (var.stop_all == True) or (var.stop == True and id in var.stop_list):
                    break
                time.sleep(1)
            except Exception as e:
                print("Exeception occured at stream loop :{}".format(e))
                break
    else:
        stream.login_tidal(username, password)
        while True:
            try:
                print("big loop {}".format(id))
                for item in songs:
                    print("lil loop {}".format(id))
                    if (var.stop_all == True) or (var.stop == True and id in var.stop_list):
                        break
                    else:
                        print(id, username, proxy_ip, item[2])
                        stream.stream_tidal(item[2], item[0])
                if (var.stop_all == True) or (var.stop == True and id in var.stop_list):
                    break
                time.sleep(1)
            except Exception as e:
                print("Exeception occured at stream loop :{}".format(e))
                break
    print("Exiting {}".format(id))

if __name__ == "__main__":
    # temp = bot()
    # temp.login_spotify("nathan.johnson@billionaireminded.com", "WillieB1@1")
    pass