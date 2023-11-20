import pyperclip
import tkinter as tk
from tkinter import messagebox
import subprocess
import os

#Made by Andrew M. btw :3
#Webex bot to ping engineers when their devices are going to expire

def calculate_gateway(row):
    gateway_map = {
    '1A': "10.122.160.1",
    '1B': "10.122.160.129",
    '2A': "10.122.160.1",
    '2B': "10.122.160.129",
    '3A': '10.122.161.1',
    '3B': '10.122.161.129',
    '4A': '10.122.161.1',
    '4B': '10.122.161.129',
    '5A': '10.122.162.1',
    '5B': '10.122.162.129',
    '6A': '10.122.162.1',
    '6B': '10.122.162.129',
    '7A': '10.122.163.1',
    '7B': '10.122.163.129',
    '8A': '10.122.163.1',
    '8B': '10.122.163.129',
    '9A': '10.122.164.1',
    '9B': '10.122.164.129',
    '10A': '10.122.164.1',
    '10B': '10.122.164.129',
    '11A': '10.122.165.1',
    '11B': '10.122.165.129',
    '12A': '10.122.165.1',
    '12B': '10.122.165.129',
    '13A': '10.122.166.1',
    '13B': '10.122.166.129',
    '14A': '10.122.166.1',
    '14B': '10.122.166.129',
    '15A': '10.122.167.1',
    '15B': '10.122.167.129',
    '16A': '10.122.167.1',
    '16B': '10.122.167.129',
    '21A': '10.122.176.1',
    '22A': '10.122.176.1',
    '23A': '10.122.176.129',
    '24A': '10.122.176.129',
    '25A': '10.122.177.1',
    '26A': '10.122.177.1',
}
    return gateway_map.get(row, "")

IPs = {
    '1A': "10.122.160.",
    '1B': "10.122.160.",
    '2A': "10.122.160.",
    '2B': "10.122.160.",
    '3A': '10.122.161.',
    '3B': '10.122.161.',
    '4A': '10.122.161.',
    '4B': '10.122.161.',
    '5A': '10.122.162.',
    '5B': '10.122.162.',
    '6A': '10.122.162.',
    '6B': '10.122.162.',
    '7A': '10.122.163.',
    '7B': '10.122.163.',
    '8A': '10.122.163.',
    '8B': '10.122.163.',
    '9A': '10.122.164.',
    '9B': '10.122.164.',
    '10A':'10.122.164.',
    '10B': '10.122.164.',
    '11A': '10.122.165.',
    '11B': '10.122.165.',
    '12A': '10.122.165.',
    '12B': '10.122.165.',
    '13A': '10.122.166.',
    '13B': '10.122.166.',
    '14A': '10.122.166.',
    '14B': '10.122.166.',
    '15A': '10.122.167.',
    '15B': '10.122.167.',
    '16A': '10.122.167.',
    '16B': '10.122.167.',
    '21A': '10.122.176.',
    '22A': '10.122.176.',
    '23A': '10.122.176.',
    '24A': '10.122.176.',
    '25A': '10.122.177.',
    '26A': '10.122.177.',
}

def IP_pinger_A(row):
    if row in IPs:
        with open(os.devnull, "wb") as limbo:
            for n in range(30, 126):
                ip = IPs[row] + str(n)
                result = subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],
                                          stdout=limbo, stderr=limbo).wait()
                if result:
                    inactive_ip = ip
                    return inactive_ip
    
def IP_pinger_B(row):
    if row in IPs:
        with open(os.devnull, "wb") as limbo:
            for n in range(145, 254):
                ip = IPs[row] + str(n)
                result = subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],
                                          stdout=limbo, stderr=limbo).wait()
                if result:
                    inactive_ip =  ip
                    return inactive_ip

