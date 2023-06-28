"""Pywinauto wrapper plugin file contains all the pywinauto functions for Plugins of VS"""
import time
import logging
import win32api
import psutil
import os
import random
import string
import datetime
import pyautogui
from pywinauto.application import Application
from pywinauto import mouse, keyboard
from configparser import ConfigParser
from Core import pywinauto_wrapper
from config import UI_elements
from Core.Subprocess_wrapper import run_cmd_get_output
from library import core_libraries_sdk

conf = ConfigParser()
conf.read("../../config/config.ini")
version = pywinauto_wrapper.get_sdk_version_detail()


def send_keys(key):
    """
    This api will send the keyboard input keys
    :param key: "Key" argument to be passed
    :return: bool
    """
    try:
        logging.debug(f"send_keys() - Typing the provided value : {key} ")
        keyboard.send_keys(key, with_spaces=True)
    except Exception as e:
        logging.error(f"Failed to send the Keyboard input command : {key}")
        logging.exception(e)


def launch_visual_studio(vs_version):
    """
    This api will launch the Visual studio
    :return: bool
    """
    if previous_visual_studio_running_check():
        kill_process()
        logging.warning("Previous Instance of visual studio process has been terminated")

    try:
        logging.debug(f"Launching Visual Studio {vs_version}")
        global vs_window
        vs_window = Application(backend='uia').start(cmd_line=rf"{conf['Plugins'][f'visual_studio_path_{vs_version}']}",
                                                     timeout=UI_elements.click_timeout)
        logging.debug(f"Verifying visibility for Continue _without code Hyperlink .... ")
        vs_window.Dialog.child_window(title="Continue _without code",
                                      control_type="Hyperlink").wait('ready', timeout=30).verify_visible()
        logging.debug(f"Successfully Launched {vs_version}")

        return True

    except Exception as e:
        logging.exception(e)
        logging.error("Something wrong in Visual Studio launch. Please verify Visual studio path and update accordingly"
                      " in config.ini file \n ")
        return False


def kill_process():
    """
    This api will kill the process for Visual Studio application
    """
    try:
        process_name = conf['SDK Process']['Visual_studio_process']
        pid = None
        for proc in psutil.process_iter():
            if process_name in proc.name():
                pid = proc.pid
                p = psutil.Process(pid)
                p.terminate()  # or p.kill()
        logging.debug(f'pid {pid} : process has been terminated. '
                      f'Visual Studio has been closed has been closed')
        time.sleep(2)  # Time required to kill all processes
    except Exception as e:
        logging.error("Failed to kill Visual Studio processes")
        logging.exception(e)


def previous_visual_studio_running_check():
    """
    This api will check if Visual Studio is still running
    :return: bool
    """
    try:
        process_name = conf['SDK Process']['Visual_studio_process']
        pid = None
        for proc in psutil.process_iter():
            if process_name in proc.name():
                pid = proc.pid
        psutil.Process(pid)
        if pid is None:
            logging.debug("No Previous running Visual Studio instance found")
        else:
            logging.warning(f"process is still running {process_name}. Visual Studio running instance found")
            return True
    except Exception as e:
        logging.error("Failed to check previous running instance for Visual Studio")
        logging.exception(e)
        return False


def open_rocm_examples_solution_file():
    # TODO: This api is for the future use , will update the api when solution files are fixed
    try:
        logging.debug("Clicking on Open a _project or solution")
        # vs_window.Dialog.child_window(title="Open a project or solution",
        #                               control_type="Button").wait('ready', timeout=30).click_input()
        vs_window.Dialog.child_window(title="Open a _project or solution", control_type="Text").wait('ready',
                                                                                                     timeout=30).click_input()
        logging.debug("Clicking on Search bar to search all locations")
        vs_window.Dialog.child_window(title="All locations", control_type="SplitButton").wait('ready',
                                                                                              timeout=UI_elements.click_timeout).click_input()
        global current_working_dir
        current_working_dir = os.getcwd()
        logging.debug(f"Current working directory is : {current_working_dir}")

        rocm_examples = conf['Project Path']['ROCm_Examples_sample_application_path']
        abs_rocm_examples = os.path.abspath(rocm_examples)
        logging.debug(f"ROCm Examples folder location provided as per config.ini file is : {abs_rocm_examples}")

        send_keys(abs_rocm_examples)
        send_keys('{ENTER}')

        vs_window.Dialog.child_window(title="File name:", auto_id="1148", control_type="Edit"). \
            wait('ready', timeout=UI_elements.click_timeout).click_input()

        file_name = "ROCm-Examples-VS2019.sln"

        logging.debug(f"open_rocm_examples_solution_file() - Searching for {file_name} file in {abs_rocm_examples}")

        send_keys(file_name)

        # vs_window.Dialog.child_window(title="ROCm-Examples-VS2019.sln", auto_id="9", control_type="ListItem").wait(
        #     'ready',
        #     timeout=10).click_input()

        logging.debug("Selected ROCm-Examples-VS2019.sln file")
        time.sleep(1)
        vs_window.Dialog.child_window(title="Open", auto_id="1", control_type="Button").wait('ready',
                                                                                             timeout=10).click_input()
        logging.debug("Clicked on Open button")

        logging.debug("Opening project or solution")
        # vs_window.Dialog.child_window(title="Solution 'ROCm-Examples-VS2019' ‎", control_type="TreeItem").wait('ready',
        #                                                                                                        timeout=UI_elements.click_timeout).verify_visible()
        try:
            vs_window.Dialog.CancelButton.click_input().wait('ready', timeout=10).click_input()
        except Exception as e:
            logging.debug("Project ROCm-Examples-VS2019 has been opened")
        vs_window.Dialog.child_window(title_re="^Solution 'ROCm-Examples-VS2019'.*", control_type="TreeItem"). \
            wait('ready', timeout=UI_elements.click_timeout).verify_visible()
        logging.debug("Project ROCm-Examples-VS2019 is visible and accessible. Project opened successfully")
        return True

    except Exception as e:
        logging.error("FAILED to open ROCm Examples project!!")
        logging.exception(e)
        return False


def open_a_solution_file(file_path, file_name):
    # TODO: WIP
    try:
        logging.debug("Clicking on Open a _project or solution")
        # vs_window.Dialog.child_window(title="Open a project or solution",
        #                               control_type="Button").wait('ready', timeout=30).click_input()
        vs_window.Dialog.child_window(title="Open a _project or solution", control_type="Text").wait('ready',
                                                                                                     timeout=30).click_input()
        logging.debug("Clicking on Search bar to search all locations")
        vs_window.Dialog.child_window(title="All locations", control_type="SplitButton").wait('ready',
                                                                                              timeout=UI_elements.click_timeout).click_input()
        global current_working_dir
        current_working_dir = os.getcwd()
        logging.debug(f"Current working directory is : {current_working_dir}")

        # rocm_examples = conf['Project Path']['ROCm_Examples_sample_application_path']
        abs_path = os.path.abspath(file_path)
        logging.debug(f"FILE PATH location provided as per config.ini file is : {file_path}")

        send_keys(abs_path)
        send_keys('{ENTER}')

        vs_window.Dialog.child_window(title="File name:", auto_id="1148", control_type="Edit"). \
            wait('ready', timeout=UI_elements.click_timeout).click_input()

        # file_name = "ROCm-Examples-VS2019.sln"

        logging.debug(f"open_a_solution_file() - Searching for {file_name} file in {abs_path}")

        send_keys(file_name)

        # vs_window.Dialog.child_window(title="ROCm-Examples-VS2019.sln", auto_id="9", control_type="ListItem").wait(
        #     'ready',
        #     timeout=10).click_input()

        logging.debug(f"Selected {file_name} file")
        time.sleep(1)
        vs_window.Dialog.child_window(title="Open", auto_id="1", control_type="Button").wait('ready',
                                                                                             timeout=10).click_input()
        logging.debug("Clicked on Open button")

        logging.debug("Opening project or solution")
        # vs_window.Dialog.child_window(title="Solution 'ROCm-Examples-VS2019' ‎", control_type="TreeItem").\
        #     wait('ready', timeout=UI_elements.click_timeout).verify_visible()
        file_name2 = file_name.replace(".sln", "")
        try:
            vs_window.Dialog.CancelButton.click_input().wait('ready', timeout=10).click_input()
        except Exception as e:
            logging.debug(f"Project {file_name} has been opened")
        vs_window.Dialog.child_window(title_re=f"^Solution '{file_name2}'.*", control_type="TreeItem"). \
            wait('ready', timeout=UI_elements.click_timeout).verify_visible()
        logging.debug(f"Project {file_name} is visible and accessible. Project opened successfully")
        return True

    except Exception as e:
        logging.error(f"FAILED to open {file_name} project!!")
        logging.exception(e)
        return False


def navigate_to_installed_extensions():
    """
    This api will navigate to Installed Extensions Dialog and will check for Extension presence and validate its
    Enabled state
    :return: bool
    """
    try:
        logging.debug("Clicking on Continue _without code..")
        vs_window.Dialog.child_window(title="Continue _without code", control_type="Text").wait('ready',
                                                                                                timeout=30).click_input()
        logging.debug("Successfully Clicked on Continue without code link on Visual Studio")
        vs_window.Dialog.child_window(title="Extensions", control_type="MenuItem").wait('ready',
                                                                                        timeout=30).click_input()
        logging.debug("Clicked on Extensions on the Tab")
        vs_window.Dialog.child_window(title="Manage Extensions", control_type="MenuItem", found_index=1).wait('ready',
                                                                                                              timeout=30).click_input()
        logging.debug("Selected Manage Extensions from the drop down")
        vs_window.Dialog.child_window(auto_id="Installed").click_input()
        logging.debug("Opened installed extensions list in the Manage Extensions dialog")
        vs_window.Dialog.child_window(title_re="^AMD HIP Toolchain.*", control_type="ListItem"). \
            wait('ready', timeout=30).click_input()
        logging.debug("Presence of AMD HIP Toolchain has been verified. Extensions are present")

        return True
    except Exception as e:
        logging.warning("Unable to navigating to installed extensions. Failed to validate the presence of extensions")
        logging.exception(e)
        return False


def close_extension_window():
    """
    This local api will close the extension window and will close Visual Studio
    :return: bool
    """
    try:
        logging.debug("Clicking on close button on extension Window")
        vs_window.Dialog.child_window(title="Close", control_type="Button",
                                      auto_id="Button_CloseDialog").click_input()
        logging.debug("Closed Installed Extensions dialog ")
        vs_window.Dialog.child_window(title="Close", control_type="Button", auto_id="Close").click()
        logging.debug("Clicked on Visual Studio close button. Visual Studio has been closed")
        time.sleep(1)  # Sleep Time to kill all processes
    except Exception as e:
        logging.error("Failed to close Installed Extensions dialog and Visual Studio")
        logging.exception(e)


def close_visual_studio():
    """
    This api will close the Visual Studio window
    :return:
    """
    try:
        logging.debug("Clicking on close button on Visual Studio Window")
        vs_window.Dialog.child_window(title="Close", control_type="Button", auto_id="Close").click()
        logging.debug("Visual Studio has been closed")
        time.sleep(1)  # Sleep Time to kill all processes
    except Exception as e:
        logging.warning("Failed to close Visual Studio. close_visual_studio - Killing process to terminate")
        logging.exception(e)
        kill_process()


