"""Pywinauto wrapper file contains all the pywinauto functions for UI and Functional use of AMD Installer"""
import time

import pyautogui
import pywinauto
import psutil
import logging
import winapps
import json
import win32api
import webbrowser
import warnings
import os
import shutil
from time import sleep
from pywinauto.application import Application
from pywinauto.findwindows import WindowNotFoundError
from pywinauto.keyboard import send_keys
from pywinauto import mouse, keyboard
from configparser import ConfigParser
from config import UI_elements
from library import application_info
from Core.Subprocess_wrapper import run_cmd_call
from win32api import GetSystemMetrics

warnings.filterwarnings('ignore')


conf = ConfigParser()
conf.read("../../config/config.ini")


def get_sdk_version_detail():
    """
    This api will fetch the ROCm version from the Install manifest json file
    :return:
    """
    f = open(conf['Installer Path']['json'])
    data = json.load(f)
    try:
        for i in data['Packages']:
            for k in data['Packages'][i]:
                if k['Info']['Description'] == "HIP SDK Core for Windows":
                    sdk = k['Info']['version']
                    sdk_version = sdk.replace(".0", "")
                    return sdk_version
    except Exception as e:
        logging.error("Failed to get SDK version from Install manifest file")
        logging.exception(e)


def get_driver_version_detail():
    """
    This api will fetch the Driver version from the Install manifest json file
    :return:
    """
    f = open(conf['Installer Path']['json'])
    data = json.load(f)
    try:
        for k in data['Packages']['Package']:
            if 'DriverVersion' in k["Info"]:
                driver_version2 = (k['Info']['DriverVersion'])

        driver_version = data['BuildInfo']['RadeonSoftwareVersion']
        version = driver_version + " , " + driver_version2
        return version
    except Exception as e:
        logging.error("Failed to get Driver version from Install manifest file")
        logging.exception(e)


# function will check if Installer already running or not. ( will run fresh setup )
def launch_installer():
    """
    This api will launch the Installer Application, and will close already running application and will return the
    location where components are getting installed
    :return : path
    """
    if previous_running_check():
        kill_process()
        logging.debug("previous APP killed")

    try:
        kill_vs_process()
        Application(backend='uia').start(cmd_line=conf['Installer Path']['setup'], timeout=UI_elements.launch_timeout)

        global second_exe_installer
        second_exe_installer = Application(backend='uia').connect(path=conf['Installer Path']['AMDSoftwareInstaller'],
                                                                  timeout=UI_elements.launch_timeout)
        second_exe_installer.Dialog.child_window(title=UI_elements.Install, control_type="Button").wait(
            'ready', timeout=UI_elements.launch_timeout).verify_visible()
        logging.debug("Successfully launched the application. Launch Completed - launch_updated()")
        second_exe_installer.Dialog.set_focus()
        path = get_component_installation_path()
        return path

    except Exception as e:
        logging.exception(e)
        logging.error("Something wrong in UI launch. Install button is not visible \n ")


def re_launch_installer():
    """
    This api will re-launch the Installer Application while the previous installer is still running and will handle
    the error popup message
    :return: bool
    """
    ok_button_timeout = 5
    Application(backend='uia').start(cmd_line=conf['Installer Path']['setup'], timeout=UI_elements.launch_timeout)
    try:
        kill_vs_process()
        Application(backend='uia').connect(
            path=conf['Installer Path']['AMDSoftwareInstaller'], timeout=UI_elements.launch_timeout)
        try:
            app = Application(backend='uia').connect(
                path=conf['Installer Path']['AMDSoftwareInstaller'], timeout=UI_elements.launch_timeout)
            logging.debug("Re launched the Installer , Waiting for the Error to pop-up. re_launch_installer()")

            app.Dialog.child_window(title="OK", control_type="Button").wait('ready',
                                                                            timeout=ok_button_timeout).verify_visible()
            app.Dialog.child_window(title="OK", control_type="Button").wait('ready', timeout=ok_button_timeout).click()
            logging.warning("warning Pop-up appeared preventing re-launch of another instance. Clicked on OK button")
            return True

        except Exception as e:
            logging.error("Failed to Click on OK button on the Pop-up appeared.\n")
            logging.exception(e)

    except Exception as e:
        logging.error("Failed to attempt to re-Launch application. re_launch_installer")
        logging.exception(e)
        return False