def Wizard(family, row, hostname, filename , interface_name=" " ,  use_dhcp=False):
    output = ''
    gateway = calculate_gateway(row)
    inactive_ip = " "


    if use_dhcp:
        inactive_ip = "\nip add dhcp"  #If the DCHP box is selected it uses DHCP instead of pinging for a empty address
        
    else:
    #...Decides to call either the A or B pinger function depending on the row.
     if row in ('1A', '2A', '3A', '4A', '5A', '6A', '7A', '8A', '9A', '10A', '11A', '12A',  '13A', '14A', '15A', '16A', '21A', '22A', '23A', '24A', '25A', '26A'):
        inactive_ip = IP_pinger_A(row)

     if row in ('1B', '2B', '3B', '4B', '5B', '6B', '7B', '8B', '9B', '10B', '11B', '12B', '13B', '14B', '15B', '16B'):
        inactive_ip = IP_pinger_B(row)

    #..Device Command Determination
    if family == "IOS-XE Switches":
        output += f"conf t\nhostname {hostname}\nip ftp source-interface g0/0\nip tftp source-interface g0/0\nno ip domain lookup \nbanner motd c A Wizard Was Here c \nline con 0\nlogging sync\nexit\nint g0/0\nno shut\nno ip add \nip add {inactive_ip} 255.255.255.128 \nip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 {gateway}\nend\nwr\nping vrf Mgmt-vrf 10.122.153.158"

    elif family == 'Nexus Switches':
        output += f'conf t \nhostname {hostname} \nip ftp source-interface mgmt0 \nip tftp source-interface mgmt0  \nint mgmt0 \nno shut \nno ip add \nip add {inactive_ip} 255.255.255.128 \nvrf member management \nvrf context management \nip route 0.0.0.0 0.0.0.0 {gateway} \ncopy run start \nping 10.122.153.158 vrf management'

    elif family == 'Data Port Vlan BB':
        output += f'conf t \nhostname {hostname} \nip ftp source-interface {interface_name} \nip tftp source-interface {interface_name} \nno ip domain lookup \nline con 0 \nlogging sync \nexit \nint vlan 1 \nip add {inactive_ip} 255.255.255.128 \nno shut \nint {interface_name} \nno shut \nsw \nsw mode access \nsw access vlan 1 \nexit \nip route 0.0.0.0 0.0.0.0 {gateway} \nend \ncopy run start \nping 10.122.153.158'

    elif family == 'ISR/ASR':
        output += f'conf t \nhostname {hostname} \nip ftp source-interface g0 \nip tftp source-interface g0 \ncdp run \nno ip domain lookup \nline con 0 \nlogging sync \nexit \nint g0 \nno shut \nip add {inactive_ip} 255.255.255.128 \nexit \nip route vrf Mgmt-intf 0.0.0.0 0.0.0.0 {gateway} \nend \ncopy run start \nping vrf Mgmt-intf 10.122.153.158' 

    elif family == 'Switch Global Route (No VRF)':
        output += f"conf t\nhostname {hostname}\nip ftp source-interface g0/0\nip tftp source-interface g0/0\nno ip domain lookup\nline con 0\nlogging sync\nexit\nint g0/0\nno shut\nno ip add \nip add {inactive_ip} 255.255.255.128 \nexit \nip route 0.0.0.0 0.0.0.0 {gateway}\nend\ncopy run start\nping 10.122.153.158"

    elif family == 'Nexus 9/3k Loader TFTP Boot':
        output += f"set ip {inactive_ip} \nset gw {gateway} \nboot tftp://10.122.153.158/{filename}"

    elif family == "IOS-XE TFTP Rommon Boot":
        output += f"IP_ADDRESS={inactive_ip} \nIP_SUBNET_MASK=255.255.255.128 \nDEFAULT_GATEWAY={gateway} \nboot tftp://10.122.153.158/{filename}"
        
    pyperclip.copy(output)  # Copy the output to the clipboard
    print(output)  # Print the output

#Takes the values from the GUI and calls the Wizard Function with them
def handle_button_click(): 
    family = family_var.get()
    row = row_var.get()
    hostname = hostname_entry.get()
    interface_name = interface_entry.get() 
    use_dhcp = dhcp_var.get()  # Get the state of the DHCP checkbox
    filename = filename_entry.get()

    if family == 'Data Port Vlan BB' and not interface_name:  # Check if interface name is empty for VlanBB
        messagebox.showerror('Error', 'Enter the interface name you weezo.')
        return 
    
    if family not in ["Nexus 9/3k Loader TFTP Boot" , "IOS-XE TFTP Rommon Boot"] and not hostname:  # Check hostname if family is not "Nexus 9/3k Loader TFTP Boot"
        messagebox.showerror('Error' , 'Enter a hostname you weezo.')
        return

    if not row:
        messagebox.showerror('Error' , 'Enter a row you weezo.')
        return
    
    Wizard(family, row, hostname, filename , interface_name , use_dhcp)
    messagebox.showinfo("Success", f"The Wizard successfully cast the spell for Family: {family} and Row: {row}.")

