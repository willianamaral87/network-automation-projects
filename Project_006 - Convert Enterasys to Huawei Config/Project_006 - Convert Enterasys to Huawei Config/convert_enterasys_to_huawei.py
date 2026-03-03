
#######################################################################
####### Configuration Conversion Script from Enterasys to Huawei ######
#######################################################################

#######################################################################
####################### INSTRUCTIONS ##################################
#######################################################################

# Check the credentials and fill in the variables below.
var_Endereco_IP_Temp = "10.10.10.10"
var_Senha_Admin = "pwd_admin"
var_Senha_PSK = "pwd_psk"

#######################################################################
#################### GET DATA FROM ENTERASYS ##########################
#######################################################################

arq_config = 'switch-enterasys.txt'

lista_config = []

# Import regular expression
import re

# Import the Enterasys backup file
with open(arq_config, 'r') as tex:
    for linha in tex:
        lista_config.append(linha)
tex.close()

# VLAN Data
output_db_vlans = []

# VLAN Interface and Default Route
intvlan_default = ''

stp_mode = 'mstp'

# Capture values from the Enterasys configuration
for i in range(len(lista_config)):
    # Hostname
    if 'set system name ' in lista_config[i]:
        hostname = lista_config[i][17:-2]
    # Location
    if 'set system location ' in lista_config[i]:
        snmp_location = lista_config[i][21:-2]
    # STP
    if 'set spantree version ' in lista_config[i]:
        stp_mode = lista_config[i][21:-1]
    
    # VLANs
    if 'set vlan name ' in lista_config[i]:
        cmd = lista_config[i]

        saida = re.search('\\"\\b', cmd, re.IGNORECASE)

        if saida is not None:
            output_db_vlans.append("vlan " +cmd[14:saida.start()-1] + "\n " + "description " + cmd[saida.start():-1] + "\n name " + cmd[saida.start():-1])
    
    if 'set ip address' in lista_config[i]:
        get_pos_final_ip = re.search('\\bmask\\b', lista_config[i], re.IGNORECASE)
        get_pos_inicial_gw = re.search('\\bgateway\\b', lista_config[i], re.IGNORECASE)
        
        if get_pos_final_ip is not None:
            ip_address = lista_config[i][15:get_pos_final_ip.start()]
            mask = lista_config[i][get_pos_final_ip.end()+1:get_pos_inicial_gw.start()]
            gateway = lista_config[i][get_pos_inicial_gw.end()+1:-1]
        
    # Management VLAN
    if 'set host vlan' in lista_config[i]:
        
        vlan_gerencia = lista_config[i][14:-1]

        # Generate VLAN interface and default route string
        intvlan_default = 'interface vlan ' + vlan_gerencia + '\n'
        intvlan_default += ' ip address '+ ip_address + mask + '\n'
        intvlan_default += ' undo icmp redirect send\n'
        intvlan_default += ' undo arp-proxy inner-sub-vlan-proxy enable\n'
        intvlan_default += 'ip route-static 0.0.0.0 0.0.0.0 '+ gateway

#########################################################################

print('Temporary Access:  ')
print('ssh -oHostKeyAlgorithms=+ssh-dss -i id_rsa admin@' + var_Endereco_IP_Temp)
print('Senha123@')
print('Senha123@')
print()

print('system-view')

print('aaa')
print(' local-user cisco password irreversible-cipher cisco123')
print(' local-user cisco privilege level 15')
print(' local-user cisco service-type telnet terminal ssh ftp')
print(' local-aaa-user password policy administrator')
print('  password history record number 0')
print('  password expire 0')
print('quit')
print('quit')

print()

print('telnet server enable')
print('telnet server-source all-interface')
print('Y')

print()

print('#Perform Log Off')
print('#Log in via Telnet using the user cisco and password cisco123')
print('telnet ' + var_Endereco_IP_Temp)
print('#Change the Password')
print('')

print('New Temporary Password:')
print('Username: cisco | senha: cisco123 | nova senha: Senha123@')
print('cisco')
print('cisco123')
print('Y')
print('cisco123')
print('Senha123@')
print('Senha123@')


print()

print('system-view')

# Print list of VLANs with names and descriptions
for vlan in range(len(output_db_vlans)):
    print(output_db_vlans[vlan])

print('quit')
print()

# Print VLAN interface and default route
print(intvlan_default)

print()

