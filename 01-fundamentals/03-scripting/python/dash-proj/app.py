"""
Refs:
- https://compile7.org/serialize-and-deserialize/how-to-serialize-and-deserialize-xml-in-dash/#reading-xml-files
- https://realpython.com/python-dash/
- https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_collapsible_symbol
"""

import xml.etree.ElementTree as ET
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html, MATCH

#read xml
tree = ET.parse("svc-os-vulns.xml")
root = tree.getroot()

#scan metadata out from runstats
runstats   = root.find("runstats")
hosts_elem = runstats.find("hosts")
finished   = runstats.find("finished")

hosts_up   = int(hosts_elem.get("up"))
hosts_down = int(hosts_elem.get("down"))
scan_time  = finished.get("timestr")
scan       = root.get("args")


# store information about each host
host_info = {}

"""
host_info = {
    '169.254.1.1': {
    
        'os'    : [osfamily, osgen],
        'ports' : [[portid, service name, product, version],],
        'vulns' : [[portid, CVE],],
    
    }
}    
"""

for host in root.findall("host"):

    #get ip
    for a in host.findall("address"):
        if a.get("addrtype") == "ipv4":
            ip = a.get("addr")
    host_info[ip] = {}
    
    #get open ports/product/service/version/vulns?
    open_ports = []
    vulns = []
    ports = host.find("ports")
    if ports is not None:
        for port in ports.findall("port"):
            port_data = []
            vuln_data = []
            state = port.find("state")
            if state is not None and state.get("state") == "open":
                port_id = port.get("portid")
                port_data.append(port_id)
                service = port.find("service")
                if service is not None:
                    service_name = service.get("name", "")
                    if service_name != "":
                        port_data.append(service_name)
                    service_product = service.get("product", "")
                    if service_product != "":
                        port_data.append(service_product)
                    service_version = service.get("version", "")
                    if service_version != "":
                        port_data.append(service_version)
                        
                #get service vulns
                script_blocks = port.findall("script")
                for script in script_blocks:
                    if script is not None:
                        if "VULNERABLE" in script.get("output") and not "NOT VULNERABLE" in script.get("output"):
                            vuln_data.append([port_id, script.get("id"), script.find("table").get("key")])
                        for table in script.findall("table"):
                            for vuln_table in table.findall("table"):
                                vuln_id = vuln_table.find("elem[@key='id']")
                                vuln_cvss = vuln_table.find("elem[@key='cvss']")
                                #lets do a 8.0 because there are way too many cves
                                if vuln_id is not None and float(vuln_cvss.text) >= 8.0:
                                    if "cve" in vuln_id.text.lower() or "vuln" in vuln_id.text.lower():
                                        vuln_data.append([port_id, vuln_id.text, vuln_cvss.text])
            if len(port_data) > 0:
                open_ports.append(port_data)
            if len(vuln_data) > 0:
                vulns.append(vuln_data)
        
    #get most likely OS candidate
    os_elem = host.find("os")
    #find returns first match or None, and nmap lists by accuracy
    match = os_elem.find("osmatch")
    if match is not None:
        os = match.get("name")
        host_info[ip]['os'] = os
    else:
        #lets check port infos, could get at least some information
        if ports is not None:
            ssh_service = None
            smb_service = None
            netbios_service = None
            for port in ports.findall("port"):
                service = port.find("service")
                if service is None:
                    continue
                portid = port.get("portid")
                if portid == "22":
                    ssh_service = service
                elif portid == "445":
                    smb_service = service
                elif portid == "139":
                    netbios_service = service
            #windows guess from smb (preferred)
            if (smb_service is not None and "windows" in smb_service.get("product", "").lower()):
                product = smb_service.get("product")
                host_info[ip]["os"] = (f"Best guess: {' '.join(product.split()[:-1])}")
            #windows guess from netbios (fallback)
            elif (netbios_service is not None and "windows" in netbios_service.get("product", "").lower()):
                product = netbios_service.get("product")
                host_info[ip]["os"] = (f"Best guess: {' '.join(product.split()[:-1])}")
            #linux/unix guess from ssh
            elif ssh_service is not None:
                version = ssh_service.get("version", "")
                ostype = ssh_service.get("ostype", "")
                if version and ostype:
                    host_info[ip]["os"] = (f"Best guess: {version.split()[1]} {ostype}")

    #update vuln list with any host vuln scripts
    hostscript = host.find("hostscript")
    if hostscript is not None:
        for script in hostscript.findall("script"):
            if "VULNERABLE" in script.get("output") and not "NOT VULNERABLE" in script.get("output"):
                host_vulns = [script.get("id"), script.find("table").get("key")]
                if len(host_vulns) > 0:
                    vulns.append(host_vulns)
                
    if len(open_ports) > 0:
        host_info[ip]['ports'] = open_ports
    if len(vulns) > 0:
        host_info[ip]['vulns'] = vulns