def double_click_launch():
    """
    This api is to launch the installer by double clicking the setup file ( TC )
    :return: bool
    """
    try:
        kill_vs_process()
        Application().start(f"explorer.exe {conf['Installer Path']['hip_sdk_setup']}")
        app = Application(backend="uia").connect(path="explorer.exe", timeout=UI_elements.launch_timeout)
        app.HIP_SDK_Setup.set_focus()
        common_files = app.HIP_SDK_Setup.ItemsView.get_item('Setup.exe')
        common_files.click_input()
        x, y = win32api.GetCursorPos()
        mouse.double_click(button='left', coords=(x, y))
        logging.debug("Double clicked on the setup.exe. Connecting to AMD installer window")
        second_exe_installer = Application(backend='uia').connect(path=conf['Installer Path']['AMDSoftwareInstaller'],
                                                                  timeout=UI_elements.launch_timeout)
        second_exe_installer.Dialog.child_window(title=UI_elements.Install, control_type="Button").wait(
            'ready', timeout=UI_elements.launch_timeout).verify_visible()
        logging.debug("Connection to AMD installer window has been completed")

        return True
    except FileNotFoundError as e:
        logging.exception(e)
        logging.error("There is no file name as Setup. File path not found")
    except Exception as ee:
        logging.exception(ee)


# Function to bring the application to front
def bring_to_front():
    """
    This api will bring the connected app to front
    """
    try:
        # Access app's window object
        app_dialog = second_exe_installer.top_window()
        app_dialog.minimize()
        app_dialog.restore()
        app_dialog.set_focus()

    except WindowNotFoundError:
        logging.exception("Something wrong with Installer bringing to front, Please check")
    except Exception as e:
        logging.error(e)
        logging.exception("Something wrong with Installer bringing to front, Please check")


# will close the already running installer
def kill_process():
    """
    Will kill the already running  AMD SDK installer application
    """
    process_name = conf['SDK Process']['Installer_Process']
    pid = None
    for proc in psutil.process_iter():
        if process_name in proc.name():
            pid = proc.pid
    p = psutil.Process(pid)
    p.terminate()  # or p.kill()
    logging.warning('pid {} : process has been terminated. Previous running '
                    'Application HIP SDK Installer has been closed'.format(pid))
    sleep(0.5)  # Time required to kill all processes


def kill_vs_process():
    """
    Will kill the already running VS application
    :return:
    """
    try:
        process_name2 = conf['SDK Process']['Visual_studio_process']
        pid = None
        for proc in psutil.process_iter():
            if process_name2 in proc.name():
                pid = proc.pid
                p = psutil.Process(pid)
                p.terminate()  # or p.kill()
        logging.debug(f'pid {pid} : process has been terminated. '
                      f'Visual Studio has been closed has been closed')
        time.sleep(2)  # Time required to kill all processes
    except Exception as e:
        logging.error("Failed to kill Visual Studio processes")
        logging.exception(e)


def validate_application_running():
    """
    Will check if AMD SDK installer application is still running or not
    :return:
    """
    process_name = conf['SDK Process']['Installer_Process']
    sleep(1)  # Time required to iterate all process and find the required process
    pid = None
    for proc in psutil.process_iter():
        if process_name in proc.name():
            name = proc.name
            logging.warning(f"Running Process Found {name}")
            pid = proc.pid

    psutil.Process(pid)
    if pid is None:
        logging.info(" Installer App is not running.")
        return True
    else:
        logging.error(f"process is still running {process_name}.")


