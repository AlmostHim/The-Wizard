import random
import json
import pyperclip
import tkinter as tk

#Device Commands
IOS_XE_commands = "\nip ftp source-interface g0/0 \nip tftp source-interface g0/0 \nno ip domain lookup \nline vty 0 15 \nlogging sync \nexit \nint g0/0   \nip add dhcp  \nno shut \nip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 " 
Nexus_commands = '\nip ftp source-interface mgmt0 \nip tftp source-interface mgmt0  \nint mgmt0   \nip add dhcp  \nno shut  \nvrf member management \nvrf context management \nip route 0.0.0.0 0.0.0.0 '
Non_VRF_BB = '\nip ftp source-interface gi0/1 \nip tftp source-interface gi0/1 \nno ip domain lookup \nline vty 0 15 \nlogging sync \nexit \nint vlan 1 \nip add dhcp \nno shut \nint g0/1 \nno shut \nsw \nsw mode access \nsw access vlan 1 \nexit \nip route 0.0.0.0 0.0.0.0 '
ISR_commands = "\nip ftp source-interface g0 \nip tftp source-interface g0 \nno ip domain lookup \nline vty 0 15 \nlogging sync \nexit \nint g0   \nip add dhcp  \nno shut \nip route vrf Mgmt-intf 0.0.0.0 0.0.0.0 " 

def Wizard(family, row, hostname):
    output = ''
    #Device Command Determinations
    if family == "IOS_XE":
        output += 'conf t \nhostname ' + hostname + IOS_XE_commands

    elif family == 'Nexus9K/3K':
        output += 'conf t \nhostname ' + hostname + Nexus_commands

    elif family == 'NonVRFBB':
        output += 'conf t \nhostname ' + hostname + Non_VRF_BB

    elif family == 'ISR':
        output += 'conf t \nhostname ' + hostname + ISR_commands

    else:
        output += "Input a correct device family you weezo."
    
    
    #Row Gateway Calulations
    if row in ('1A', '2A'):
        output += "10.122.160.1"

    elif row in ('1B', '2B'):
        output += "10.122.160.129"

    elif row in ('3A', '4A'):
        output += "10.122.161.1"

    elif row in ('3B' , '4B'):
        output += "10.122.161.129"

    elif row in ('5A' , '6A'):
        output += "10.122.162.1"

    elif row in ('5B' , '6B'):
        output += "10.122.162.129"

    elif row in ('7A' , '8A'):
        output += "10.122.163.1"

    elif row in ('7B' , '8B'):
        output += "10.122.163.129"

    elif row in ('9A' , '10A'):
        output += "10.122.164.1"

    elif row in ('9B' , '10B'):
        output += "10.122.164.129"

    elif row in ('11A' , '12A'):
        output += "10.122.165.1"

    elif row in ('11B' , '12B'):
        output += "10.122.165.129"

    elif row in ('13A' , '14A'):
        output += "10.122.166.1"

    elif row in ('13B' , '14B'):
        output += "10.122.166.129"

    elif row in ('15A' , '16A'):
        output += "10.122.167.1"

    elif row in ('15B' , '16B'):
        output += "10.122.167.129"

    elif row in ('21A' , '22A'):
        output += "10.122.176.1"

    elif row in ('23A' , '24A'):
        output += "10.122.176.129"

    elif row in ('25A' , '26A'):
        output += "10.122.177.1"

    else:
        output += "\nEither the row hasn't been defined yet or you inputted an incorrect row. You weezo."

    output += '\nend \ncopy run start'

    pyperclip.copy(output)  # Copy the output to the clipboard
    print(output)  # Print the output

def handle_button_click():
    family = family_var.get()
    row = row_var.get()
    hostname = hostname_entry.get()
    Wizard(family, row, hostname)

# Create the Tkinter window
window = tk.Tk()

# Create a variable to store the selected device family
family_var = tk.StringVar(window)
family_var.set('IOS_XE')  # Set the default value

# Create a drop-down menu for device family
family_label = tk.Label(window, text='Device Family:')
family_label.pack()
family_dropdown = tk.OptionMenu(window, family_var, 'IOS_XE', 'Nexus9K/3K', 'NonVRFBB', 'ISR')
family_dropdown.pack()

# Create an entry field for hostname
hostname_label = tk.Label(window, text=' Device Hostname:')
hostname_label.pack()
hostname_entry = tk.Entry(window)
hostname_entry.pack()

# Create a variable to store the selected row
row_var = tk.StringVar(window)


# Create a drop-down menu for row
row_label = tk.Label(window, text='Row:')
row_label.pack()
row_dropdown = tk.OptionMenu(window, row_var, '1A', '1B', '2A', '2B', '3A', '3B', '4A', '4B', '5A', '5B', '6A', '6B', '7A', '7B', '8A', '8B', '9A', '9B', '10A', '10B', '11A', '11B', '12A', '12B', '13A', '13B', '14A', '14B', '15A', '15B', '16A', '16B', '21A', '22A', '23A', '24A', '25A', '26A')
row_dropdown.pack()

# Create a button to trigger the Wizard function
button = tk.Button(window, text='Run Wizard', command=handle_button_click)
button.pack()

# Start the Tkinter event loop
window.mainloop()
