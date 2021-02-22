import subprocess
import optparse
import re
def get_arguments():

    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface you want to change")
    parser.add_option("-m", "--mac", dest="new_mac", help="New Mac address")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify the interface.")
    elif not options.new_mac:
        parser.error("[-] Please specify new mac address.")
    return options

def change_mac(interface, new_mac):
    print("[+] Changing Mac address interface "+ interface+" to "+new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)

options = get_arguments()
current_mac = get_current_mac(options.interface)
if current_mac:
    print("Current MAC = ", str(current_mac))
    change_mac(options.interface, options.new_mac)
else:
    print("[-] Cloud not read Mac address")