def extension_verification(request):
    """
    This api will check will extensions are installed in the Visual Studio
    :return:
    """
    try:
        assert navigate_to_installed_extensions(), logging.error("extension_verification() - "
                                                                 "Failed to navigate to Installed Extensions")
        try:
            logging.debug("Plugin Extension has been validated successfully")
            extension_version = vs_window.Dialog.child_window(
                auto_id="TextBlock_DetailVersionValue").get_properties()
            logging.debug(f" Version for the plugin extension is : {extension_version['texts'][0]}")

            logging.debug("Checking Plugin Extension default State..")

            vs_window.Dialog.child_window(title="_Disable", control_type="Text"). \
                wait('ready', timeout=UI_elements.click_timeout).verify_visible()

            close_extension_window()
            return True

        except Exception as e:
            logging.exception(e)

            vs_window.Dialog.child_window(title="_Enable", control_type="Text"). \
                wait('ready', timeout=UI_elements.click_timeout).verify_visible()
            logging.error("Plugin Extension Default state found is DISABLED!!")
            screenshot(request)
            logging.warning("Enabling Plugin Extension now")
            element_click(title="_Enable", control_type="Text", timeout=UI_elements.click_timeout)
            close_extension_window()

            time.sleep(15)  # sleep time required for changes to take effect
            return False

    except Exception as e:
        logging.error("extension_verification() - Failed to validate the Extension in Visual Studio."
                      " Check debug logs for more details")
        logging.exception(e)
        return False


def element_click(title, control_type, timeout):
    """
    This api will click on the element of the provided arguments
    :param title: Title of the UI element
    :param control_type: type of UI element ( button/combobox/list )
    :param timeout: Max time to Click on element
    :return: bool
    """
    try:
        if vs_window.Dialog.child_window(title=title, control_type=control_type).exists(
                timeout=UI_elements.click_timeout):
            vs_window.Dialog.child_window(title=title, control_type=control_type) \
                .wait('ready', timeout=timeout).click_input()
            return True
    except Exception as e:
        logging.error(f"Failed to Click on the element : {title}")
        logging.exception(e)
        return False


def hip_project_template_check(template):
    """
    This api will check if the HIP Project template ( Matrix Transpose ) is visible or not
    :return: bool
    """
    try:
        logging.debug("Clicking on Create new project.")
        vs_window.Dialog.child_window(title_re="^Create.*", control_type="Button").wait(
            'ready', timeout=UI_elements.click_timeout).click_input()
        # vs_window.Dialog.child_window(title="Create a _new project", control_type="Text").wait(
        #     'ready',
        #     timeout=UI_elements.click_timeout).click_input()
        logging.debug("Clicked on Create new project. Checking for AMD HIP Template. clicking on search box")

        vs_window.Dialog.child_window(auto_id="PART_SearchBox").click_input()

        text = "AMD HIP"
        send_keys(text)
        time.sleep(10)  # Sleep time required for templates to load/ Visual Studio stabilization

        if vs_window.Dialog.child_window(title=f"{template}", control_type="ListItem").exists(
                timeout=UI_elements.click_timeout):
            logging.debug(
                f"{template} Template is visible. Extension is Enabled. HIP Project Template Found!")
            time.sleep(2)  # Sleep time for visual studio to refresh
            return True
        else:
            logging.debug("No AMD HIP Template found")

            return False
    except Exception as e:
        logging.error("Failed to check AMD HIP Template - hip_project_template_check()\n Validate installation of "
                      "plugin and extension presence")
        logging.exception(e)
        return False


def create_template_project(template, configuration):
    """
    This api will create a sample project using the AMD HIP Template
    :return: bool
    """
    try:
        if hip_project_template_check(template):
            logging.debug("Selecting default Template Matrix multiplication to create sample project")
            vs_window.Dialog.child_window(title=f"{template}", control_type="ListItem"). \
                wait('ready', timeout=UI_elements.click_timeout).click_input()
            logging.debug("Clicked on Matrix multiplication Template. Clicking on Next Button")

            vs_window.Dialog.child_window(auto_id="button_Next").click_input()
            time.sleep(10)

            global timestamp
            timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d__%H_%M_%S')

            logging.debug(f"Setting the default name for matrix transpose template project : "
                          f"MatrixTranspose_Template_{timestamp}")

            send_keys(f'MatrixTranspose_Template_{timestamp} ')
            logging.debug("Random Project Name has been given - create_template_project()")

            # vs_window.Dialog.child_window(title="Location", auto_id="locationCmb",
            #                               control_type="ComboBox").click_input()
            vs_window.Dialog.child_window(auto_id="PART_EditableTextBox", control_type="Edit").click_input()

            location = conf['Installer Path']['hip_sdk_setup']
            project_location = os.path.abspath(location)

            logging.debug(f"Setting the project location as {project_location}")
            send_keys(project_location)
            vs_window.Dialog.child_window(auto_id="button_Next").click_input()
            app_dialog = vs_window.top_window()
            app_dialog.maximize()

            vs_window.Dialog.child_window(title="Solution Configurations", auto_id="PART_FocusTarget",
                                          control_type="ComboBox").wait(
                'ready', timeout=UI_elements.click_timeout).click_input()

            vs_window.Dialog.child_window(title=f"{configuration}", auto_id=f"{configuration}", control_type="ListItem",
                                          found_index=0).wait(
                'ready',
                timeout=UI_elements.click_timeout).click_input()

            vs_window.Dialog.child_window(title="Solution Platforms", auto_id="PART_FocusTarget",
                                          control_type="ComboBox").wait(
                'ready', timeout=UI_elements.click_timeout).click_input()

            vs_window.Dialog.child_window(title="x64", auto_id="x64", control_type="ListItem", found_index=0).wait(
                'ready',
                timeout=UI_elements.click_timeout).click_input()
            vs_window.Dialog.child_window(title="View", control_type="MenuItem").wait('ready',
                                                                                      timeout=UI_elements.click_timeout).click_input()
            vs_window.Dialog.child_window(title="Solution Explorer", control_type="MenuItem", found_index=0).wait(
                'ready',
                timeout=UI_elements.click_timeout).click_input()
            vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*.{timestamp}.*", control_type="TreeItem") \
                .wait('ready', timeout=UI_elements.click_timeout).expand()
            logging.debug("Project creation successful - create_template_project()")
            return True
        else:
            logging.error("create_template_project() - Failed to create template project. Template not visible")
            return False

    except Exception as e:
        logging.error("create_template_project() - Failed to create template project")
        logging.exception(e)
        return False


def build_template_project(compiler, configuration):
    """
    This api will build and execute the created sample project using the template
    :param configuration:
    :param compiler: Compiler to use ( HIP_Clang or HIP_nvcc )
    :return: bool
    """
    try:
        generated_log_path = ""
        logging.debug(f"Verifying the outer configuration. Setting value to provided :   *** {configuration} ***")
        vs_window.Dialog.child_window(title="Solution Configurations", auto_id="PART_FocusTarget",
                                      control_type="ComboBox").wait(
            'ready', timeout=UI_elements.click_timeout).click_input()

        vs_window.Dialog.child_window(title=f"{configuration}", auto_id=f"{configuration}",
                                      control_type="ListItem", found_index=0). \
            wait('ready', timeout=UI_elements.click_timeout).click_input()

        vs_window.Dialog.child_window(title="Solution Platforms", auto_id="PART_FocusTarget",
                                      control_type="ComboBox").wait(
            'ready', timeout=UI_elements.click_timeout).click_input()

        vs_window.Dialog.child_window(title="x64", auto_id="x64", control_type="ListItem", found_index=0).wait(
            'ready', timeout=UI_elements.click_timeout).click_input()

        if vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*",
                                         control_type="TreeItem").exists(timeout=UI_elements.click_timeout):
            try:
                logging.debug("Building Project, Checking for the Compiler set to project")
                # vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*.{timestamp} ‎({compiler})",
                #                               control_type="TreeItem").verify_visible()
                vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*.({compiler})",
                                              control_type="TreeItem").verify_visible()
                logging.debug(f"Parameter passed for compiler {compiler} , is verified. "
                              f"Building the project using {compiler} compiler")

                # ************************************************************************
                logging.debug(
                    f"Verifying the Properties configuration. Setting value to provided :   *** {configuration} ***")
                vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*",
                                              control_type="TreeItem").right_click_input()
                vs_window.Dialog.child_window(title="Properties", control_type="MenuItem"). \
                    wait('ready', timeout=UI_elements.click_timeout).click_input()
                time.sleep(1)
                vs_window.Dialog.child_window(title="Configuration:", control_type="ComboBox"). \
                    wait('ready', timeout=UI_elements.click_timeout).click_input()
                vs_window.Dialog.child_window(title=f"{configuration}", control_type="ListItem"). \
                    wait('ready', timeout=UI_elements.click_timeout).click_input()
                vs_window.Dialog.child_window(title="Platform:", control_type="ComboBox"). \
                    wait('ready', timeout=UI_elements.click_timeout).click_input()
                vs_window.Dialog.child_window(title="x64", control_type="ListItem"). \
                    wait('ready', timeout=UI_elements.click_timeout).click_input()
                vs_window.Dialog.child_window(title="OK", auto_id="1", control_type="Button"). \
                    wait('ready', timeout=UI_elements.click_timeout).click_input()
                # ************************************************************************

            except Exception:
                logging.warning(f"Parameter passed for compiler {compiler} , is not verified. Changing to "
                                f"{compiler} compiler")
                vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*",
                                              control_type="TreeItem").right_click_input()
                change_compiler(compiler, configuration)
                logging.debug(f"Compiler has been changed to requested {compiler}")

            vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*",
                                          control_type="TreeItem").right_click_input()

            logging.debug(f"Clicked on MatrixTranspose_Template")

            vs_window.Dialog.child_window(title="Rebuild", control_type="MenuItem").\
                wait('ready', timeout=UI_elements.click_timeout).click_input()
            logging.debug(f"Right click on project and clicked on rebuild project.")

            vs_window.Dialog.child_window(title="Rebuild All succeeded", control_type="Text").\
                wait('ready', timeout=UI_elements.build_timeout).click_input()
            logging.debug("Building the Project is successful")

            return True

        else:
            logging.debug("Unable to Find the project created. FAILED")
            vs_window.Dialog.child_window(title="Close", auto_id="button_Close", control_type="Button").click_input()
            logging.debug("Visual Studio has been closed")
            return False

    except Exception as e:
        logging.exception(e)
        logging.error("build_template_project() - Failed to Build project ")
        return False


def execute_template_project():
    """
    This api will check the logs for template project build and will execute the template project exe file
    :return bool
    """
    generated_log_path = ""
    core_directory = conf['Installer Path']['hip_sdk_setup']
    logging.debug(f"Starting verification and execution of exe file generated - execute_template_project()")
    for root, dirs, files in os.walk(core_directory):
        for filename in files:
            if filename == f"MatrixTranspose_Template_{timestamp}.log":
                logging.debug(f"Generated log file path : {os.path.abspath(os.path.join(root, filename))}")
                generated_log_path = os.path.abspath(os.path.join(root, filename))
                logging.debug(f"This is generated_log_path: {generated_log_path} - execute_template_project()")

    f = open(generated_log_path, "r")

    project_directory = os.path.abspath(os.path.join(core_directory, f"MatrixTranspose_Template_{timestamp}"))

    if f"MatrixTranspose_Template_{timestamp}.exe" in f.read():
        if ': error :' not in f.read():
            logging.debug("Project build succeeded WITHOUT ERRORS. Executing the exe generated now...")

            execute_all_project_paths(project_directory)
            logging.debug("FINISHED executing the exe file generated")
            return True