print('undo header login')
print('undo header shell')

print('dns domain net.company.com.br')
print('http server disable')
print('Y')
print('http secure-server disable')
print('Y')

print()

print('######### Configure SSH ############')
print('stelnet server enable')
print('ssh user admin')
print('ssh user admin authentication-type password')
print('ssh user admin service-type stelnet')
print('ssh authentication-type default password')
print('ssh server cipher aes256_ctr aes128_ctr')
print('ssh server hmac sha2_256')
print('ssh server dh-exchange min-len 2048')
print('undo ssh server publickey')

print()

print('#########  ############')

print('user-interface vty 0 4')
print(' authentication-mode aaa')
print(' protocol inbound all')
print(' user privilege level 15')
print(' idle-timeout 10')

print()

print('user-interface vty 16 20')
print(' authentication-mode aaa')
print(' protocol inbound all')
print(' user privilege level 15')
print(' idle-timeout 10')
print('quit')

print()

print('undo http acl')
print('undo telnet server acl')
print('undo ssh server acl')

print()

print('undo acl number 2080')
print('undo acl number 2090')

print()

print('----- Rede A -----')
print('acl name SNMP_RO_SERVER_A 2070')
print(' rule 5 permit source 10.10.1.0 0.0.0.255')
print(' rule 10 permit source 10.101.1.0  0.0.0.255')
print(' rule 100 deny logging')

print()

print('----- Rede B -----')
print('acl name SNMP_RO_SERVER_A 2070')
print(' rule 5 permit source 10.107.11.0 0.0.0.255')
print(' rule 10 permit source 10.107.15.0 0.0.0.255')
print(' rule 100 deny logging')

print()

print('acl number 2080')
print(' description SNMP_RO_SERVER_B')
print(' rule permit source 10.3.0.0 0.0.1.255')
print(' rule permit source 10.25.0.0 0.0.0.255')
print(' rule deny source any logging')
print('quit')

print()

print('acl number 2090')
print(' description Acesso_Remoto')
print(' rule permit source 10.1.0.0 0.0.1.255')
print(' rule permit source 10.2.0.0 0.0.0.255')
print(' rule deny source any logging')
print('quit')

print()

print('snmp-agent')
print('snmp-agent community read COMMUNITY_A acl 2080')
print('snmp-agent community read COMMUNITY_B acl 2070')
print('snmp-agent sys-info location ' + snmp_location )
print('undo snmp-agent sys-info contact')
print('snmp-agent sys-info version all')
print('snmp-agent trap enable')
print('Y')

print('snmp-agent trap source Vlanif' + vlan_gerencia)
print('snmp-agent protocol source-interface Vlanif' + vlan_gerencia)

print()
print('----- Rede B -----')
print('snmp-agent sys-info contact port-security')


print()

print('info-center timestamp log date')
print('info-center logbuffer size 1024')
print('info-center loghost 10.1.0.8 facility local4')
print('info-center loghost source Vlanif'+vlan_gerencia)

print()

print('clock timezone RJO minus 03:00:00')

print()


print('undo ntp-service disable')
print('ntp-service server disable')
print('Y')

print()

print('ntp-service ipv6 server disable')
print('ntp-service unicast-server 10.2.1.7')
print('ntp-service unicast-server 10.2.3.1')
print('ntp-service unicast-server 10.3.0.5')

print()

print('lldp enable')

print('stp mode ' + stp_mode)






print('####### TACACS Configuration #######')

print()

print('hwtacacs-server template TACACS')
print('hwtacacs-server authentication 10.2.3.5')
print('hwtacacs-server authentication 10.2.1.2 secondary')
print('hwtacacs-server authorization 10.2.3.5')
print('hwtacacs-server authorization 10.2.1.2 secondary')
print('hwtacacs-server accounting 10.2.3.5')
print('hwtacacs-server accounting 10.2.1.2 secondary')
print('hwtacacs-server source-ip source-vlanif ' + vlan_gerencia )
print('hwtacacs-server shared-key cipher ' + var_Senha_PSK)
print('undo hwtacacs-server user-name domain-included')
print('quit')

print()

print('aaa')
print('recording-scheme ACESSO_CLI')
print(' recording-mode hwtacacs TACACS')
print(' cmd recording-scheme ACESSO_CLI')

print('authentication-scheme ACESSO_CLI')
print(' authentication-mode local hwtacacs')

