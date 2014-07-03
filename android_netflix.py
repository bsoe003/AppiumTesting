import os
import unittest
from appium import webdriver
from selenium.webdriver.common.by import By
import time
import constants
from operator import eq

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class SampleNetflixTest(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = constants.platform
        desired_caps['platformVersion'] = constants.version
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['app'] = PATH(constants.apk)
        desired_caps['appPackage'] = constants.package
        desired_caps['appActivity'] = constants.activity
        #desired_caps['appWaitPackage'] = constants.package
        #desired_caps['appWaitActivity'] = '.UIWebViewActivity'

        self.driver = webdriver.Remote(constants.host, desired_caps)
        self.driver.implicitly_wait(30)
        
    def tearDown(self):
        self.driver.close_app()
        self.driver.quit()

    def options(self,choice):
        option = -1
        if(eq(choice,"Settings")):
            option = 0
        elif(eq(choice,"Sign Out")):
            option = 1
        else:
            return False
        self.driver.find_elements_by_class_name("android.widget.ImageButton")[0].click()
        self.driver.find_elements_by_class_name("android.widget.LinearLayout")[option].click()
        return True

    "Testing Login Page of Netflix"
    def test_login(self): 
        """ Testing Login with ViaSat Credentials """
		
        """ Looking for "Sign In" of application.
		    If found click
            Else keep searching then exit if necessary"""
        while(not eq(self.driver.current_activity,".ui.signup.SignupActivity")):
	        time.sleep(0.5)
	        continue

        textview = self.driver.find_elements_by_class_name("android.widget.TextView")
        self.driver.implicitly_wait(30)
        textview[0].click()
        self.driver.implicitly_wait(30) # wait for sign-in page to load
		
        """ Login with ViaSat credentials """
        textfield = self.driver.find_elements_by_class_name("android.widget.EditText")
        username = raw_input("\n\nUsername: ")
        if eq(username,""):
	        username = constants.username
        textfield[0].send_keys(username)
        password = raw_input("Password: ")
        if eq(password,""):
	        password = constants.password
        textfield[1].send_keys(password)
        self.driver.find_elements_by_class_name("android.widget.Button")[0].click()
        print "Signing In"
        
        while(not eq(self.driver.current_activity,".ui.profiles.ProfileSelectionActivity")):
	        time.sleep(0.5)
	        continue

        name = raw_input("\nPlease type name of your desired profile: ")
        while(True):
            try:
                print "Checking if input is invalid ..."
                profile = self.driver.find_element_by_android_uiautomator('new UiSelector().description("'+name+'")')
                profile.click()
                break;
            except Exception:
                name = raw_input("Not an exisitng user, please again: ")
        

        while(not eq(self.driver.current_activity,".ui.home.HomeActivity")):
	        time.sleep(0.5)
	        continue

        self.driver.implicitly_wait(30)
        self.driver.find_elements_by_class_name("android.widget.Button")[0].click()
        self.driver.implicitly_wait(30)

        choice = raw_input("What do you want to do?")
        valid = self.options(choice)
        while(not valid):
            choice = raw_input("Invalid option, try again:")
            valid = self.options(choice)
        
        self.driver.find_elements_by_class_name("android.widget.Button")[1].click()
        self.driver.implicitly_wait(30)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SampleNetflixTest)
    unittest.TextTestRunner(verbosity=2).run(suite)