def target_gpu_check(target, compiler, configuration):
    """
    This api will set the GPU offload architecture to all provided architectures
    :param configuration:
    :param target: Provided Architecture
    :param compiler: Provided Compiler ( HIP_Clang or HIP_nvcc )
    :return:bool
    """
    temp_compiler_name = compiler.replace("HIP_", "")
    try:
        logging.debug("Right click on template")
        try:
            logging.debug("Checking for the compiler in template name")
            # vs_window.Dialog.child_window(title=f"MatrixTranspose.*.{timestamp} ‎({compiler})",
            #                               control_type="TreeItem").wait('ready',
            #                                                             timeout=UI_elements.click_timeout).verify_visible()
            vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*.({compiler})",
                                          control_type="TreeItem").verify_visible()
            logging.debug(f"Parameter passed for compiler {compiler} , is verified. "
                          f"Building the project using {compiler} compiler")
        except Exception as e:
            logging.debug(e)
            logging.debug("Changing compiler to requested compiler in template...")
            change_compiler(compiler, configuration)

        logging.debug("right click on template")
        vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*.({compiler})",
                                      control_type="TreeItem").wait('ready',
                                                                    timeout=UI_elements.click_timeout).right_click_input()
        logging.debug("clicked on properties element in template dialog...")
        vs_window.Dialog.child_window(title="Properties", control_type="MenuItem").wait('ready',
                                                                                        timeout=UI_elements.click_timeout).click_input()
        logging.debug("Opening properties Dialog")

        # vs_window.Dialog.child_window(title=f"General [AMD HIP for {temp_compiler_name}]", control_type="TreeItem"). \
        #     wait('ready', timeout=UI_elements.click_timeout).click_input()

        try:
            app_dialog = vs_window.top_window()
            app_dialog.minimize()
            app_dialog.restore()
            app_dialog.set_focus()
        except Exception as e:
            logging.warning(e)
        logging.debug(f"Clicking on : General [AMD HIP for {temp_compiler_name}]")
        time.sleep(5)

        vs_window.Dialog.child_window(title=f"General [AMD HIP for {temp_compiler_name}]",
                                      control_type="TreeItem").wait('ready', timeout=10).click_input()

        # ************************************************************************
        time.sleep(1)
        vs_window.Dialog.child_window(title="Configuration:", control_type="ComboBox"). \
            wait('ready', timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title=f"{configuration}", control_type="ListItem"). \
            wait('ready', timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="Platform:", control_type="ComboBox"). \
            wait('ready', timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="x64", control_type="ListItem"). \
            wait('ready', timeout=UI_elements.click_timeout).click_input()
        # ************************************************************************

        logging.debug("clicking on Offload Architectures...")

        vs_window.Dialog.child_window(title="Offload Architectures", control_type="TreeItem"). \
            wait('ready', timeout=UI_elements.click_timeout).click_input(button="left", double=True)

        # x, y = win32api.GetCursorPos()
        # mouse.double_click(button='left', coords=(x, y))

        logging.debug("Sending requested architecture to Offload Architectures values...")
        send_keys(target)
        vs_window.Dialog.child_window(title="OK", auto_id="1", control_type="Button").wait('ready',
                                                                                           timeout=UI_elements.click_timeout).click_input()
        return True

    except Exception as e:
        logging.exception(e)
        logging.error(f"target_gpu_check() - Failed to change architecture for the provided {target} architecture")
        return False


def configuration_properties(compiler, configuration):
    """
    This api will compare the default configuration options for the provided compiler
    :param configuration:
    :param compiler: Compiler to check ( HIP_Clang or HIP_nvcc )
    :return: bool
    """

    # clang_properties_list = ['Yes', '$(HIPRootDir)bin\\', 'Yes (-v)', '', '$(HIP_PATH)\\', '', '$(HIPRootDir)lib',
    #                          'amdhip64', '$(HIPRootDir)lib\\bitcode', '', '', 'gfx900;gfx906;gfx908;gfx90a;gfx1030']

    clang_properties_list = ['Yes', 'Yes (-v)', '', '', '$(HIP_PATH)', '$(HIPFoundDir)', '$(HIPRootDir)bin',
                             '$(HIPRootDir)include', '$(HIPRootDir)lib\\bitcode', '$(HIPRootDir)lib',
                             'amdhip64', '', '', '', 'gfx900;gfx906;gfx908;gfx90a;gfx1030']

    # nvcc_properties_list = ['$(HIP_PATH)\\', 'Yes', '$(CUDA_PATH)\\', '$(CUDARootDir)bin', r'$(CUDARootDir)lib\x64',
    #                         'Yes (-v)', '']

    nvcc_properties_list = ['', '$(HIP_PATH)', '$(HIPFoundDir)', '$(HIPRootDir)include', 'Yes', '', '$(CUDA_PATH)',
                            '$(CUDAFoundDir)', r'$(CUDARootDir)\bin', '$(CUDARootDir)\include',
                            r'$(CUDARootDir)\lib\x64',
                            'Yes (-v)', '']

    configuration_list = []
    temp_compiler_name = compiler.replace("HIP_", "")
    visibility_timeout = 2

    try:
        vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*.({compiler})",
                                      control_type="TreeItem").verify_visible()
        logging.debug(f"Parameter passed for compiler {compiler} , is verified for project. ")

    except Exception as e:
        logging.info(e)
        vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*",
                                      control_type="TreeItem").wait('ready',
                                                                    timeout=UI_elements.click_timeout).right_click_input()
        change_compiler(compiler, configuration)

    vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*.({compiler})",
                                  control_type="TreeItem").wait('ready',
                                                                timeout=UI_elements.click_timeout).right_click_input()
    vs_window.Dialog.child_window(title="Properties", control_type="MenuItem").wait('ready',
                                                                                    timeout=UI_elements.click_timeout).click_input()
    time.sleep(1)
    logging.debug(f"Clicking on : General [AMD HIP for {temp_compiler_name}]")
    time.sleep(5)

    vs_window.Dialog.child_window(title=f"General [AMD HIP for {temp_compiler_name}]",
                                  control_type="TreeItem").wait('ready', timeout=10).click_input()

    # ************************************************************************
    time.sleep(1)
    vs_window.Dialog.child_window(title="Configuration:", control_type="ComboBox"). \
        wait('ready', timeout=UI_elements.click_timeout).click_input()
    vs_window.Dialog.child_window(title=f"{configuration}", control_type="ListItem"). \
        wait('ready', timeout=UI_elements.click_timeout).click_input()
    vs_window.Dialog.child_window(title="Platform:", control_type="ComboBox"). \
        wait('ready', timeout=UI_elements.click_timeout).click_input()
    vs_window.Dialog.child_window(title="x64", control_type="ListItem"). \
        wait('ready', timeout=UI_elements.click_timeout).click_input()
    # ************************************************************************

    if compiler == "clang":
        vs_window.Dialog.child_window(title="Position", control_type="Thumb", found_index=0). \
                wait('ready', timeout=10).click_input(button='left', double=False, wheel_dist=10, pressed='')

        pyautogui.scroll(800)

    if compiler == "HIP_clang":
        error_flag = 0
        clang_config_name_list = ["Use clang", "Verbose Mode",
                                  "Additional Compiler Options", "HIP Custom Root Directory",
                                  "HIP Found Directory",
                                  "HIP Root Directory", "HIP Executable Directory", "HIP Include Directory",
                                  "HIP Device Libraries Directory",
                                  "HIP Host Library Directory",
                                  "HIP Host Library Name", "HIP Path", "HIP Version",
                                  "Print ROCm Search Directories",
                                  "Offload Architectures", ]

        for prop_name in clang_config_name_list:
            try:
                text = vs_window.Dialog.child_window(title=f"{prop_name}", control_type="TreeItem",
                                                     found_index=0).wrapper_object()
                logging.debug(f"For {prop_name} This is the value from use clang : {text.legacy_properties()['Value']}")
                configuration_list.append(text.legacy_properties()['Value'])
            except Exception as e:
                # logging.error(f"Configuration property for {text.legacy_properties()['Value']} DOES NOT MATCH")
                logging.exception(e)
                error_flag = 1

        logging.debug(f"This is Live fetched list : {configuration_list}")
        logging.debug(f"This is Golden data list : {clang_properties_list}")

        if configuration_list == clang_properties_list:

            logging.debug("All configuration for clang compiler are verified are verified")
            if error_flag == 0:
                return True
        else:
            logging.error("Failed to validate All configuration for clang compiler. ")

            l_func1 = lambda x, y: list((set(x) - set(y)))
            l_func2 = lambda x, y: list((set(y) - set(x)))

            clang_properties_list.sort()
            configuration_list.sort()

            expected_result = l_func1(clang_properties_list, configuration_list)
            live_result = l_func2(clang_properties_list, configuration_list)

            logging.debug(f" Expected_result: {expected_result}")
            logging.debug(f" Found result: {live_result}")
            return False

    if compiler == "HIP_nvcc":
        error_flag = 0
        nvcc_config_name_list = ['HIP Custom Root Directory', 'HIP Found Directory', 'HIP Root Directory',
                                 'HIP Include Directory', 'Use nvcc',
                                 'CUDA Custom Root Directory', 'CUDA Found Directory', 'CUDA Root Directory',
                                 'CUDA Executable Directory', 'CUDA Include Directory',
                                 'CUDA Library Directory', 'Verbose Mode', 'Additional Compiler Options']

        for prop_name in nvcc_config_name_list:
            try:
                text = vs_window.Dialog.child_window(title=f"{prop_name}", control_type="TreeItem",
                                                     found_index=0).wrapper_object()
                logging.debug(f"For {prop_name} this is the value from use clang : {text.legacy_properties()['Value']}")
                configuration_list.append(text.legacy_properties()['Value'])
            except Exception as e:
                logging.error(f"Configuration property for {text.legacy_properties()['Value']} DOES NOT MATCH")
                logging.exception(e)
                error_flag = 1

        logging.debug(f"This is Live fetched list : {configuration_list}")
        logging.debug(f"This is Golden data list : {nvcc_properties_list}")

        if configuration_list == nvcc_properties_list:
            logging.debug("All configuration for clang compiler are verified are verified")
            if error_flag == 0:
                return True
        else:
            logging.error("Failed to validate All configuration for clang compiler.")

            l_func1 = lambda x, y: list((set(x) - set(y)))
            l_func2 = lambda x, y: list((set(y) - set(x)))

            nvcc_properties_list.sort()
            configuration_list.sort()

            expected_result = l_func1(nvcc_properties_list, configuration_list)
            live_result = l_func2(nvcc_properties_list, configuration_list)

            logging.debug(f" Expected_result: {expected_result}")
            logging.debug(f" Found result: {live_result}")
            return False