#print(host_info)

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Nmap Dash"

#Layout

host_table = []


#iterate through each host and create the host table
for host_ip, host in host_info.items():
    
    #[0] is always service info
    port_vuln_match = {}
    
    if host.get("ports"):
        for p in host.get("ports"):
            port_vuln_match[''.join(p[:1])] = [p[1:]]
    
    #match vuln to port
    if host.get("vulns"):
        for all_vulns in host.get("vulns"):
            for v in all_vulns:
                if v[0] in port_vuln_match:
                    port_vuln_match[v[0]].append(v[1:])
                    
    #build rows first
    rows = []
    for r in port_vuln_match:
        rows.append(
            html.Tr(children=[
                html.Td(f"{r} - {' '.join(port_vuln_match[r][0])}"),
                html.Td(', '.join(v[0] for v in port_vuln_match[r][1:]) or "None identified by scan"), #check this one, looks like got rid of some hostscript vulns?
            ]),
        )
    
    vuln_count = sum(len(group) for group in host.get('vulns', 'Unk'))

    host_data = html.Div(children=[
        html.Table(
            html.Thead(
                html.Tr(className="collapsible", id={"type": "host-btn", "index": host_ip}, n_clicks=0, children=[
                    html.Th(host_ip),
                    html.Th(host.get('os', 'Unknown')),
                    html.Th(f'Open Ports: {len(host.get('ports', 'Unk'))}'),
                    html.Th(f'Vulnerabilities: {vuln_count}'),
                ]),
            ),
        ),
        html.Div(className="content", id={"type": "host-detail", "index": host_ip}, style={"display": "none"}, children=[
            html.Table(className="detail-table", children=[
                html.Tr(children=[
                    html.Td("Port / Service:"),
                    html.Td("Vulnerabilities:"),
                ]),
                *rows,
            ]),
        ]),
    ])
    host_table.append(host_data)

app.layout = html.Div(children=[
    
    #<div>
    html.Div(className="header", children=[
        html.H1(children="Nmap Scan Dashboard", className="header-title"),
        html.P(f"Scan time: {scan_time}", className="header-description"),
        html.P(f"Number of hosts: {hosts_up}", className="header-description"),
    ]),
    #</div>


    
    #<div>
    html.Div(className="row", children=[
    
    
        #<card 1 - graph>
        html.Div(className="column column-25", children=[
            html.Div(className="card", children=[
                #<graph data>
                html.Div(children=[
                    "Graph PlaceholdeR"
                ]),
                #</graph data>
            ]),
        ]),
        #<card 1>


        #<card 2 - host data>
        html.Div(className="column column-75", children=[
            html.Div(className="card", children=[
            
                #<div>
                html.Div(children=[
                    html.Div(children=[
                        html.Table(
                            html.Tr(children=[
                                html.Th("Host"),
                                html.Th("Operating System"),
                                html.Th("Open Ports"),
                                html.Th("Vulnerabilities"),
                            ]),
                        ),
                    ]),
                ]),
                #</div>

            
            
            
                html.Div(className="host_data", children=[
                    *host_table,
                ]),
            ]),
        ]),
        #<card 2>
        
        
    ])
    #</div>


   
])

@app.callback(
    Output({"type": "host-detail", "index": MATCH}, "style"),
    Input({"type": "host-btn", "index": MATCH}, "n_clicks"),
    prevent_initial_call=True,
)
def toggle(n_clicks):
    return {"display": "block"} if n_clicks % 2 == 1 else {"display": "none"}

if __name__ == "__main__":
    app.run(debug=True)