# Create the Tkinter window
window = tk.Tk()
window.geometry("340x250")

# Create a variable to store the selected device family
family_var = tk.StringVar(window)


# Create a drop-down menu for device family
family_label = tk.Label(window, text='Device Family:')
family_label.pack()
family_dropdown = tk.OptionMenu(window, family_var, 'IOS-XE Switches', 'Nexus Switches', 'Data Port Vlan BB', 'ISR/ASR' , 'Switch Global Route (No VRF)' , 'Nexus 9/3k Loader TFTP Boot' , "IOS-XE TFTP Rommon Boot")
family_dropdown.pack()

# Create an entry field for hostname
hostname_label = tk.Label(window, text=' Device Hostname:')
hostname_entry = tk.Entry(window)


# Create an entry field for the interface name
interface_label = tk.Label(window, text='Interface Name (e.g., G1/0/52):')
interface_entry = tk.Entry(window)

# Create an entry field for the interface name
filename_label = tk.Label(window, text='File Name on FTP Server')
filename_entry = tk.Entry(window)


# Create a variable to store the selected row
row_var = tk.StringVar(window)


# Create a drop-down menu for row
row_label = tk.Label(window, text='Row:')
row_dropdown = tk.OptionMenu(window, row_var, '1A', '1B', '2A', '2B', '3A', '3B', '4A', '4B', '5A', '5B', '6A', '6B', '7A', '7B', '8A', '8B', '9A', '9B', '10A', '10B', '11A', '11B', '12A', '12B', '13A', '13B', '14A', '14B', '15A', '15B', '16A', '16B', '21A', '22A', '23A', '24A', '25A', '26A')


# Create a variable to store the DHCP checkbox state
dhcp_var = tk.BooleanVar(window)
dhcp_var.set(False)  # Set the default state to unchecked

# Create a checkbox for DHCP
dhcp_checkbox = tk.Checkbutton(window, text= 'DHCP (Check if you keep getting duplicate IPs)', variable=dhcp_var)

# Create a button to trigger the Wizard function
button = tk.Button(window, text='Call The Wizard', command=handle_button_click)

# Logic for choosing which fields pop up for which family
def IOS_XE_Dynamic(*args):
    selected_family = family_var.get()
    if selected_family in ['IOS-XE Switches', 'Nexus Switches', 'ISR/ASR', 'Switch Global Route (No VRF)']:
        hostname_label.pack_forget()
        hostname_entry.pack_forget()
        interface_label.pack_forget()
        interface_entry.pack_forget()
        dhcp_checkbox.pack_forget()
        row_label.pack_forget()
        row_dropdown.pack_forget()
        button.pack_forget()

        hostname_label.pack()
        hostname_entry.pack()
        dhcp_checkbox.pack()
        row_label.pack()
        row_dropdown.pack()
        button.pack()

    if selected_family == 'Data Port Vlan BB':
        hostname_label.pack_forget()
        hostname_entry.pack_forget()
        interface_label.pack_forget()
        interface_entry.pack_forget()
        dhcp_checkbox.pack_forget()
        row_label.pack_forget()
        row_dropdown.pack_forget()
        button.pack_forget()

        hostname_label.pack()
        hostname_entry.pack()
        interface_label.pack()
        interface_entry.pack()
        dhcp_checkbox.pack()
        row_label.pack()
        row_dropdown.pack()
        button.pack()

    if selected_family in ["IOS-XE TFTP Rommon Boot" , 'Nexus 9/3k Loader TFTP Boot']:
        hostname_label.pack_forget()
        hostname_entry.pack_forget()
        interface_label.pack_forget()
        interface_entry.pack_forget()
        dhcp_checkbox.pack_forget()
        row_label.pack_forget()
        row_dropdown.pack_forget()
        button.pack_forget()    

        filename_label.pack()
        filename_entry.pack()
        row_label.pack()
        row_dropdown.pack()
        button.pack()


# Bind the toggle functions to the family_var variable
family_var.trace_add('write', IOS_XE_Dynamic)

# Start the Tkinter event loop
window.mainloop()
