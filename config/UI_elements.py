"""
UI_elements.py file has all the UI elements unique names, and default timeouts for click and app launch operation
"""

from library.application_info import ui_sdk_version

# All Buttons
cancel_button = "Cancel"
Install = "Install"
yes = "Yes Quit"
no = "No"
Finish = "Finish"
Restart = "Restart"
close = "close"
minimize = "minimize"
amd_logo = "AMD Logo"
browse = "Install Details_$_Browse"

# Select / deSelect button
select_all = "Install Details_$_HIP Select All"
deselect_all = "Install Details_$_HIP DeselectAll"

# HIP SDK Core additional options button
hip_sdk_core_additional = "Install Details_$_SDK Core Additional Options "

# HIP Libraries UI elements
hip_lib_checkbox_full = "Install Details_$_HIP Libraries_$_Full_$_Install All Components"
hip_lib_checkbox_partial = "Install Details_$_HIP Libraries_$_Partial_$_Install(Some Component)"
hip_lib_checkbox_none = "Install Details_$_HIP Libraries_$_None_$_Skip(Do not Install)"
hip_lib_rt_true = f"Install Details_$_HIP Libraries Runtime _$_{ui_sdk_version()}_$_true"
hip_lib_rt_false = f"Install Details_$_HIP Libraries Runtime _$_{ui_sdk_version()}_$_false"
hip_lib_dev_true = f"Install Details_$_HIP Libraries Development (Libs, and headers)_$_{ui_sdk_version()}_$_true"
hip_lib_dev_false = f"Install Details_$_HIP Libraries Development (Libs, and headers)_$_{ui_sdk_version()}_$_false"
hip_lib_additional = "Install Details_$_HIP Libraries Additional Options "

# HIP Runtime Compiler UI elements
hip_rtc_checkbox_full = "Install Details_$_HIP Runtime Compiler_$_Full_$_Install All Components"
hip_rtc_checkbox_partial = "Install Details_$_HIP Runtime Compiler_$_Partial_$_Install(Some Component)"
hip_rtc_checkbox_none = "Install Details_$_HIP Runtime Compiler_$_None_$_Skip(Do not Install)"
hip_rtc_runtime_true = f"Install Details_$_HIP RTC Runtime _$_{ui_sdk_version()}_$_true"
hip_rtc_runtime_false = f"Install Details_$_HIP RTC Runtime _$_{ui_sdk_version()}_$_false"
hip_rtc_dev_true = f"Install Details_$_HIP RTC Development(Headers) _$_{ui_sdk_version()}_$_true"
hip_rtc_dev_false = f"Install Details_$_HIP RTC Development(Headers) _$_{ui_sdk_version()}_$_false"
hip_rtc_additional = "Install Details_$_HIP RTC Additional Options "

# HIP Ray Tracing UI elements
hip_ray_tracing_checkbox_full = "Install Details_$_HIP Ray Tracing_$_Full_$_Install All Components"
hip_ray_tracing_checkbox_partial = "Install Details_$_HIP Ray Tracing_$_Partial_$_Install(Some Component)"
hip_ray_tracing_checkbox_none = "Install Details_$_HIP Ray Tracing_$_None_$_Skip(Do not Install)"
hip_ray_tracing_runtime_true = f"Install Details_$_HIP RayTracing RunTime _$_{ui_sdk_version()}_$_true"
hip_ray_tracing_runtime_false = f"Install Details_$_HIP RayTracing RunTime _$_{ui_sdk_version()}_$_false"
hip_ray_tracing_runtime_Header_true = f"Install Details_$_HIP RayTracing Runtime  (Headers)_$_{ui_sdk_version()}_$_true"
hip_ray_tracing_runtime_Header_false = f"Install Details_$_HIP RayTracing Runtime  (Headers)_$_{ui_sdk_version()}_$_false"
hip_ray_tracing_additional_options = "Install Details_$_HIP RayTrace Additional Options "

# BitCode UI elements
bitcode_checkbox_full = "Install Details_$_BitCode Profiler_$_Full_$_Install All Components"
bitcode_checkbox_none = "Install Details_$_BitCode Profiler_$_None_$_Skip(Do not Install)"
bitcode_runtime_true = f"Install Details_$_HIP Bitcode Runtime _$_{ui_sdk_version()}_$_true"
bitcode_runtime_false = f"Install Details_$_HIP Bitcode Runtime _$_{ui_sdk_version()}_$_false"
bitcode_additional_options = "Install Details_$_HIP BitCode Additional Options "

# HIP Visual studio Plugin UI elements
# vs_checkbox_full = "Install Details_$_Visual Studio_$_Full_$_Install All Components"
vs_checkbox_full = "Install Details_$_Visual Studio (No Redistribution)_$_Full_$_Install All Components"
vs_checkbox_partial = "Install Details_$_Visual Studio (No Redistribution)_$_Partial_$_Install(Some Component)"
vs_checkbox_none = "Install Details_$_Visual Studio (No Redistribution)_$_None_$_Skip(Do not Install)"
vs_2017_plugin_true = f"Install Details_$_HIP SDK  Visual Studio 2017 Plugin_$_{ui_sdk_version()}_$_true"
vs_2017_plugin_false = f"Install Details_$_HIP SDK  Visual Studio 2017 Plugin_$_{ui_sdk_version()}_$_false"
vs_2019_plugin_true = f"Install Details_$_HIP SDK  Visual Studio 2019 Plugin_$__$_{ui_sdk_version()}true"
vs_2019_plugin_false = f"Install Details_$_HIP SDK  Visual Studio 2019 Plugin_$__$_{ui_sdk_version()}false"
vs_2022_plugin_true = f"Install Details_$_HIP SDK  Visual Studio 2022 Plugin_$__$_{ui_sdk_version()}true"
vs_2022_plugin_false = f"Install Details_$_HIP SDK  Visual Studio 2022 Plugin_$__$_{ui_sdk_version()}false"
vs_additional_options = "Install Details_$_HIP VS Additional Options "