def previous_running_check():
    """
    This api will check if Installer is still running
    :return: bool
    """
    process_name = conf['SDK Process']['Installer_Process']
    pid = None
    for proc in psutil.process_iter():
        if process_name in proc.name():
            pid = proc.pid
    psutil.Process(pid)
    if pid is None:
        logging.debug("No Previous running app found")
    else:
        logging.warning(f"process is still running {process_name}.")
        return True


# Function to click any element by passing argument
def element_click(title, control_type=UI_elements.button, timeout=UI_elements.click_timeout):
    """
    This api will click on the element of the provided arguments
    :param title: Title of the UI element
    :param control_type: type of UI element ( button/combobox/list )
    :param timeout: Max time to Click on element
    :return: bool
    """
    try:
        second_exe_installer.Dialog.child_window(title=title,
                                                 control_type=control_type).wait('ready', timeout=timeout).click()
        return True
    except Exception as e:
        logging.error(f"Failed to Click on the element : {title}")
        logging.exception(e)
        return False


# Function to click any element by passing argument
def element_click_input(title, control_type=UI_elements.button, timeout=UI_elements.click_timeout):
    """
    This api will click on the element of the provided arguments and move the pointer
    :param title: Title of the UI element
    :param control_type: type of UI element ( button/combobox/list )
    :param timeout: Max time to Click on element
    :return: bool
    """
    try:
        second_exe_installer.Dialog.child_window(title=title,
                                                 control_type=control_type).wait('ready', timeout=timeout).click_input()
        return True
    except Exception as e:
        logging.error(f"Failed to Click on the element : {title}")
        logging.exception(e)
        return False


# Function to expand combo box by passing argument
def combo_box_expand(title, control_type=UI_elements.combo_box, timeout=UI_elements.click_timeout):
    """
    This api will expand the combo box
    :param title: Title of the UI element
    :param control_type: type of UI element , combobox
    :param timeout: Max time to Click on element
    :return: bool
    """
    try:
        second_exe_installer.Dialog.child_window(title=title,
                                                 control_type=control_type).wait('ready', timeout=timeout).expand()
        return True
    except Exception as e:
        logging.error(f"Failed to Click on the ComboBox element : {title}")
        logging.exception(e)
        return False


# Scroll functionality
def scroll(value):
    """
    This api will bring the pointer to center of screen where installer screne is present.
    will bring the installer screen to front, and will scroll down
    :param value: X is value passed to scroll down. ( Minimum value for scroll down is -100 for pyautogui framework
    :return:
    """
    try:
        second_exe_installer.Dialog.set_focus()
        bring_to_front()
        # screen_width = GetSystemMetrics(0)
        # screen_height = GetSystemMetrics(1)
        if second_exe_installer.Dialog.child_window(title=UI_elements.Install, control_type="Button"). \
                wait('ready', timeout=UI_elements.click_timeout):
            # pyautogui.moveTo(screen_width / 2, screen_height / 2, duration=0.15)
            # second_exe_installer.Dialog.AMDHIPSDKInstaller.click_input()
            second_exe_installer.Dialog.ScrollBar.click_input()
            # x, y = win32api.GetCursorPos()
            # pywinauto.mouse.scroll(coords=(x, y), wheel_dist=10)
            pyautogui.scroll(value)
    except Exception as e:
        logging.error("scroll() failed")
        logging.exception(e)


def drag_dialog():
    """
    This api is will drag the AMD HIP SDK Installer to left of screen and will bring back
    :return:
    """
    try:
        second_exe_installer.Dialog.AMDHIPSDKInstaller.click_input()
        x, y = win32api.GetCursorPos()
        mouse.press(button='left', coords=(x, y))
        time.sleep(0.5)  # Wait time required to move the mouse
        mouse.release(button='left', coords=(0, 0))
        mouse.press(button='left', coords=(0, 0))
        mouse.release(button='left', coords=(x, y))
        return True
    except Exception as e:
        logging.error("Failed to Drag the dialog - drag_dialog()")


