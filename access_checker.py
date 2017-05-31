#!/usr/bin/env python3.6

import sys
import selenium.webdriver
import getpass
from selenium.webdriver.common.keys import Keys
import time
import paramiko
from terminaltables import AsciiTable
from colorama import Fore, Back, Style


bad_result = "☠"
good_result = "🍻"
test_evidence = {"Wendy": "☠", "Wendy2": "☠", "MAchine1": "☠"}

# username = input("Please enter your username:")
print ("Please enter you AD password")
adPassword = getpass.getpass()

print ("Please enter you onshore LDAP password")
onshorePassword = getpass.getpass()

print ("Please enter you offshore LDAP password")
offshorePassword = getpass.getpass()

test_data = [
    ['Test name', 'Status', 'Type of test', 'URI', 'username', "password_type", "username_id", "password_name", "validation_id", "button_class"],
    ['Wendy', "☠", "http", "https://e-kartoteka.pl/#/login", "d4721@domkrak", "AD", "username", "passwd","wlaczWskazowki", "button.k-button.btn-block"]#,
    # ['Wendy2', "☠"],
    # ['Access to a server', "☠"]
]



# options = {"url": "https://e-kartoteka.pl/#/login",
# "username": "",
#            "password": "",
#            "username_id": "username",
#            "password_name": "passwd",
#            "button_class": "button.k-button.btn-block",
#            "validation_id": "wlaczWskazowki",
#            "test_name": "Wendy"}

def checkAccessToMachine(options):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(options['hostname'], username=options['user'], password=options['password'])
    # print("could connect")
    stdin, stdout, stderr = ssh.exec_command('sudo -i -H -- echo $USER ; echo $USER')
    if options['user'] in stdout.readline():
        ssh.close()
        return good_result
    else:
        ssh.close()
        return bad_result


def checkByValidationId(driver, options):
    try:
        driver.find_element_by_id(options["validation_id"])
        driver.save_screenshot("good.png")
        driver.quit()
        return good_result
    except selenium.common.exceptions.NoSuchElementException:
        driver.save_screenshot("bad.png")
        driver.quit()
        return bad_result


def checkAccessToWebsite(options):
    driver = selenium.webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get(options["url"])
    # logout if needed
    # try:
    # driver.find_element_by_css_selector("span.glyphicon.glyphicon-off").click()
    # except selenium.common.exceptions.NoSuchElementException:
    # print ("Exception caught")
    driver.find_element_by_id(options["username_id"]).send_keys(options["username"])
    time.sleep(1)
    driver.find_element_by_name(options["password_name"]).send_keys(options["password"])
    time.sleep(1)
    driver.find_element_by_css_selector(options["button_class"]).click()
    time.sleep(1)
    driver.maximize_window()
    return checkByValidationId(driver, options)


for list in test_data:
    if list[0] == 'Test name':
        continue

    if list[5] == 'AD':
        password = adPassword
    elif list[5] == 'onshore':
        password = onshorePassword
    else:
        password = offshorePassword

    if list[2] == 'http':
        list[1] = checkAccessToWebsite({"url": list[3],
                                        "username": list[4],
                                        "password": password,
                                        "username_id": list[7],
                                        "password_name": list[7],
                                        "button_class": list[9],
                                        "validation_id": list[8]})
    elif list[2] == 'ssh':
        checkAccessToMachine({"user": "", "password": "", "hostname": "", "test_name": "MAchine1"})

# options = {"url": "https://e-kartoteka.pl/#/login",
#            "username": "",
#            "password": "",
#            "username_id": "username",
#            "password_name": "passwd",
#            "button_class": "button.k-button.btn-block",
#            "validation_id": "wlaczWskazowki",
#            "test_name": "Wendy"}
#
# # test_evidence[options['test_name']] = checkAccessToWebsite(options)
#
# options2 = {"url": "https://e-kartoteka.pl/#/login",
#             "username": "",
#             "password": "",
#             "username_id": "username",
#             "password_name": "passwd",
#             "button_class": "button.k-button.btn-block",
#             "validation_id": "wlaczWskazowki",
#             "test_name": "Wendy2"}
#
# # test_evidence[options2['test_name']] = checkAccessToWebsite(options2)
#
# print (test_evidence)
#
# optionsHost = {"user": "", "password": "", "hostname": "", "test_name": "MAchine1"}
#
# test_evidence[optionsHost['test_name']] = checkAccessToMachine(optionsHost)
# print (test_evidence)
#
# table_data = [
#     ['Test', 'Status'],
#     ['Wendy', test_evidence['Wendy']],
#     ['Wendy2', test_evidence['Wendy']],
#     ['Access to a server', test_evidence['MAchine1']]
# ]
print(Fore.GREEN + '------========================SUMMARY========================------')
table = AsciiTable(test_data)
print (Fore.RED + table.table)
# print (checkAccessToMachine(optionsHost))

# options = {"url": "https://e-kartoteka.pl/#/login",
# "username": "",
# "password": "",
#            "username_id": "username",
#            "password_name": "passwd",
#            "button_class": "button.k-button.btn-block",
#            "validation_id": "wlaczWskazowki",
#            "test_name":"Wendy"}


# def checkJenkins():
# try:
# elem = driver.find_element_by_partial_link_text("log out")
#         return elem.text
#     except selenium.common.exceptions.NoSuchElementException:
#         print ("You are not logged in to Wendy, let me try to login you")


# checkJenkins()

# username = input("Please enter your username:")
# print ("Please enter you onshore LDAP password")
# onShorePassword = getpass.getpass()

# driver.find_element_by_id("j_username").send_keys(username)
# driver.find_element_by_name("j_password").send_keys(onShorePassword)
# driver.find_element_by_id("yui-gen1-button").click()

# if checkJenkins() == "log out":
#     print ("You can connect to Wendy")
# else:
#     print ("Connection to Wendy was not established")
# print ("Please enter you AD password")

# driver.quit()

# driver = selenium.webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])

# adPassword = getpass.getpass()


# def checkSplunkConnection(urlToSplunk):
#     urlToSplunk=f"https://{urlToSplunk}/en-US/account/login?return_to=%2Fen-US%2F"
#     print (f"URL to Splunk is {urlToSplunk}")
#     driver.get(urlToSplunk)
#     driver.find_element_by_id("username").send_keys(username)
#     pp = driver.find_element_by_id("password")
#     pp.send_keys(adPassword)
#     pp.send_keys(Keys.RETURN)
#     driver.save_screenshot("test.png")
#     try:
#         print (driver.find_element_by_class_name("app-name"))
#         driver.save_screenshot("test1.png")
#         print (f"You have connection to {urlToSplunk}")
#     except selenium.common.exceptions.NoSuchElementException:
#         print (f"You do not have connection to {urlToSplunk}")


# checkSplunkConnection("clp.cxp.williamhill.plc")
# checkSplunkConnection("clp.pp2.williamhill.plc")
# checkSplunkConnection("clp.prod.williamhill.plc")

# driver.quit()