print('authorization-scheme ACESSO_CLI')
print(' authorization-mode local  hwtacacs')

print('accounting-scheme ACESSO_CLI')
print(' accounting-mode hwtacacs')

print('domain company.net')
print(' authentication-scheme ACESSO_CLI')
print(' accounting-scheme default')
print(' authorization-scheme ACESSO_CLI')
print(' hwtacacs-server TACACS')


print('domain company.net admin')

print()

print('##### Apply Port Configurations ######')


#########################################################
print()
print('#### Port Configuration ####')
print('interface range GigabitEthernet0/0/2 to GigabitEthernet0/0/24')
print(' port link-type hybrid')
print(' port hybrid pvid vlan 106')
print(' port hybrid tagged vlan 506')
print(' port hybrid untagged vlan 106')
print()
print('interface XGigabitEthernet0/0/1')
print(' description PORTA - SWITCH')
print(' port link-type trunk')
print(' port trunk allow-pass vlan 2 to 4094')
print(' lldp compliance cdp txrx')


print()
print()
print('######################################################################')
print('######## Finalize Configuration During the Maintenance Window ########')
print('######################################################################')

print()

print('#### Change RADIUS Entry to TACACS on ACS\n')

print()


print('Validar SNMP: ')
print('snmpwalk -v2c -c community ' + hostname + ' sysLocation')

print()
print()
print()

print('# Validate access using local admin user')
print('# Validate access using TACACS')
print()
print('# AChange Local Admin Password:')

print('aaa')
print(' local-user admin password irreversible-cipher cisco123')
print('# Nova senha de admin ' + var_Senha_Admin)

print()
print()

print('user-interface vty 0 4')
print('authentication-mode aaa')
print('protocol inbound ssh')
print('acl 2090 inbound')

print()

print('user-interface vty 16 20')
print('authentication-mode aaa')
print('protocol inbound ssh')
print('acl 2090 inbound')

print()

print('user-interface console 0')
print('authentication-mode aaa')

print()

print('# Adjust accounting on the ACS only after TACACS is working, and set local accounting after TACACS.')
print()
print('aaa')
print(' authentication-scheme ACESSO_CLI')
print('  authentication-mode hwtacacs local')
print()
print(' authorization-scheme ACESSO_CLI')
print('  authorization-mode hwtacacs local')
print()
print(' domain company.net')
print('  accounting-scheme ACESSO_CLI')

print()
print()
print()

print('aaa')
print('authorization-scheme ACESSO_CLI')
print('  authorization-cmd 0 hwtacacs local')
print('  authorization-cmd 1 hwtacacs local')
print('  authorization-cmd 2 hwtacacs local')
print('  authorization-cmd 3 hwtacacs local')
print('  authorization-cmd 4 hwtacacs local')
print('  authorization-cmd 5 hwtacacs local')
print('  authorization-cmd 6 hwtacacs local')
print('  authorization-cmd 7 hwtacacs local')
print('  authorization-cmd 8 hwtacacs local')
print('  authorization-cmd 9 hwtacacs local')
print('  authorization-cmd 10 hwtacacs local')
print('  authorization-cmd 11 hwtacacs local')
print('  authorization-cmd 12 hwtacacs local')
print('  authorization-cmd 13 hwtacacs local')
print('  authorization-cmd 14 hwtacacs local')
print('  authorization-cmd 15 hwtacacs local')



print()

print('#### Finalize the Configuration')
print()

print('undo telnet server enable')
print('Y')

print()

print('http acl 2090')
print('telnet server acl 2090')
print('ssh server acl 2090')


print('# Remove Unused Configurations')
print()

print('aaa')
print(' undo local-user cisco')
 
print('interface MEth0/0/1')
print(' shutdown')
 
print('interface Vlanif1')
print(' shutdown')

print('interface Vlanif1200')
print(' undo description')
print(' undo ip address dhcp-alloc')
print(' quit')
 
print('undo interface Vlanif1200')


print()

print('snmp-agent sys-info contact port-security')


print()
print('######################################################')


print('######### Apply PORT-SECURITY #########')
print('######### Configuration Example #######')
print('interface range GigabitEthernet0/0/2 to GigabitEthernet0/0/24')
print(' shutdown')
print(' port-security enable')
print(' port-security max-mac-num 3')
print(' port-security protect-action restrict')
print(' port-security mac-address sticky')
print(' undo shutdown')