def click_browse():
    """
    This api will click on the browse buttons present on the AMD Installer
    :return:
    """
    try:
        browse = second_exe_installer.dialog.child_window(title=UI_elements.browse,
                                                          control_type=UI_elements.button). \
            wait('ready', timeout=UI_elements.click_timeout)
        time.sleep(2)  # Wait time to open Browse
        browse.click_input()
    except Exception as e:
        logging.error("Failed to click on browse button")


def change_browse_path():
    """
    This api is used to change the browse path and give some other correct path
    :return:
    """
    try:
        click_browse()
        send_keys('^l')
        send_keys('C:\Program Files', with_spaces=True)  # Giving new path
        send_keys('{ENTER}')
        time.sleep(2)  # Wait time to for changing path
        second_exe_installer.Dialog.SelectFolder.click_input()
        return True
    except Exception as e:
        logging.error(e)


def change_incorrect_browse_path():
    """
    This api will change the browse path and give some incorrect path and will deal with the error popup (TC)
    :return: bool
    """
    try:
        click_browse()
        send_keys('^l')
        send_keys('C:\incorrectpath', with_spaces=True)  # Giving new path
        send_keys('{ENTER}')
        time.sleep(2)  # Wait time to for changing path
        second_exe_installer.Dialog.OkButton.click_input()
        second_exe_installer.Dialog.Cancel.click_input()
        return True
    except Exception as e:
        logging.exception(e)


# # Fetch and verify the UI element property of button
def get_prop_button(true_button):
    """
    This api will give the property of the UI element
    :param true_button: Button name
    :return: bool
    """
    try:
        second_exe_installer.Dialog.child_window(title=true_button, control_type="Button").wait(
            'ready', timeout=3).verify_visible()
        abc = second_exe_installer.Dialog.child_window(title=true_button, control_type="Button").wait(
            'ready', timeout=1).get_properties()

        logging.debug(f"Name of: {true_button} : verified successfully as per records.")
        return True

    except Exception:
        logging.debug(f"Element {true_button} not found , scrolling down once to check."
                      "raising exception for the default option.")


# Fetch the UI element property of Combo Box
def get_prop_combo_box(true_combo):
    """
        This api will give the property of the UI element, combobox
    :param true_combo: Combobox name
    :return: bool
    """
    try:
        second_exe_installer.Dialog.child_window(title=true_combo, control_type="ComboBox").wait(
            'ready', timeout=3).verify_visible()
        logging.debug(f"Name of : {true_combo} :verified successfully as per records.")
        return True

    except Exception:
        logging.debug(f"Element {true_combo} not found , scrolling down once to check."
                      "raising exception for the default option.")


def verify_click(element):
    """
    This api will check if the click to the provided element is success or not. Name of the element should change
    :param element: element which was clicked ( passed from UI_elements.py)
    """
    try:
        second_exe_installer.Dialog.child_window(title=element, control_type="Button").wait(
            'ready', timeout=0.2).verify_visible()
        logging.warning(f"Verify_click() -  {element} element is still visible")
        return True

    except Exception:
        logging.debug(f"Click on {element} has been verified Successfully. verify_visible()")
        return False


def verify_visible(element):
    """
    This api is an extension to verify_visible of pywinauto to use it in other scripts without import
    :param element: Element ID to be passed from UI_elements.py
    """
    try:
        second_exe_installer.Dialog.child_window(title=element, control_type="Button").wait(
            'ready', timeout=0.2).verify_visible()
        logging.debug(f"{element} is visible. verify_visible()")
        return True

    except Exception as e:
        logging.error(f"Verify_visible() -  {element} is not visible.")
        logging.exception(e)
        return False