# Driver installation UI elements
driver_combobox_when_dontInstall_no_driver = "DriverType_0_$_Comboboxitem_Don't Install_$_"
driver_combobox_when_dontInstall_downgraded_driver = "DriverType_0_$_Comboboxitem_Don't Install_$_Install (Upgrade)"
driver_combobox_when_dontInstall = "DriverType_0_$_Comboboxitem_Don't Install_$_Install (Repair)"
driver_combobox_when_dontInstall_upgraded_driver = "DriverType_0_$_Comboboxitem_Don't Install_$_Install (Downgrade)"

# driver_combobox = "DriverType_0_$_Combobox"
driver_combobox_when_Install = "DriverType_0_$_Comboboxitem_Install_$_undefined"
install_list_item = "DriverType_1_$_Listitem_Install"
dont_install_list_item = "DriverType_0_$_Listitem_Don't Install"

factory_reset_additional = "Install Details_$_Additional Options"

full_install_combo_box = "InstallType_$_Comboboxitem_Full Install"
full_install = "InstallType_$_Listitem_Full Install"
minimal_install_combo_box = "InstallType_$_Comboboxitem_Minimal Install"
minimal_install = "InstallType_$_Listitem_Minimal Install"
driver_only_combo_box = "InstallType_$_Comboboxitem_Driver Only"
driver_only_install = "InstallType_$_Listitem_Driver Only"

factory_reset_checkbox_false = "Install Details_$_Factory Reset_$_false"
factory_reset_checkbox_true = "Install Details_$_Factory Reset_$_true"

# License Agreement
license_agreement_link = "EULA"
license_agreement_link_done = "Eula_$_undefined"

# Installation Complete
installation_complete_screen = "Installation Complete_$_FinalState_$_true"
signup_for_newsletter = "Install Finish Screen _$_Stay upto date_$_Stay up to date on the latest news from AMD HIP SDKSign up to our newsletter"

# Installation names as per Control Panel
name_hip_sdk_core = 'HIP SDK Core'
name_hip_libraries_runtime = 'HIP SDK Libraries Runtime'
name_hip_libraries_development = 'HIP SDK Libraries Development'
name_hip_sdk_runtime_compiler_runtime = 'HIP SDK Runtime Compiler Runtime'
name_hip_sdk_runtime_compiler_development = 'HIP SDK Runtime Compiler Development'
name_hip_sdk_profiler = 'HIP SDK Profiler'
name_hip_ray_tracing_runtime = 'HIP SDK Ray Tracing Runtime'
name_hip_ray_tracing_runtime_header_development = 'HIP SDK Ray Tracing Development'
name_vs_2017 = 'HIP SDK Visual Studio 2017 Plugin'
name_vs_2019 = 'HIP SDK Visual Studio 2019 Plugin'
name_vs_2022 = 'HIP SDK Visual Studio 2022 Plugin'
name_AMD_drivers = 'AMD Software'

# Uninstallation names
uninstall_hip_sdk_core = "name = 'HIP SDK Core'"
uninstall_hip_libraries_runtime = "name = 'HIP SDK Libraries Runtime'"
uninstall_hip_libraries_development = "name = 'HIP SDK Libraries Development'"
uninstall_hip_sdk_runtime_compiler_runtime = "name = 'HIP SDK Runtime Compiler Runtime'"
uninstall_hip_sdk_runtime_compiler_development = "name = 'HIP SDK Runtime Compiler Development'"
uninstall_hip_sdk_profiler = "name = 'HIP SDK Profiler'"
uninstall_hip_ray_tracing_runtime = "name = 'HIP SDK Ray Tracing Runtime'"
uninstall_hip_ray_tracing_runtime_header_development = "name = 'HIP SDK Ray Tracing Development'"
uninstall_vs_2017 = "name = 'HIP SDK Visual Studio 2017 Plugin'"
uninstall_vs_2019 = "name = 'HIP SDK Visual Studio 2019 Plugin'"
uninstall_vs_2022 = "name = 'HIP SDK Visual Studio 2022 Plugin'"
uninstall_AMD_drivers = "name = 'AMD Software'"

# Control Types
button = "Button"
combo_box = "ComboBox"

# Timeouts
launch_timeout = 120
connect_timeout = 180
click_timeout = 10
finish_timeout = 750
build_timeout = 30

# Architecture
configuration_arch_list = ["gfx1031;gfx1032;gfx1100;gfx1102;gfx1030"]
# "gfx900", "gfx90a", "gfx906", "gfx908", "gfx1030"