def build_all_sample_applications(project_path, compiler, test_name, configuration):
    """
    This api will build all sample application ( rocm- examples ) project, present in HIP_SDK_Setup folder
    :param project_path: Path of the project ( mentioned in config.ini)
    :param compiler: Compiler to use (HIP_Clang or HIP_nvcc )
    :param test_name: Name of test case
    :param configuration : Debug/release
    :return: bool
    """
    try:
        logging.debug("Building all sln files under ROCm examples")
        vs_window.Dialog.child_window(title="Solution Configurations", auto_id="PART_FocusTarget",
                                      control_type="ComboBox").wait('ready', timeout=20).click_input()
        vs_window.Dialog.child_window(title=f"{configuration}", auto_id=f"{configuration}", control_type="ListItem",
                                      found_index=0).wait('ready',
                                                          timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="View", control_type="MenuItem"). \
            wait('ready', timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="Solution Explorer", control_type="MenuItem", found_index=0). \
            wait('ready', timeout=UI_elements.click_timeout).click_input()

        sample_application_folder_expand(project_path, compiler, configuration)

        up_scroll = 800
        pyautogui.scroll(up_scroll)  # scrolling to the top of configuration properties dialog

        vs_window.Dialog.child_window(title_re="^Solution 'ROCm-Examples-VS2019'.*", control_type="TreeItem"). \
            wait('ready', timeout=UI_elements.click_timeout).right_click_input()

        vs_window.Dialog.child_window(title="Rebuild Solution", control_type="MenuItem"). \
            wait('ready', timeout=20).click_input()
        error_flag = 0
        try:
            vs_window.Dialog.child_window(title="Rebuild All succeeded", control_type="Text"). \
                wait('ready', timeout=UI_elements.build_timeout).click_input()
            logging.debug("Rebuild all Project has been succeeded.")

        except Exception as e:
            logging.error(f"Failed to build all projects successfully. Rebuild success not found. "
                          f"Check logs if few projects failed to build\n{e}")
            error_flag = 1

        logging.debug("Saving the build output and validating the result")
        save_build_output_and_validate_result(project_path, test_name)

        if error_flag == 0:
            logging.debug("Build is success, Executing the .exe files generated for the respective builds")
            execute_all_project_paths(project_path)
            return True
        else:
            return False

    except Exception as e:
        logging.exception(e)
        logging.error("Failed to Build Sample application project using Clang Compiler")
        return False


def sample_application_folder_expand(project_path, compiler, configuration):
    """
    This api will expand all folders present in rocm-examples project, and will check the compiler status, if required,
     will change the compiler
    :param configuration:
    :param project_path: Path of the project ( mentioned in config.ini)
    :param compiler: Compiler to use (HIP_Clang or HIP_nvcc )
    :return: bool
    """
    visiblity_timeout = 2
    vs_window.Dialog.child_window(title="HIP-Basic", control_type="TreeItem").wait('ready',
                                                                                   timeout=UI_elements.click_timeout).expand()
    vs_window.Dialog.child_window(title="HIP-Basic", control_type="TreeItem").wait('ready',
                                                                                   timeout=UI_elements.click_timeout).click_input()
    pyautogui.scroll(-800)
    vs_window.Dialog.child_window(title="Libraries", control_type="TreeItem").wait('ready',
                                                                                   timeout=UI_elements.click_timeout).expand()
    logging.debug("expanding libraries directory successfully....")
    pyautogui.scroll(-800)
    vs_window.Dialog.child_window(title="exampleLibraryTemplate", control_type="TreeItem").wait('ready',
                                                                                                timeout=UI_elements.click_timeout).expand()
    logging.debug("expanding exampleLibraryTemplate directory successfully....")
    pyautogui.scroll(-800)
    vs_window.Dialog.child_window(title="hipCUB", control_type="TreeItem").wait('ready',
                                                                                timeout=UI_elements.click_timeout).expand()
    logging.debug("expanding hipCUB directory successfully....")
    pyautogui.scroll(-800)
    vs_window.Dialog.child_window(title="rocPRIM", control_type="TreeItem").wait('ready',
                                                                                 timeout=UI_elements.click_timeout).expand()
    logging.debug("expanding rocPRIM directory successfully....")
    pyautogui.scroll(-800)
    vs_window.Dialog.child_window(title="rocRAND", control_type="TreeItem").wait('ready',
                                                                                 timeout=UI_elements.click_timeout).expand()
    logging.debug("expanding rocRAND directory successfully....")
    vs_window.Dialog.child_window(title="rocThrust", control_type="TreeItem").wait('ready',
                                                                                   timeout=UI_elements.click_timeout).expand()
    pyautogui.scroll(800)

    generated_exe_name = []
    all_exe = []
    repeated_projects = ["ROCm-Examples-VS2019.sln"]
    for root, dirs, files in os.walk(project_path):
        for filename in files:
            if filename.endswith(".sln"):
                if filename not in repeated_projects:
                    x = os.path.splitext(filename)[0]
                    generated_exe_name.append(x)
    logging.debug(f"Total sln files found in the project are {len(generated_exe_name)}")
    logging.debug(f"Names of sln files found in the project are {generated_exe_name}")

    for project in generated_exe_name:
        if project not in all_exe:
            try:
                up_scroll = 800
                pyautogui.scroll(up_scroll)
                vs_window.Dialog.child_window(title=f"{project} ‎({compiler})", control_type="TreeItem",
                                              found_index=0).wait(
                    'ready',
                    timeout=visiblity_timeout).click_input()
                logging.debug(f"verifying {project} successfully.....")
                all_exe.append(project)

            except Exception:
                vs_window.Dialog.child_window(title_re=f"^{project}.*", control_type="TreeItem", found_index=0).wait(
                    'ready',
                    timeout=UI_elements.click_timeout).right_click_input()
                change_compiler(compiler, configuration)
                logging.debug(f"fChanging compiler is successfully in {project}...")
                all_exe.append(project)
        else:
            try:
                pyautogui.scroll(800)
                vs_window.Dialog.child_window(title=f"{project} ‎({compiler})", control_type="TreeItem",
                                              found_index=1).wait(
                    'ready',
                    timeout=visiblity_timeout).click_input()
                logging.debug(f"verifying {project} successfully.....")
            except Exception:
                vs_window.Dialog.child_window(title_re=f"^{project}.*", control_type="TreeItem", found_index=1).wait(
                    'ready',
                    timeout=UI_elements.click_timeout).right_click_input()
                change_compiler(compiler, configuration)
                logging.debug(f"Changing compiler is successfully in {project}...")


def change_compiler(compiler, configuration):
    """
    This api will change the compiler to the provided value
    :param configuration:
    :param compiler: Compiler to use (HIP_Clang or HIP_nvcc )
    :return: bool
    """
    try:
        compiler = compiler.replace("HIP_", "")
        logging.debug(f"change_compiler() - Changing the compiler to provided {compiler} compiler ")

        vs_window.Dialog.child_window(title="Properties", control_type="MenuItem").wait('ready',
                                                                                        timeout=UI_elements.click_timeout).click_input()

        vs_window.Dialog.child_window(title="Configuration:", control_type="ComboBox").wait('ready',
                                                                                            timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title=f"{configuration}", control_type="ListItem").wait('ready',
                                                                                              timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="Platform:", control_type="ComboBox").wait('ready',
                                                                                       timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="x64", control_type="ListItem").wait(
            'ready',
            timeout=UI_elements.click_timeout).click_input()

        vs_window.Dialog.child_window(title="Platform Toolset", control_type="TreeItem").wait('ready',
                                                                                              timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="Open", control_type="Button", found_index=0).wait('ready',
                                                                                               timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title=f"AMD HIP for {compiler} Compiler", control_type="ListItem").wait('ready',
                                                                                         timeout=10).click_input()
        try:
            vs_window.Dialog.child_window(title="Apply", auto_id="12321", control_type="Button").wait('ready',
                                                                                                      timeout=UI_elements.click_timeout).click_input()
            vs_window.Dialog.child_window(title="OK", auto_id="1", control_type="Button").wait('ready',
                                                                                               timeout=UI_elements.click_timeout).click_input()
        except:
            vs_window.Dialog.child_window(title="OK", auto_id="1", control_type="Button").wait('ready',
                                                                                               timeout=UI_elements.click_timeout).click_input()
        logging.debug(
            f"change_compiler() - Changing the compiler to provided {compiler} compiler Completed Successfully")
        return True
    except Exception as e:
        logging.error(e)
        logging.exception("Requested compiler is not visible")
        return False


def save_build_output_and_validate_result(project_path, test_name):
    """
    This api will save the output result log of sample project run and will validate if all the exe are present in
    the logs with no errors and bild is success
    :param project_path: Path of the project ( mentioned in config.ini)
    :param test_name: Name of test sln file
    :return: bool
    """
    try:
        vs_window.Dialog.child_window(title="Output", control_type="Text", found_index=0).click_input(button="left",
                                                                                                      double=True)
        vs_window.Dialog.child_window(title="File", control_type="MenuItem").wait('ready',
                                                                                  timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="Save Output As...", control_type="MenuItem").wait('ready',
                                                                                               timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="All locations", control_type="SplitButton").wait('ready',
                                                                                              timeout=UI_elements.click_timeout).click_input()

        global last_log_folder
        last_log_folder = os.listdir(r"..\..\Reports")[-1]  # This will go to Reports folder from current Plugin Folder
        logging.debug(f"Saving Logs and output Results to {last_log_folder} in Reports folder")

        temp = (f'..\..\Reports\{last_log_folder}')
        path = os.path.abspath(temp)

        send_keys(path)
        send_keys('{ENTER}')

        vs_window.Dialog.child_window(title="File name:", auto_id="1001", control_type="Edit"). \
            wait('ready', timeout=UI_elements.click_timeout).click_input()

        build_log_file_name = "Build_output_logs_GUI_" + test_name + last_log_folder

        send_keys(build_log_file_name)  # Typed the file name to save

        vs_window.Dialog.child_window(title="Save", control_type="SplitButton"). \
            wait('ready', timeout=UI_elements.click_timeout).click_input()

        path_output = "Build_output_logs_GUI_" + test_name + last_log_folder + ".txt"

        fullpath = os.path.join(path, path_output)
        file1 = open(fullpath, "r+")
        data = file1.read()
        # data1 = file1.readline()
        logging.debug(f"\n\nComplete Solution build output logs:  \n\n{data}\n\n")

        all_exe_path = get_all_exe_path(project_path)
        for i in all_exe_path:  # TODO: Will change later
            if i in data:
                logging.debug(f"Build is Success for : {i}\n")
            else:
                logging.warning(f"Build is FAILED/SKIPPED for : {i}\n")

    except Exception as e:
        logging.error("save_build_output_and_validate_result() - Failed to validate build result")
        logging.exception(e)