def get_component_installation_path():
    """
    This api will fetch the installation path from the Installer
    :return: path
    """
    second_exe_installer.Dialog.child_window(title=UI_elements.Install, control_type="Button").wait(
        'ready', timeout=UI_elements.launch_timeout).verify_visible()
    scroll_value = 700
    scroll(scroll_value)
    element_click(title=UI_elements.hip_sdk_core_additional, control_type=UI_elements.button,
                  timeout=UI_elements.click_timeout)
    connected_label = second_exe_installer.Dialog.child_window(control_type="Edit")
    if connected_label.exists(timeout=UI_elements.click_timeout):
        abc = second_exe_installer.Dialog.child_window(control_type="Edit").wait(
            'ready', timeout=2).get_properties()
        path = abc['texts']
        logging.debug(f'Installation path is : {path}')
        element_click(title=UI_elements.hip_sdk_core_additional, control_type=UI_elements.button,
                      timeout=UI_elements.click_timeout)
        return path[0]
    else:
        logging.error("Failed to get the installation path. Make sure HIP SDK core component is visible")


# Function to Validate Installation
def validate_installation(name):
    """
    This api will validate if the installed component is present in the control panel programs and features or not
    :param name: Component installed
    :return: bool
    """
    flag = 0
    for item in winapps.search_installed():
        if name in item.name:
            logging.info(f"Installation of : {name} : has been verified. Installation : SUCCESS")
            if get_sdk_version_detail() in item.version:
                logging.info(f"ROCm Version {get_sdk_version_detail()}: verified ")
                logging.info("Installation Verification Successful")
                flag = 1
                return True
            else:
                logging.error(f" {name} is present in control but Failed to verify ROCm version. "
                              f"Current version is {item.version}. ROCm version provided as per "
                              f"config json file is {get_sdk_version_detail()}")
    if flag == 0:
        logging.error(f"Failed to Validate Installation from control Panel: {name} is not Present in Control panel")


def validate_driver_installation(name):
    """
    This api will validate if the installed driver is present in the control panel programs and features or not
    :param name: Driver installed
    :return: bool
    """
    flag = 0
    for item in winapps.search_installed():
        if name in item.name:
            logging.info(f"Installation of : {name} : has been verified. DRIVERS Installation : SUCCESS")
            flag = 1
            return True
    if flag == 0:
        logging.error(f"Failed to Validate Installation from control Panel: {name} is not Present in Control panel")
        return False


def uninstall_component(name):
    """
    This api will uninstall the component from control panel
    :param name: Component to uninstall
    :return: bool
    """
    try:
        logging.debug(f"{name} is getting uninstalled from Control Panel. Please wait...")
        query = ["wmic.exe", "product", "where", name, "uninstall"]
        run_cmd_call(query)
        logging.debug(f"{name} has been uninstalled from Control Panel.")
        return True

    except Exception as e:
        logging.error(f" uninstall_component() : Failed to Uninstall Program from Control Panel: {name}")
        logging.exception(e)


def alt_f4_close():
    """
    This api will close the installer application using alt+f4 buttons
    :return: bool
    """
    logging.debug("Closing the application using keyboard keys alt+f4")
    bring_to_front()
    second_exe_installer.Dialog.set_focus()
    send_keys('%{F4}')
    sleep(0.5)  # Time required to close the installer and remove process from running processes
    if validate_application_running():
        logging.debug("Successfully closed application using keyboard keys alt+f4")
        return True
    else:
        logging.error("failed to validate app close - alt_f4_close()")


def amd_logo_check():
    """
    This api will check the functionality of AMD Logo button
    """
    try:
        element_click(title=UI_elements.amd_logo,
                      control_type=UI_elements.button,
                      timeout=UI_elements.click_timeout)

    except Exception as e:
        logging.exception(e)
    try:
        app = Application(backend='uia')
        app.connect(title_re=".*Chrome.*")
        element_name = "Address and search bar"
        dlg = app.top_window()
        url = dlg.child_window(title=element_name, control_type="Edit").get_value()
        logging.debug(url)
        dlg.minimize()
    except:
        try:
            app = Application(backend='uia')
            app.connect(title_re=".*Microsoft​ Edge.*", found_index=0)
            dlg = app.top_window()
            wrapper = dlg.child_window(title="App bar", control_type="ToolBar")
            url = wrapper.descendants(control_type='Edit')[0]
            logging.debug(url.get_value())
            url = url.get_value()
            dlg.minimize()
        except Exception as e:
            logging.error("Unable to fetch URL from edge browser")
    if str(url) == 'https://www.amd.com/en':
        logging.info("AMD Logo URL Verified")
        return True


