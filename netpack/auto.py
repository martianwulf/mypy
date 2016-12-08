# originally called myweb
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import InvalidElementStateException as IESE
import time
import re

#caps = DesiredCapabilities.FIREFOX.copy()
#caps['marionette'] = True
#caps['binary'] = 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'

#findFillReg = r'^findAndFill\(\s*([a-zA-Z][a-zA-Z0-9]*)\s*,\s*([a-zA-Z][a-zA-Z0-9]*)\s*\)$'
#findClickReg = r'^findAndClick\(\s*([a-zA-Z][a-zA-Z0-9]*)\s*\)$'

class Finder():
    '''Base class for Finders'''
    def __init__(self, desc):
        self.desc = desc
    def find(self, driver):
        pass

class PageElement():
    '''Base class for all Page Elements'''
    def __init__(self, arg):
        self.arg =  arg
    def execute(self, driver):
        pass
    
class PageElement2():
    '''Base class for all Page Elements'''
    def __init__(self, Finder):
        self.finder = Finder
    def find(self, driver):
        return self.finder.find(driver)
    def execute(self, driver):
        pass

class Findbyid(Finder):
    '''Finds element by id'''
    def find(self, driver):
        if isinstance(driver,webdriver.Firefox):
            return WebDriverWait(driver,10).until(lambda x: x.find_element_by_id(self.desc))

class Findbyname(Finder):
    '''Finds element by id'''
    def find(self, driver):
        if isinstance(driver,webdriver.Firefox):
            return WebDriverWait(driver,10).until(lambda x: x.find_element_by_name(self.desc))

class Findbyclassname(Finder):
    '''Finds elements by class'''
    def find(self, driver):
        if isinstance(driver,webdriver.Firefox):
            return WebDriverWait(driver,10).until(lambda x: x.find_element_by_class_name(self.desc))

class Findbyxpath(Finder):
    '''Finds element by xpath'''
    def find(self, driver):
        if isinstance(driver,webdriver.Firefox):
            return WebDriverWait(driver,10).until(lambda x: x.find_element_by_xpath(self.desc))

class Fillelement(PageElement2):
    def __init__(self, Finder, text):
        super().__init__(Finder)
        self.text = text
    def execute(self, driver):
        elem = self.find(driver)
        if elem is not None:
            elem.clear()
            elem.send_keys(self.text)

class Clickelement(PageElement2):
    def execute(self, driver):
        elem = self.find(driver)
        if elem is not None:
            elem.click()

class PageHandler(PageElement2):
    def __init__(self, Finder, func=None):
        super().__init__(Finder)
        self.func = func
    def execute(self, driver):
        elem = self.find(driver)
        if (elem is not None) and (self.func is not None):
            '''call function to load '''
            actionlist = self.func(driver)
            if actionlist is not None:
                print("actionlist length: {}".format(len(actionlist)))
                for pgelem in actionlist:
                    count = 3
                    while True:
                        try:
                            pgelem.execute(driver)
                            break
                        except IESE as e:
                            print("InvalidElementStateException")
                            if count == 0:
                                break
                            else:
                                count -= 1
                            time.sleep(1)
                            continue
                        except Exception as e:
                            print("{}. {}".format(type(e), e))
                            break
                    #Wait for a second before next page flip
                    time.sleep(1)
            print("Page with id: {} done".format(self.finder.desc))
            return True
        else:
            return False

class FindByName(PageElement):
    '''Finds element by Name'''
    def execute(self, driver):
        if isinstance(driver,webdriver.Firefox):
            return WebDriverWait(driver,10).until(lambda x: x.find_element_by_name(self.arg))
    
class ClickElementId(PageElement):
    def __init__(self, id):
        return super().__init__(id)
    def execute(self, driver):
        el = WebDriverWait(driver,10).until(lambda x: x.find_element_by_id(self.arg))
        if el is not None:
            el.click()
        else:
            logging.debug('Couldn\'t find element with id {}'.format(self.arg))

class ClickElementName(PageElement):
    def __init__(self, name):
        return super().__init__(name)
    def execute(self, driver):
        el = WebDriverWait(driver,10).until(lambda x: x.find_element_by_name(self.arg))
        if el is not None:
            el.click()
        else:
            logging.debug('Couldn\'t find element with id {}'.format(self.arg))

class FillElementId(PageElement):
    def __init__(self, id, value):
        self.value = value
        return super().__init__(id)
    def execute(self, driver):
        el = WebDriverWait(driver,10).until(lambda x: x.find_element_by_id(self.arg))
        if el is not None:
            el.clear()
            el.send_keys(self.value)
            el = None
        else:
            logging.debug('Couldn\'t find element with id {}'.format(self.arg))

class FillElementName(PageElement):
    def __init__(self, name, value):
        self.value = value
        #return super().__init__(name)
    def execute(self, driver):
        el = WebDriverWait(driver,10).until(lambda x: x.find_element_by_name(self.arg))
        if el is not None:
            el.clear()
            el.send_keys(self.value)
            el = None
        else:
            logging.debug('Couldn\'t find element with id {}'.format(self.arg))

class SelectElement(PageElement):
    def __init__(self, id, value):
        self.value = value
        return super().__init__(id)
    def execute(self, driver):
        sel = Select(WebDriverWait(driver,10).until(lambda x: x.find_element_by_id(self.arg)))
        if sel is not None:
            sel.select_by_value(self.value)
        else:
            logging.debug('Couldn\'t find element with id {}'.format(self.arg))

class ActionSeq():
    '''Class containing a list of '''
    def __init__(self):
        self.elemseq = []
    def addElem(self, elem):
        self.elemseq.append(elem)
    def run(self, driver):
        for item in self.elemseq:
            try:
                item.execute(driver)
            except Exception as e:
                print('{} in ActionSeq class'.format(e))

class Browser():
    '''A class for opening and controlling a browser'''
    def __init__(self, outfile=None):
        self.outfile = outfile
        self.actionseq = []
        self.databus = {}
    def addActionSeq(self, ActionSeq):
        self.actionseq.append(ActionSeq)
        #ActionSeq.setdriver(self.driver)
    def work(self):
        if len(self.actionseq) <1:
            print('No actionseq')
            return
        for pg in self.actionseq:
            pg.run(self.driver)

def automate(driver, ActionSeq):
    '''Iterates through and executes the execute method of the PageElements in a ActionSeq object'''
    if len(ActionSeq.elemseq) < 1:
        print('No actionseq')
        return
    #for action in ActionSeq.elemseq:
    #    action.execute(driver)
    ActionSeq.run(driver)