def get_all_exe_path(project_path):
    """
    This api will return all the exe files present in the project rocm-examples
    :param project_path: Path of the project ( mentioned in config.ini)
    :return: list of all exe files
    """
    try:
        # logging.debug(f"this is the current working directory in get_all_exe(): {os.getcwd()}")
        # path = conf['Project Path']['ROCm_Examples_sample_application_path']
        generated_exe_path = []
        for root, dirs, files in os.walk(project_path):
            for filename in files:
                if filename.endswith(".exe"):
                    generated_exe_path.append(os.path.abspath(os.path.join(root, filename)))
        logging.debug(f"This is generated exe path {generated_exe_path} in {project_path} - get_all_exe_path()")
        sln_names = []
        repeated_projects = ["ROCm-Examples-VS2019.sln"]
        for root, dirs, files in os.walk(project_path):
            for filename in files:
                if filename.endswith(".sln"):
                    if filename not in repeated_projects:
                        x = os.path.splitext(filename)[0]
                        sln_names.append(x)
        logging.debug(f"get_all_exe_path() - This is the list of all exe found : {generated_exe_path}")
        logging.debug(f"Total expected count is ( .sln files count ): {len(sln_names)}. "
                      f"  exe files found for this run : {len(generated_exe_path)}")
        return generated_exe_path  # This is all exe path
    except Exception as e:
        logging.error("Failed to fetch all exe path in the rocm-examples project folder")
        logging.exception(e)


def execute_all_project_paths(project_path):
    """
    This api will execute all the exe files present in the project path
    :param project_path: Path of the project ( mentioned in config.ini)
    """
    try:
        # data = get_all_exe_path("rocm-examples")
        logging.debug("Called api - execute_all_project_paths()")
        data = get_all_exe_path(project_path)
        logging.debug(f"RUNNING ALL exe BUILDS\n")
        for i in data:
            query = fr'cd "{os.path.dirname(i)}" && {i}'
            catch = run_cmd_get_output(query)
            logging.debug(f"Output of build {i} is : \n{catch}\n\n")
        logging.debug(f"RUNNING ALL exe COMPLETED.\n")
        return True
    except Exception as e:
        logging.error(f"Failed to execute all exe path in {project_path} project folder")
        logging.exception(e)
        return False


def change_configuration_properties(compiler, configuration):
    """
        This api will compare the default configuration options for the provided compiler
        :param configuration:
        :param compiler: Compiler to check ( HIP_Clang or HIP_nvcc )
        :return: bool
        """

    clang_config_name_list = ["Additional Compiler Options",
                              'HIP Custom Root Directory',
                              "HIP Path",
                              "HIP Host Library Name",
                              "HIP Version", "Print ROCm Search Directories",
                              "Offload Architectures", ]

    nvcc_config_name_list = ['CUDA Custom Root Directory', 'Verbose Mode', 'Additional Compiler Options']

    error_flag = 0
    if compiler == "HIP_clang":
        error_flag = 0
        for prop_name in clang_config_name_list:
            logging.debug(f"Passing invalid value to **** {prop_name} **** and checking for build")
            if pass_invalid_configuration_property_value(compiler, timestamp, configuration, prop_name) != 0:
                error_flag += 1

    if compiler == "HIP_nvcc":
        error_flag = 0
        for prop_name in nvcc_config_name_list:
            logging.debug(f"Passing invalid value to **** {prop_name} **** and checking for build")
            if pass_invalid_configuration_property_value(compiler, timestamp, configuration, prop_name) != 0:
                error_flag += 1

    logging.info(f"Value of error flag = {error_flag}")
    if error_flag == 0:
        return True
    else:
        logging.error("For provided invalid values, For Some config, Build was Success. FAILURE!!")
        return False


def pass_invalid_configuration_property_value(compiler, timestamp, configuration, prop_name):
    """This api will pass invalid parameters to the configuration properties
    Compiler: Compiler selected
    timestamp: Current time
    Configuration: debug/Release
    Prop_name: property name selected from list
    """
    visibility_timeout = 2
    temp_compiler_name = compiler.replace("HIP_", "")
    error_flag = 0
    try:
        try:
            vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*.({compiler})",
                                          control_type="TreeItem").verify_visible()
            logging.debug(f"Parameter passed for compiler {compiler} , is verified. "
                          f"Building the project using {compiler} compiler")
        except Exception:
            vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*",
                                          control_type="TreeItem").wait('ready',
                                                                        timeout=UI_elements.click_timeout).right_click_input()
            change_compiler(compiler, configuration)

        vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*.({compiler})",
                                      control_type="TreeItem").wait('ready', timeout=UI_elements.click_timeout). \
            right_click_input()

        vs_window.Dialog.child_window(title="Properties", control_type="MenuItem"). \
            wait('ready', timeout=UI_elements.click_timeout).click_input()

        time.sleep(1)
        logging.debug(f"Clicking on : General [AMD HIP for {temp_compiler_name}]")
        time.sleep(5)

        vs_window.Dialog.child_window(title=f"General [AMD HIP for {temp_compiler_name}]",
                                      control_type="TreeItem").wait('ready', timeout=10).click_input()

        # ************************************************************************
        time.sleep(1)
        vs_window.Dialog.child_window(title="Configuration:", control_type="ComboBox"). \
            wait('ready', timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title=f"{configuration}", control_type="ListItem"). \
            wait('ready', timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="Platform:", control_type="ComboBox"). \
            wait('ready', timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="x64", control_type="ListItem"). \
            wait('ready', timeout=UI_elements.click_timeout).click_input()
        # ************************************************************************

        vs_window.Dialog.child_window(title="Position", control_type="Thumb", found_index=0). \
            wait('ready', timeout=10).click_input(button='left', double=False, wheel_dist=10, pressed='')

        pyautogui.scroll(800)

        vs_window.Dialog.child_window(title=f"{prop_name}", control_type="TreeItem").click_input(button="left",
                                                                                                 double=True)

        send_keys("Invalid_Data")

        vs_window.Dialog.child_window(title="OK", auto_id="1", control_type="Button").wait(
            'ready', timeout=10).click_input()

        if build_template_project(compiler, configuration):
            error_flag = 1
            logging.debug(f"Build is successful even if we change {prop_name} to invalid value")
        else:
            logging.debug(f"Build is un-successful if we change {prop_name} to invalid value")

        try:
            vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*.({compiler})",
                                          control_type="TreeItem").verify_visible()
            logging.debug(f"Parameter passed for compiler {compiler} , is verified. ")
        except Exception:
            vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*",
                                          control_type="TreeItem").wait('ready',
                                                                        timeout=UI_elements.click_timeout).right_click_input()
            change_compiler(compiler, configuration)

        vs_window.Dialog.child_window(title_re=f"^MatrixTranspose.*.({compiler})",
                                      control_type="TreeItem").wait('ready',
                                                                    timeout=UI_elements.click_timeout).right_click_input()
        vs_window.Dialog.child_window(title="Properties", control_type="MenuItem").wait('ready',
                                                                                        timeout=UI_elements.click_timeout).click_input()
        time.sleep(2)
        vs_window.Dialog.child_window(title=f"General [AMD HIP for {temp_compiler_name}]",
                                      control_type="TreeItem").wait( 'ready', timeout=10).click_input()
        time.sleep(1)

        vs_window.Dialog.child_window(title="Position", control_type="Thumb", found_index=0). \
            wait('ready', timeout=10).click_input(button='left', double=False, wheel_dist=10, pressed='')
        pyautogui.scroll(800)

        vs_window.Dialog.child_window(title=f"{prop_name}", control_type="TreeItem").click_input(button="left",
                                                                                                 double=True)

        vs_window.Dialog.child_window(title="Open", control_type="Button", found_index=0).wait('ready',
                                                                                               timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="<inherit from parent or project defaults>",
                                      control_type="ListItem").wait('ready',
                                                                    timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="OK", auto_id="1", control_type="Button").wait(
            'ready',
            timeout=10).click_input()

    except Exception as e:
        logging.exception(e)

    if error_flag == 1:
        logging.error(f"For few invalid values provided for {prop_name}, build is success, check logs for details")
        return error_flag
    else:
        return error_flag


def create_header_file():
    """
    This api will create a header file from scratch in the template project
    :return:
    """
    try:
        vs_window.Dialog.child_window(title="Header Files", control_type="TreeItem").wait(
            'ready',
            timeout=10).right_click_input()
        vs_window.Dialog.child_window(title="Add", control_type="MenuItem").wait(
            'ready',
            timeout=10).click_input()
        vs_window.Dialog.child_window(title="New Item...", control_type="MenuItem").wait(
            'ready',
            timeout=10).click_input()
        vs_window.Dialog.child_window(title="Installed", auto_id="Installed:ToggleButton", control_type="Button").wait(
            'ready',
            timeout=10).click_input()
        vs_window.Dialog.child_window(title="Header File (.h)", auto_id="Header File (.h)",
                                      control_type="ListItem").wait(
            'ready',
            timeout=10).click_input()
        vs_window.Dialog.child_window(auto_id="txt_Name").wait(
            'ready',
            timeout=10).click_input(button="left", double=True)

        send_keys("msvc_defines.h")

        vs_window.Dialog.child_window(title="Add", auto_id="btn_OK", control_type="Button").wait(
            'ready', timeout=10).click_input(button="left", double=True)
        return True
    except Exception as e:
        logging.debug(e)
        return False


def adding_data_to_header_file():
    """
    This api will add data to header file with timestamp name taken from create project api
    :return: bool
    """
    try:
        project_location_config = conf['Installer Path']['hip_sdk_setup']
        project_location = os.path.abspath(project_location_config)
        with open("../../Tools/header_file.h") as f:
            with open(
                    rf"{project_location}\MatrixTranspose_Template_{timestamp}\MatrixTranspose_Template_{timestamp}\msvc_defines.h",
                    "w") as f1:
                for line in f:
                    f1.write(line)
        return True
    except Exception as e:
        logging.debug(e)
        logging.error("Failed to copy data from header_file.h file to header file")
        return False


def create_source_file():
    """
    This api will create a source file from scratch in the template project
    :return: bool
    """
    try:
        vs_window.Dialog.child_window(title="Source Files", control_type="TreeItem").wait(
            'ready',
            timeout=10).right_click_input()
        vs_window.Dialog.child_window(title="Add", control_type="MenuItem").wait(
            'ready',
            timeout=10).click_input()
        vs_window.Dialog.child_window(title="New Item...", control_type="MenuItem").wait(
            'ready',
            timeout=10).click_input()
        vs_window.Dialog.child_window(title="Installed", auto_id="Installed:ToggleButton",
                                      control_type="Button").wait(
            'ready',
            timeout=10).click_input()
        vs_window.Dialog.child_window(title="HIP File (.hip)", auto_id="HIP File (.hip)", control_type="ListItem").wait(
            'ready',
            timeout=10).click_input()
        vs_window.Dialog.child_window(auto_id="txt_Name").wait(
            'ready',
            timeout=10).click_input(button="left", double=True)

        # send_keys(f"MatrixTranspose_Template_{timestamp}.hip")
        send_keys("Matrix_Transpose_Template_source_file.hip")

        vs_window.Dialog.child_window(title="Add", auto_id="btn_OK", control_type="Button").wait(
            'ready',
            timeout=10).click_input(button="left", double=True)
        # vs_window.Dialog.child_window(title="Source Files", control_type="TreeItem").wait(
        #     'ready',
        #     timeout=10).click_input(button="left", double=True)
        logging.debug("Creating source file completed")
        return True
    except Exception as e:
        logging.debug(e)
        logging.error("Failed create source file")


