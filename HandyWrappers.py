from selenium.webdriver.common.by import By

class HandyWrappers:

    def __init__(self, driver):
        self.driver = driver

    def getByType(self, LocatorType):
        LocatorType = LocatorType.lower()
        if LocatorType == 'id':
            return By.ID
        elif LocatorType == 'name':
            return By.NAME
        elif LocatorType == 'xpath':
            return By.XPATH
        elif LocatorType == 'classname':
            return By.CLASS_NAME
        elif LocatorType == 'css':
            return By.CSS_SELECTOR
        elif LocatorType == 'linktext':
            return By.LINK_TEXT
        elif LocatorType == 'tagname':
            return By.TAG_NAME
        else:
            print("Locator Type" + LocatorType + "not Correct or Supported")
        return False

    def GetElement(self, Locator, LocatorType='id'):
        element = None
        try:
            LocatorType = LocatorType.lower()
            ByType = self.getByType(LocatorType)
            element = self.driver.find_element(ByType, Locator)
            return element
        except:
            return element

    def GetElements(self, Locator, LocatorType='id'):
        Elements = []
        try:
            LocatorType = LocatorType.lower()
            ByType = self.getByType(LocatorType)
            Elements = self.driver.find_elements(ByType, Locator)
            if Elements not in [None, False]:
                print("Elements found")
                pass
            else:
                print("Elements list empty!")
                pass
        except:
            print("Elements Error!")
        return Elements

    def ClickElement(self, Locator, LocatorType='id'):
        try:
            Get_Element = self.GetElement(Locator, LocatorType)
            if Get_Element is not None or False:
                Get_Element.click()
                print('Element Clicked')
            else:
                pass
        except:
            pass

    def GetElementText(self, Locator, LocatorType='id'):
        Element_text = ''
        try:
            Get_Element = self.GetElement(Locator, LocatorType)
            if Get_Element is not None or False:
                Element_text = Get_Element.text
                # print('Element Text: ' + Element_text)
            else:
                print("Element does not have any text")
        except:
            print('Element Error!')
        return Element_text

    def GetElementlistofText(self, Locator, LocatorType='id'):
        list_of_Text = []
        try:
            ElementlistofText = self.GetElements(Locator, LocatorType)
            for elements in ElementlistofText:
                if elements not in [None, False]:
                    text_elements = elements.text
                    list_of_Text.append(text_elements)
                else:
                    print("Element list not exist!")
            # print(list_of_Text)
        except:
            print('Element error!')
        return list_of_Text

    def GetElementAttribute(self, Locator, LocatorType='id', attribute='class'):
        attribute_value = None
        try:
            Element = self.GetElement(Locator, LocatorType)
            if Element not in [None, False]:
                attribute_value = Element.get_attribute(attribute)
                # print("Value of attribute is: " + attribute_value)
            else:
                print("Value of attribute does not exist")
        except:
            print('Value of attribute has error')
        return attribute_value

    def GetElementlistofattribute(self, Locator, LocatorType='id', attribute='class'):
        list_of_attribute = []
        try:
            elements = self.GetElements(Locator, LocatorType)
            for element in elements:
                if element not in [None, False]:
                    attribute_value = element.get_attribute(attribute)
                    list_of_attribute.append(attribute_value)
                else:
                    print('list of attribute value is empty')
            # print(list_of_attribute)
        except:
            print('list of attribute value error')
        return list_of_attribute

    def isElementPresent(self, Locator, LocatorType='id'):
        try:
            element = self.GetElement(Locator, LocatorType)
            if element is not None:
                return True
            else:
                return False
        except:
            return False