def signup_newsletter_check():
    """
    This api will check the functionality of signup to newsletter link button
    """
    try:
        # element_click(title=UI_elements.signup_for_newsletter,
        #               control_type=UI_elements.button,
        #               timeout=UI_elements.click_timeout)
        second_exe_installer.Dialog.child_window(title=UI_elements.signup_for_newsletter,
                                                 control_type=UI_elements.button).\
            wait('ready', timeout=UI_elements.click_timeout).click_input()
        logging.debug("Clicked on Signup to our newsletter link")
        time.sleep(5)  # sleep time for url to open
    except Exception as e:
        logging.exception(e)
    try:
        app = Application(backend='uia')
        app.connect(title_re=".*Chrome.*")
        element_name = "Address and search bar"
        dlg = app.top_window()
        url = dlg.child_window(title=element_name, control_type="Edit").get_value()
        logging.debug(url)
        dlg.minimize()
    except:
        try:
            app = Application(backend='uia')
            app.connect(title_re=".*Microsoft​ Edge.*", found_index=0)
            dlg = app.top_window()
            wrapper = dlg.child_window(title="App bar", control_type="ToolBar")
            url = wrapper.descendants(control_type='Edit')[0]
            logging.debug(url.get_value())
            url = url.get_value()
            dlg.minimize()
        except Exception as e:
            logging.error("Unable to fetch URL from edge browser. check internet connection and validate link")
            logging.exception(e)
    if str(url) == 'https://explore.amd.com/gaming-software-news/sign-up':
        logging.debug("Newsletter signup URL Verified")
        return True


def screenshot(request):
    """
    This api will take the snapshot of the screen and will store in the Reports folder
    :param request: It takes node name ( TC name ) as input
    """
    try:
        timestamp = os.listdir(r"..\..\Reports")[-1]
        logging.debug(f"timestamp is: {timestamp}")
        logging.info("ERROR SNAPSHOT HAS BEEN TAKEN")
        if not os.path.exists(f'..\..\Reports\{timestamp}_\Installer_Error_Snapshots\{request}'):
            os.makedirs(f'..\..\Reports\{timestamp}\Installer_Error_Snapshots\{request}')
        pyautogui.screenshot(fr"..\..\Reports\{timestamp}\Installer_Error_Snapshots\{request}\Error_Snapshot_for_test_case.png")
    except Exception as e:
        logging.error("Failed to take Snapshot - screenshot()")
        logging.exception(e)


def teardown():
    """Writing the teardown Procedure( WIP )"""

    with open('../../config/uninstall.json', 'r') as f:
        tear_down_object = json.load(f)

    final_list = application_info.installed_software_list()
    # logging.debug(final_list)

    for element in tear_down_object.values():
        if 'uninstall' in tear_down_object.keys():
            for element_i in element.keys():
                if element_i in final_list:
                    uninstall_component(element[element_i])
                    logging.debug(f"Found {element_i} Component in control panel. Uninstalling Component")

    program_files_path = r'C:\Program Files'  # TODO : Fetch the path from installer
    if os.path.exists(os.path.join(program_files_path, "AMD", "ROCm")):
        try:
            # C:\\Program Files\\AMD  ( Default path )
            path = os.path.join(program_files_path, "AMD", "ROCm")
            shutil.rmtree(path)
        except Exception as e:
            logging.exception(e)

    if validate_application_running():
        logging.debug("Teardown Completed")
    else:
        kill_process()
        logging.warning("Previous running instance of Installer has been closed")
        logging.debug("Teardown Completed")


def print_control_identifiers():
    """
    This api will print control identifiers. ( For Dev use only )
    """
    second_exe_installer.Dialog.print_control_identifiers()