def adding_data_to_source_file():
    """
    This api will add data to source file with timestamp name taken from create project api
    :return: bool
    """
    try:
        project_location_config = conf['Installer Path']['hip_sdk_setup']
        project_location = os.path.abspath(project_location_config)
        with open("../../Tools/source_file.hip") as f:
            with open(
                    rf"{project_location}\MatrixTranspose_Template_{timestamp}\MatrixTranspose_Template_{timestamp}\Matrix_Transpose_Template_source_file.hip",
                    "w") as f1:
                for line in f:
                    f1.write(line)
        return True
    except Exception as e:
        logging.debug(e)
        logging.debug("Failed to copy data from source_file.hip to source file")
        return False


def screenshot(request):
    """
    This api will take the snapshot of the screen and will store in the Reports folder
    :param request: It takes node name ( TC name ) as input
    """
    try:
        last_log_folder = os.listdir(r"..\..\Reports")[-1]
        logging.debug(f"Screenshot Timestamp is: {last_log_folder}")
        logging.info("ERROR SNAPSHOT HAS BEEN TAKEN")
        if not os.path.exists(rf'..\..\Reports\{last_log_folder}\Plugin_Error_Snapshots\{request}'):
            os.makedirs(rf'..\..\Reports\{last_log_folder}\Plugin_Error_Snapshots\{request}')
        pyautogui.screenshot(
            fr"..\..\Reports\{last_log_folder}\Plugin_Error_Snapshots\{request}\Error_Snapshot_for_test_case.png")
    except Exception as e:
        logging.error("Failed to take Snapshot - screenshot()")
        logging.exception(e)


def plugin_teardown():
    try:
        logging.debug("Teardown Process in progress. Removing all previous running instances of visual Studio")
        kill_process()
        time.sleep(10)  # Sleep time required to close all running instances
        logging.debug("Teardown Process Completed")

    except Exception as e:
        logging.error("plugin_teardown() - failed to close all instances")
        logging.exception(e)


# *******************************************************************************************************************
# *******************************************************************************************************************
# *******************************************************************************************************************
# *******************************************************************************************************************
# *******************************************************************************************************************
# TODO: Below api are not used, however might be used in future ( can be ignored for now )
#  ( not used anywhere in scripts )

def install_plugin_via_gui():
    Application().start(r'explorer.exe "C:\Program Files\AMD\ROCm\5.3\Visual Studio"')
    explorer = Application(backend="uia").connect(path="explorer.exe", title="Visual Studio")
    HIP = explorer.VisualStudio.ItemsView.get_item('HIPExtension2022.vsix')
    HIP.click_input()
    x, y = win32api.GetCursorPos()
    mouse.double_click(button='left', coords=(x, y))
    app_dialog = explorer.top_window()
    app_dialog.minimize()
    time.sleep(10)
    vsix_exe = Application(backend='win32').connect(path=rf"{conf['Plugins']['VSIXInstaller_exe_path']}",
                                                    timeout=UI_elements.click_timeout)
    app_dialog = vsix_exe.top_window()
    app_dialog.minimize()
    app_dialog.restore()
    app_dialog.set_focus()
    send_keys('E')
    time.sleep(1)
    send_keys('I')
    time.sleep(70)
    app_dialog.minimize()
    app_dialog.restore()
    app_dialog.set_focus()
    send_keys('C')
    logging.debug("validating the extension")


def uninstall_plugin_via_gui():
    vs_window = Application(backend="uia").start(
        r'"C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\devenv.exe"')
    vs_window.Dialog.child_window(title="Continue _without code", control_type="Text").wait('ready',
                                                                                            timeout=20).click_input()
    vs_window.Dialog.child_window(title="Extensions", control_type="MenuItem").wait('ready',
                                                                                    timeout=UI_elements.click_timeout).click_input()
    vs_window.Dialog.child_window(title="Manage Extensions", control_type="MenuItem", found_index=1). \
        wait('ready', timeout=UI_elements.click_timeout).click_input()
    vs_window.Dialog.child_window(auto_id="Installed").click_input()
    vs_window.Dialog.child_window(title="AMD HIP Toolchain [Preview] ", auto_id="AMD HIP Toolchain",
                                  control_type="ListItem").wait('ready',
                                                                timeout=UI_elements.click_timeout).click_input()
    vs_window.Dialog.child_window(title="_Uninstall", control_type="Text").wait('ready',
                                                                                timeout=UI_elements.click_timeout).click_input()
    vs_window.MicrosoftVisualStudio.child_window(title="Yes", auto_id="6", control_type="Button"). \
        wait('ready', timeout=UI_elements.click_timeout).click_input()
    vs_window.MicrosoftVisualStudio.child_window(auto_id="Button_CloseDialog").wait('ready',
                                                                                    timeout=UI_elements.click_timeout).click_input()
    vs_window.Dialog.child_window(auto_id="Close").wait('ready', timeout=UI_elements.click_timeout).click_input()
    time.sleep(3)
    vsix_exe = Application(backend='win32').connect(path=rf"{conf['Plugins']['VSIXInstaller_exe_path']}",
                                                    timeout=UI_elements.click_timeout)
    logging.debug("connecting to VSIX dialog success")
    app_dialog = vsix_exe.top_window()
    time.sleep(10)
    app_dialog.minimize()
    app_dialog.restore()
    app_dialog.set_focus()
    logging.debug("Focus set to VSIX dialog")
    send_keys('M')
    time.sleep(1)
    send_keys('E')
    time.sleep(70)
    logging.debug("Closing the VSIX dialog")
    app_dialog.minimize()
    app_dialog.restore()
    send_keys('C')
    logging.debug("Uninstallation from GUI Completed.")


def uninstall_plugin_via_cmd():
    try:
        logging.debug(f"{conf['Plugins']['VS_2022_installation_path']}" +
                      " /u:AMD_HIP_17.406c48f7-1987-4755-890b-5f849ffc2725")
        Application(backend='win32').start(
            cmd_line=rf"{conf['Plugins']['VS_2022_installation_path']}" +
                     " /u:AMD_HIP_17.406c48f7-1987-4755-890b-5f849ffc2725", timeout=UI_elements.click_timeout)
        vsix_uninstall_exe = Application(backend='win32').connect(path=rf"{conf['Plugins']['VSIXInstaller_exe_path']}",
                                                                  timeout=UI_elements.click_timeout)
        vsix_uninstall_exe.VSIXInstaller.set_focus()
        logging.debug("Uninstall query run success")

    except Exception as e:
        logging.error("Failed to execute uninstallation query, check visual studio path and GUI ID for same in"
                      " config.ini file and update accordingly")
        logging.exception(e)
        return False


def launch_plugin_installer():
    """
    This api will launch the vsix.exe file the VS installed path and HIP SDK Installation path using cmd
    :return bool
    """
    # cmd_line = r'"C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\VSIXInstaller.exe" /a /f
    # "C:\Program Files\AMD\ROCm\5.3\Visual Studio\HIPExtension2022.vsix"

    try:
        # Application(backend='win32').start(cmd_line=rf"{conf['Plugins']['VS_2022_installation_path']} /a /f
        # {conf['Installer Path']['Default_installation_path']}{version}\Visual Studio\HIPExtension2022.vsix",
        # timeout=UI_elements.launch_timeout)

        Application(backend='win32').start(
            cmd_line=rf"{conf['Plugins']['VS_2022_installation_path']}" +
                     " /a /f" + f" {conf['Installer Path']['Default_installation_path']}{version}" +
                     '\Visual Studio\HIPExtension2022.vsix"', timeout=UI_elements.click_timeout)

        global vsix_exe
        vsix_exe = Application(backend='win32').connect(path=rf"{conf['Plugins']['VSIXInstaller_exe_path']}",
                                                        timeout=UI_elements.click_timeout)
        vsix_exe.VSIXInstaller.set_focus()
        time.sleep(3)  # Default sleep time to launch the application
        app_dialog = vsix_exe.top_window()
        app_dialog.minimize()
        app_dialog.restore()
        app_dialog.set_focus()
        logging.debug("Launch of VSIX exe is Success")
        return True

    except Exception as e:
        logging.exception(e)
        logging.error("Something wrong in VSIX exe launch. Please verify Visual studio path and update accordingly"
                      " in config.ini file \n ")
        return False


def build_sample_application_check_all_logs_abhi_code():
    # TODO: No test case for this check. Future use
    try:
        vs_window.Dialog.child_window(title="Solution Configurations", auto_id="PART_FocusTarget",
                                      control_type="ComboBox").wait(
            'ready', timeout=20).click_input()
        vs_window.Dialog.child_window(title="Release", auto_id="Release", control_type="ListItem",
                                      found_index=0).wait('ready',
                                                          timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="View", control_type="MenuItem").wait('ready',
                                                                                  timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="Solution Explorer", control_type="MenuItem", found_index=0).wait(
            'ready',
            timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="HIP-Basic", control_type="TreeItem").wait('ready',
                                                                                       timeout=UI_elements.click_timeout).expand()
        text = vs_window.Dialog.child_window(title="dynamic_shared_vs2019 ‎(HIP_clang)",
                                             control_type="TreeItem").wrapper_object()
        logging.debug(f"this is the value from use clang ======>{text.legacy_properties()['Value']}")
        project_name = text.legacy_properties()['Value']
        vs_window.Dialog.child_window(title="dynamic_shared_vs2019 ‎(HIP_clang)", control_type="TreeItem").wait(
            'ready',
            #                                                                                                   timeout=UI_elements.click_timeout).right_click_input()
            # vs_window.Dialog.child_window(title="Solution 'ROCm-Examples-VS2019' ", control_type="TreeItem").wait('ready',
            timeout=UI_elements.click_timeout).right_click_input()

        vs_window.Dialog.child_window(title="Properties", control_type="MenuItem").wait('ready',
                                                                                        timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="Platform Toolset", control_type="TreeItem").wait('ready',
                                                                                              timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="Open", control_type="Button", found_index=0).wait('ready',
                                                                                               timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="AMD HIP for clang Compiler", control_type="ListItem").wait('ready',
                                                                                                        timeout=10).click_input()
        app_dialog = vs_window.top_window()
        app_dialog.minimize()
        app_dialog.restore()
        app_dialog.set_focus()

        try:
            vs_window.Dialog.child_window(title="Apply", auto_id="12321", control_type="Button").wait('ready',
                                                                                                      timeout=UI_elements.click_timeout).click_input()
            vs_window.Dialog.child_window(title="OK", auto_id="1", control_type="Button").wait('ready',
                                                                                               timeout=UI_elements.click_timeout).click_input()
        except:
            vs_window.Dialog.child_window(title="OK", auto_id="1", control_type="Button").wait('ready',
                                                                                               timeout=UI_elements.click_timeout).click_input()
        # vs_window.Dialog.child_window(title="dynamic_shared_vs2019 (HIP_clang)", control_type="TreeItem").wait('ready',
        #                                                                                                   timeout=UI_elements.click_timeout).right_click_input()

        time.sleep(3)
        vs_window.Dialog.child_window(title="dynamic_shared_vs2019 ‎(HIP_clang)", control_type="TreeItem").wait(
            'ready', timeout=UI_elements.click_timeout).right_click_input()
        vs_window.Dialog.child_window(title="Rebuild", control_type="MenuItem").wait('ready',
                                                                                     timeout=UI_elements.click_timeout).click_input()

        # time.sleep(30)
        vs_window.Dialog.child_window(title="Rebuild All succeeded", control_type="Text").wait('ready',
                                                                                               timeout=200).click_input()

        vs_window.Dialog.child_window(title="File", control_type="MenuItem").wait('ready',
                                                                                  timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="Save Output As...", control_type="MenuItem").wait('ready',
                                                                                               timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="All locations", control_type="SplitButton").wait('ready',
                                                                                              timeout=UI_elements.click_timeout).click_input()
        path = os.getcwd()
        logging.debug(path)
        os.chdir('..\..\Reports')
        logging.debug(path)
        path = os.getcwd()
        send_keys(path)
        send_keys('{ENTER}')
        vs_window.Dialog.child_window(title="Save", auto_id="1", control_type="SplitButton").wait('ready',
                                                                                                  timeout=UI_elements.click_timeout).click_input()
        try:
            vs_window.Dialog.child_window(title="Yes", control_type="Button").wait('ready',
                                                                                   timeout=UI_elements.click_timeout).click()
            logging.debug("Overwriting old output file")
        except Exception:
            logging.debug("creating a new output file")
        fullpath = path + "\Output-Build.txt"
        file1 = open(fullpath, "r+")

        data = file1.read()
        # logging.debug(data)
        logging.debug(project_name)
        new_file = project_name.replace("(HIP_clang)", '.exe')
        new_file2 = new_file.replace(" ", "")
        new_file3 = new_file2.replace("‎", "")
        logging.debug(new_file3)
        if new_file3 in data:
            logging.debug(f"the build successful for this project=====> {new_file3}")
            return True
        else:
            logging.debug("BUILD FAILED!!!!!")
        vs_window.Dialog.child_window(title="Close", control_type="Button", auto_id="Close").click()

    except Exception as e:
        logging.exception(e)
        logging.error("Failed to Build Sample application project using Clang Compiler")
        return False


def build_one_sample_application_clang():
    # TODO: No test cases for this api. Future use
    try:
        vs_window.Dialog.child_window(title="Solution Configurations", auto_id="PART_FocusTarget",
                                      control_type="ComboBox").wait(
            'ready', timeout=20).click_input()
        vs_window.Dialog.child_window(title="Release", auto_id="Release", control_type="ListItem",
                                      found_index=0).wait('ready',
                                                          timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="View", control_type="MenuItem").wait('ready',
                                                                                  timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="Solution Explorer", control_type="MenuItem", found_index=0).wait(
            'ready',
            timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="HIP-Basic", control_type="TreeItem").wait('ready',
                                                                                       timeout=UI_elements.click_timeout).expand()
        vs_window.Dialog.child_window(title="dynamic_shared_vs2019 ‎(HIP_clang)", control_type="TreeItem").wait(
            'ready',
            timeout=UI_elements.click_timeout).right_click_input()
        # vs_window.Dialog.child_window(title="Solution 'ROCm-Examples-VS2019' ‎", control_type="TreeItem").wait('ready',
        #                                                                                                   timeout=UI_elements.click_timeout).right_click_input()
        vs_window.Dialog.child_window(title="Properties", control_type="MenuItem").wait('ready',
                                                                                        timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="Platform Toolset", control_type="TreeItem").wait('ready',
                                                                                              timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="Open", control_type="Button", found_index=0).wait('ready',
                                                                                               timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="AMD HIP for clang Compiler", control_type="ListItem").wait('ready',
                                                                                                        timeout=UI_elements.click_timeout).click_input()
        try:
            vs_window.Dialog.child_window(title="Apply", auto_id="12321", control_type="Button").wait('ready',
                                                                                                      timeout=UI_elements.click_timeout).click_input()
            vs_window.Dialog.child_window(title="OK", auto_id="1", control_type="Button").wait('ready',
                                                                                               timeout=UI_elements.click_timeout).click_input()
        except:
            vs_window.Dialog.child_window(title="OK", auto_id="1", control_type="Button").wait('ready',
                                                                                               timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="dynamic_shared_vs2019 ‎(HIP_clang)", control_type="TreeItem").wait(
            'ready',
            timeout=UI_elements.click_timeout).right_click_input()
        # vs_window.Dialog.child_window(title="Solution 'ROCm-Examples-VS2019' ‎", control_type="TreeItem").wait('ready',
        #                                                                                                   timeout=UI_elements.click_timeout).right_click_input()

        vs_window.Dialog.child_window(title="Rebuild", control_type="MenuItem").wait('ready',
                                                                                     timeout=UI_elements.click_timeout).click_input()

        # time.sleep(30)
        vs_window.Dialog.child_window(title="Rebuild All succeeded", control_type="Text").wait('ready',
                                                                                               timeout=200).click_input()
        # vs_window.Dialog.print_control_identifiers()
        generated_log_path = ""
        directory = conf['Installer Path']['hip_sdk_setup']
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename == f"dynamic_shared_vs2019.log" and "Debug" not in root:
                    logging.debug(f"generated log file path : {os.path.join(root, filename)}")
                    generated_log_path = os.path.join(root, filename)

        # f = open(rf"C:/HIP_SDK_Setup.log", "r")
        f = open(generated_log_path, "r")

        if f"dynamic_shared_vs2019.exe" in f.read():
            if ': error :' not in f.read():
                logging.debug("Sample application build succeeded WITHOUT ERRORS")
                return True
        vs_window.Dialog.child_window(title="Close", control_type="Button", auto_id="Close").click()
    except Exception as e:
        logging.exception(e)
        logging.error("Failed to Build Sample application project using Clang Compiler")
        return False


def build_all_sample_applications_old():
    try:
        logging.debug("Building all sln files under ROCm examples")
        vs_window.Dialog.child_window(title="Solution Configurations", auto_id="PART_FocusTarget",
                                      control_type="ComboBox").wait(
            'ready', timeout=20).click_input()
        vs_window.Dialog.child_window(title="Release", auto_id="Release", control_type="ListItem",
                                      found_index=0).wait('ready',
                                                          timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="View", control_type="MenuItem").wait('ready',
                                                                                  timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="Solution Explorer", control_type="MenuItem", found_index=0).wait(
            'ready',
            timeout=UI_elements.click_timeout).click_input()
        vs_window.Dialog.child_window(title="HIP-Basic", control_type="TreeItem").wait('ready',
                                                                                       timeout=UI_elements.click_timeout).expand()
        # vs_window.Dialog.child_window(title="dynamic_shared_vs2019 ‎(HIP_clang)", control_type="TreeItem").wait('ready',
        #                                                                                                   timeout=UI_elements.click_timeout).right_click_input()
        vs_window.Dialog.child_window(title="Solution 'ROCm-Examples-VS2019' ‎", control_type="TreeItem").wait(
            'ready',
            timeout=UI_elements.click_timeout).right_click_input()

        vs_window.Dialog.child_window(title="Rebuild Solution", control_type="MenuItem").wait('ready',
                                                                                              timeout=20).click_input()

        # time.sleep(30)
        vs_window.Dialog.child_window(title="Rebuild All succeeded", control_type="Text").wait('ready',
                                                                                               timeout=200).click_input()
        logging.debug("building all examples Completed successfully")

        check_each_project_log()

        vs_window.Dialog.child_window(title="Close", control_type="Button", auto_id="Close").click()
    except Exception as e:
        logging.exception(e)
        logging.error("Failed to Build Sample application project using Clang Compiler")
        return False


def check_each_project_log():
    # TODO: No test case for each log. Future use
    generated_log_path = []
    names = []
    # error_flag=0
    directory = conf['Installer Path']['hip_sdk_setup']
    logging.debug("Checking logs for all solutions build")
    for root, dirs, files in os.walk(os.path.join(directory, "rocm-examples")):
        for filename in files:
            if filename.endswith(".sln"):
                logging.debug(f"generated log file path : {os.path.join(root, filename)}")
                generated_log_path.append(os.path.join(root, filename))
                a = filename.replace(".sln", "")
                names.append(a)
                if filename != "ROCm-Examples-VS2019.sln":
                    f = open(os.path.join(root, "Release", filename.replace(".sln", ".log")), "r")
                    logging.debug("opening the file")
                    if filename.replace(".sln", ".exe") in f.read():
                        logging.debug(".exe check done")
                        if ': error :' not in f.read():
                            logging.debug(f"Sample application {filename} build succeeded WITHOUT ERRORS\n\n")
                            return True

# def sample_application_folder_expand(compiler):
#     visiblity_timeout = 2
#     vs_window.Dialog.child_window(title="HIP-Basic", control_type="TreeItem").wait('ready',
#                                                                                    timeout=UI_elements.click_timeout).expand()
#     try:
#         vs_window.Dialog.child_window(title=f"dynamic_shared_vs2019 ‎({compiler})", control_type="TreeItem").wait(
#             'ready',
#             timeout=visiblity_timeout).verify_visible()
#         logging.debug("verifying dynamic shared successfully.....")
#     except Exception:
#         vs_window.Dialog.child_window(title_re="^dynamic_shared_vs2019.*", control_type="TreeItem").wait(
#             'ready',
#             timeout=UI_elements.click_timeout).right_click_input()
#         change_compiler(compiler)
#         logging.debug("changing compiler is successfully in dynamic_shared_vs2019.....")
#     try:
#         vs_window.Dialog.child_window(title=f"device_query_vs2019 ‎({compiler})", control_type="TreeItem").wait(
#             'ready',
#             timeout=visiblity_timeout).verify_visible()
#         logging.debug("verifying device_query_vs2019 successfully.....")
#     except Exception:
#         vs_window.Dialog.child_window(title_re="^device_query_vs2019.*", control_type="TreeItem").wait(
#             'ready',
#             timeout=UI_elements.click_timeout).right_click_input()
#         change_compiler(compiler)
#         logging.debug("changing compiler is successfully in device_query_vs2019.....")
#     try:
#         vs_window.Dialog.child_window(title=f"events_vs2019 ‎({compiler})", control_type="TreeItem").wait(
#             'ready',
#             timeout=visiblity_timeout).verify_visible()
#         logging.debug("verifying events_vs2019 successfully.....")
#
#     except Exception:
#         vs_window.Dialog.child_window(title_re="^events_vs2019.*", control_type="TreeItem").wait(
#             'ready',
#             timeout=UI_elements.click_timeout).right_click_input()
#         change_compiler(compiler)
#         logging.debug("changing compiler is successfully in events_vs2019.....")
#     try:
#         vs_window.Dialog.child_window(title=f"matrix_multiplication_vs2019 ‎({compiler})",
#                                       control_type="TreeItem").wait(
#             'ready',
#             timeout=visiblity_timeout).verify_visible()
#         logging.debug("verifying matrix_multiplication_vs2019 successfully.....")
#     except Exception:
#         vs_window.Dialog.child_window(title_re="^matrix_multiplication_vs2019.*",
#                                       control_type="TreeItem").wait(
#             'ready',
#             timeout=UI_elements.click_timeout).right_click_input()
#         change_compiler(compiler)
#         logging.debug("changing compiler is successfully  in matrix_multiplication_vs2019 .....")
#     try:
#         vs_window.Dialog.child_window(title=f"occupancy_vs2019 ‎({compiler})", control_type="TreeItem").wait(
#             'ready',
#             timeout=visiblity_timeout).verify_visible()
#         logging.debug("verifying occupancy_vs2019 successfully.....")
#     except Exception:
#         vs_window.Dialog.child_window(title_re="^occupancy_vs2019.*", control_type="TreeItem").wait(
#             'ready',
#             timeout=UI_elements.click_timeout).right_click_input()
#         change_compiler(compiler)
#         logging.debug("changing compiler is successfully in  occupancy_vs2019 .....")
#
#     # try:
#     #     vs_window.Dialog.child_window(title=f"saxpy_vs2019 ‎({compiler})", control_type="TreeItem").wait(
#     #         'ready',
#     #         timeout=visiblity_timeout).verify_visible()
#     #     logging.debug("verifying saxpy_vs2019 successfully.....")
#     # except Exception:
#     #     vs_window.Dialog.child_window(title_re="^saxpy_vs2019.*", control_type="TreeItem").wait(
#     #         'ready',
#     #         timeout=UI_elements.click_timeout).right_click_input()
#     #     change_compiler(compiler)
#     #     logging.debug("changing compiler is successfully  in saxpy_vs2019 .....")
#
#     try:
#         vs_window.Dialog.child_window(title=f"streams_vs2019 ‎({compiler})", control_type="TreeItem",
#                                       found_index=0).wait(
#             'ready',
#             timeout=visiblity_timeout).verify_visible()
#         logging.debug("verifying streams_vs2019 successfully.....")
#         logging.debug("Building all sln files under ROCm examples=====1")
#     except Exception:
#         vs_window.Dialog.child_window(title_re="^streams_vs2019.*", control_type="TreeItem", found_index=0).wait(
#             'ready',
#             timeout=UI_elements.click_timeout).right_click_input()
#         change_compiler(compiler)
#         logging.debug("changing compiler is successfully in streams_vs2019  .....")
#     vs_window.Dialog.child_window(title="Libraries", control_type="TreeItem").wait('ready',
#                                                                                    timeout=UI_elements.click_timeout).expand()
#     logging.debug("expanding libraries directory successfully....")
#     vs_window.Dialog.child_window(title="exampleLibraryTemplate", control_type="TreeItem").wait('ready',
#                                                                                                 timeout=UI_elements.click_timeout).expand()
#     logging.debug("expanding exampleLibraryTemplate directory successfully....")
#     vs_window.Dialog.child_window(title="hipCUB", control_type="TreeItem").wait('ready',
#                                                                                 timeout=UI_elements.click_timeout).expand()
#     logging.debug("expanding hipCUB directory successfully....")
#     vs_window.Dialog.child_window(title="rocPRIM", control_type="TreeItem").wait('ready',
#                                                                                  timeout=UI_elements.click_timeout).expand()
#     logging.debug("expanding rocPRIM directory successfully....")
#     vs_window.Dialog.child_window(title="rocRAND", control_type="TreeItem").wait('ready',
#                                                                                  timeout=UI_elements.click_timeout).expand()
#     logging.debug("expanding rocRAND directory successfully....")
#     vs_window.Dialog.child_window(title="rocThrust", control_type="TreeItem").wait('ready',
#                                                                                    timeout=UI_elements.click_timeout).expand()
#     logging.debug("expanding rocThrust directory successfully....")
#     try:
#         vs_window.Dialog.child_window(title=f"example_template_vs2019 ‎({compiler})", control_type="TreeItem").wait(
#             'ready',
#             timeout=visiblity_timeout).verify_visible()
#         logging.debug("verifying example_template_vs2019 successfully.....")
#     except Exception:
#         vs_window.Dialog.child_window(title_re="^example_template_vs2019.*", control_type="TreeItem").wait(
#             'ready',
#             timeout=UI_elements.click_timeout).right_click_input()
#         change_compiler(compiler)
#         logging.debug("changing compiler is successfully  in example_template_vs2019 .....")
#     try:
#         vs_window.Dialog.child_window(title=f"device_radix_sort_vs2019 ‎({compiler})", control_type="TreeItem").wait(
#             'ready',
#             timeout=visiblity_timeout).verify_visible()
#         logging.debug("verifying device_radix_sort_vs2019 successfully.....")
#     except Exception:
#         vs_window.Dialog.child_window(title_re="^device_radix_sort_vs2019.*", control_type="TreeItem").wait(
#             'ready',
#             timeout=UI_elements.click_timeout).right_click_input()
#         change_compiler(compiler)
#         logging.debug("changing compiler is successfully  in device_radix_sort_vs2019 .....")
#
#     # TODO: Two sln with same name device sum
#     # try:
#     #     vs_window.Dialog.child_window(title=f"device_sum_vs2019 ‎({compiler})", control_type="TreeItem").wait(
#     #         'ready',
#     #         timeout=visiblity_timeout).verify_visible()
#     #     logging.debug("verifying device_sum_vs2019 successfully.....")
#     # except Exception:
#     #     vs_window.Dialog.child_window(title_re="^device_sum_vs2019.*", control_type="TreeItem").wait(
#     #         'ready',
#     #         timeout=UI_elements.click_timeout).right_click_input()
#     #     change_compiler(compiler)
#     #     logging.debug("changing compiler is successfully  in device_sum_vs2019 .....")
#
#
#     try:
#         vs_window.Dialog.child_window(title=f"block_sum_vs2019 ‎({compiler})", control_type="TreeItem").wait(
#             'ready',
#             timeout=visiblity_timeout).verify_visible()
#         logging.debug("verifying block_sum_vs2019 successfully.....")
#     except Exception:
#         vs_window.Dialog.child_window(title_re="^block_sum_vs2019.*", control_type="TreeItem").wait(
#             'ready',
#             timeout=UI_elements.click_timeout).right_click_input()
#         change_compiler(compiler)
#         logging.debug("changing compiler is successfully  in block_sum_vs2019 .....")
#
#     # try:
#     #     vs_window.Dialog.child_window(title=f"device_sum_vs2019 ‎({compiler})", control_type="TreeItem",
#     #                                   found_index=0).wait(
#     #         'ready',
#     #         timeout=visiblity_timeout).verify_visible()
#     #     logging.debug("verifying device_sum_vs2019 successfully.....")
#     # except Exception:
#     #     vs_window.Dialog.child_window(title_re="^device_sum_vs2019.*", control_type="TreeItem", found_index=0).wait(
#     #         'ready',
#     #         timeout=UI_elements.click_timeout).right_click_input()
#     #     change_compiler(compiler)
#     #     logging.debug("changing compiler is successfully  in device_sum_vs2019 .....")
#
#     try:
#         vs_window.Dialog.child_window(title=f"simple_distributions_cpp_vs2019 ‎({compiler})",
#                                       control_type="TreeItem").wait(
#             'ready',
#             timeout=visiblity_timeout).verify_visible()
#         logging.debug("verifying simple_distributions_cpp_vs2019 successfully.....")
#     except Exception:
#         vs_window.Dialog.child_window(title_re="^simple_distributions_cpp_vs2019.*", control_type="TreeItem").wait(
#             'ready',
#             timeout=UI_elements.click_timeout).right_click_input()
#         change_compiler(compiler)
#         logging.debug("changing compiler is successfully  in simple_distributions_cpp_vs2019 .....")
#     try:
#         vs_window.Dialog.child_window(title=f"device_ptr_vs2019 ‎({compiler})", control_type="TreeItem").wait(
#             'ready',
#             timeout=visiblity_timeout).verify_visible()
#         logging.debug("verifying device_ptr_vs2019 successfully.....")
#     except Exception:
#         vs_window.Dialog.child_window(title_re="^device_ptr_vs2019.*", control_type="TreeItem").wait(
#             'ready',
#             timeout=UI_elements.click_timeout).right_click_input()
#         change_compiler(compiler)
#         logging.debug("changing compiler is successfully  in device_ptr_vs2019 .....")
#     try:
#         vs_window.Dialog.child_window(title=f"norm_vs2019 ‎({compiler})", control_type="TreeItem").wait(
#             'ready',
#             timeout=visiblity_timeout).verify_visible()
#         logging.debug("verifying norm_vs2019 successfully.....")
#     except Exception:
#         vs_window.Dialog.child_window(title_re="^norm_vs2019.*", control_type="TreeItem").wait(
#             'ready',
#             timeout=UI_elements.click_timeout).right_click_input()
#         change_compiler(compiler)
#         logging.debug("changing compiler is successfully  in norm_vs2019 .....")
#     try:
#         vs_window.Dialog.child_window(title=f"reduce_sum_vs2019 ‎({compiler})", control_type="TreeItem").wait(
#             'ready',
#             timeout=visiblity_timeout).verify_visible()
#         logging.debug("verifying reduce_sum_vs2019 successfully.....")
#     except Exception:
#         vs_window.Dialog.child_window(title_re="^reduce_sum_vs2019.*", control_type="TreeItem").wait(
#             'ready',
#             timeout=UI_elements.click_timeout).right_click_input()
#         change_compiler(compiler)
#         logging.debug("changing compiler is successfully  in reduce_sum_vs2019 .....")
#     try:
#         vs_window.Dialog.child_window(title=f"remove_points_vs2019 ‎({compiler})", control_type="TreeItem",
#                                       found_index=0).wait(
#             'ready',
#             timeout=visiblity_timeout).verify_visible()
#         logging.debug("verifying remove_points_vs2019 successfully.....")
#     except Exception:
#         vs_window.Dialog.child_window(title_re="^remove_points_vs2019.*", control_type="TreeItem", found_index=0).wait(
#             'ready',
#             timeout=UI_elements.click_timeout).right_click_input()
#         change_compiler(compiler)
#         logging.debug("changing compiler is successfully  in remove_points_vs2019 .....")
#
#     # TODO: Saxpy has two files with same name
#
#     # try:
#     #     vs_window.Dialog.print_control_identifiers()
#     #
#     #     vs_window.Dialog.child_window(title=f"saxpy_vs2019 ‎({compiler})", control_type="TreeItem", found_index=2).wait(
#     #         'ready',
#     #         timeout=visiblity_timeout).verify_visible()
#     #     logging.debug("verifying saxpy_vs2019 successfully.....")
#     # except Exception:
#     #     vs_window.Dialog.child_window(title="^saxpy_vs2019.*", control_type="TreeItem", found_index=2).wait(
#     #         'ready',
#     #         timeout=UI_elements.click_timeout).right_click_input()
#     #     change_compiler(compiler)
#     #     logging.debug("changing compiler is successfully  in saxpy_vs2019 .....")
#
#     try:
#         vs_window.Dialog.child_window(title=f"vectors_vs2019 ‎({compiler})", control_type="TreeItem").wait(
#             'ready',
#             timeout=visiblity_timeout).verify_visible()
#         logging.debug("verifying vectors_vs2019 successfully.....")
#         logging.debug("Building all sln files under ROCm examples====2")
#     except Exception:
#         vs_window.Dialog.child_window(title_re="^vectors_vs2019.*", control_type="TreeItem").wait(
#             'ready',
#             timeout=UI_elements.click_timeout).right_click_input()
#         change_compiler(compiler)
#         logging.debug("changing compiler is successfully  in vectors_vs2019 .....")
