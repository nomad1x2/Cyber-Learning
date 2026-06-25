"""
Refs:
- https://compile7.org/serialize-and-deserialize/how-to-serialize-and-deserialize-xml-in-dash/#reading-xml-files
- https://realpython.com/python-dash/
- https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_collapsible_symbol
- https://htmlcolorcodes.com/color-picker/
"""

import xml.etree.ElementTree as ET
from dash import Dash, Input, Output, dcc, html, MATCH
import base64, io

def parse_xml(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    root = ET.parse(io.BytesIO(decoded)).getroot()
    
    runstats   = root.find("runstats")
    hosts_elem = runstats.find("hosts")
    finished   = runstats.find("finished")

    hosts_up   = int(hosts_elem.get("up"))
    hosts_down = int(hosts_elem.get("down"))
    scan_time  = finished.get("timestr")
    scan       = root.get("args")

    host_info = {}

    #this absolutely atrocious block of code could most likely be more efficient
    for host in root.findall("host"):

        for a in host.findall("address"):
            if a.get("addrtype") == "ipv4":
                ip = a.get("addr")
        host_info[ip] = {}

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

                    script_blocks = port.findall("script")
                    for script in script_blocks:
                        if script is not None:
                            if "VULNERABLE" in script.get("output") and "NOT VULNERABLE" not in script.get("output"):
                                table = script.find("table")
                                if table is not None:
                                    vuln_data.append([port_id, script.get("id"), script.find("table").get("key")])
                            for table in script.findall("table"):
                                for vuln_table in table.findall("table"):
                                    vuln_id   = vuln_table.find("elem[@key='id']")
                                    vuln_cvss = vuln_table.find("elem[@key='cvss']")
                                    
                                    #this is the big filter for what vulns are processed, edit as needed
                                    if vuln_id is not None and vuln_cvss is not None:
                                        if float(vuln_cvss.text) >= 8.0:
                                            if "vuln" in vuln_id.text.lower() or "cve" in vuln_id.text.lower():
                                                vuln_data.append([port_id, vuln_id.text, vuln_cvss.text])
                if len(port_data) > 0:
                    open_ports.append(port_data)
                if len(vuln_data) > 0:
                    vulns.append(vuln_data)

        os_elem = host.find("os")
        if os_elem is not None:
            match = os_elem.find("osmatch")
            if match is not None:
                host_info[ip]['os'] = match.get("name")
            else:
                if ports is not None:
                    ssh_service     = None
                    smb_service     = None
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
                    if smb_service is not None and "windows" in smb_service.get("product", "").lower():
                        product = smb_service.get("product")
                        host_info[ip]["os"] = " ".join(product.split()[:-1])
                    elif netbios_service is not None and "windows" in netbios_service.get("product", "").lower():
                        product = netbios_service.get("product")
                        host_info[ip]["os"] = " ".join(product.split()[:-1])
                    elif ssh_service is not None:
                        version = ssh_service.get("version", "")
                        ostype  = ssh_service.get("ostype", "")
                        if version and ostype:
                            host_info[ip]["os"] = f"{version.split()[1]} {ostype}"

        hostscript = host.find("hostscript")
        if hostscript is not None:
            for script in hostscript.findall("script"):
                if "VULNERABLE" in script.get("output") and "NOT VULNERABLE" not in script.get("output"):
                    table = script.find("table")
                    if table is not None:
                        host_vulns = [script.get("id"), table.get("key")]
                        if len(host_vulns) > 0:
                            vulns.append([host_vulns])

        if len(open_ports) > 0:
            host_info[ip]['ports'] = open_ports
        if len(vulns) > 0:
            host_info[ip]['vulns'] = vulns
    return host_info, scan_time, hosts_up

#severe helpers

#makeshift severity scale: 0,~10,+
def severity_class(vuln_count):
    if vuln_count == 0:
        return "sev-none"
    if vuln_count <= 10:
        return "sev-med"
    return "sev-high"


def make_badge(vuln_count):
    sev = severity_class(vuln_count)
    if vuln_count == 0:
        label = "Clean"
    elif vuln_count == 1:
        label = "1 vuln"
    else:
        label = f"{vuln_count} vulns"
    return html.Span(label, className=f"badge {sev}")

def build_rows(host_info):

    all_rows    = []
    total_vulns = 0
    high_count  = 0
    clean_count = 0

    for host_ip, host in host_info.items():

        vuln_count      = 0
        port_vuln_match = {}

        if host.get("ports"):
            for p in host.get("ports"):
                port_vuln_match[''.join(p[:1][0])] = [p[1:]]

        #need to find a better way to match vulns without port nums mentioned?
        if host.get("vulns"):
            for all_vulns in host.get("vulns"):
                for v in all_vulns:
                    if v[0] in port_vuln_match:
                        port_vuln_match[v[0]].append(v[1:])
                        vuln_count += 1
                    elif "smb" in v[0].lower():
                        port_vuln_match['445'].append(v[1:])
                        vuln_count += 1

        total_vulns += vuln_count
        if vuln_count > 10:
            high_count += 1
        if vuln_count == 0:
            clean_count += 1

        sev = severity_class(vuln_count)

        #port/cve rows for the detail panel
        detail_rows = []
        for r in port_vuln_match:
            service_str = f"{r} - {' '.join(port_vuln_match[r][0])}"
            vuln_list   = port_vuln_match[r][1:]

            if vuln_list:
                cve_pills = []
                for v in vuln_list:
                    cve_pills.append(html.Span(v[0], className="cve-pill"))
                cve_cell = html.Td(cve_pills, className="td-cves")
            else:
                cve_cell = html.Td("None identified by scan", className="td-cves td-cves-empty")

            detail_rows.append(
                html.Tr(children=[
                    html.Td(service_str, className="td-service"),
                    cve_cell,
                ])
            )

        summary_row = html.Tr(
            className=f"host-summary-row {sev}",
            id={"type": "host-btn", "index": host_ip},
            n_clicks=0,
            children=[
                html.Td(className=f"sev-bar {sev}"),
                html.Td(host_ip,                         className="td-ip"),
                html.Td(host.get("os", "Unknown"),       className="td-os"),
                html.Td(str(len(host.get("ports", []))), className="td-ports"),
                html.Td(make_badge(vuln_count),          className="td-badge"),
            ],
        )

        detail_row = html.Tr(
            id={"type": "host-detail", "index": host_ip},
            style={"display": "none"},
            children=[
                html.Td(colSpan=5, className="detail-cell", children=[
                    html.Table(className="detail-table", children=[
                        html.Thead(
                            html.Tr(children=[
                                html.Th("Port / Service",  className="detail-th"),
                                html.Th("Vulnerabilities", className="detail-th"),
                            ])
                        ),
                        html.Tbody(detail_rows),
                    ]),
                ]),
            ],
        )

        all_rows.append(summary_row)
        all_rows.append(detail_row)
        
    return all_rows, total_vulns, high_count, clean_count

#app setup

host_info = {}
scan_time = "No scan loaded"
hosts_up  = 0
all_rows, total_vulns, high_count, clean_count = build_rows(host_info)

app = Dash(__name__)
app.title = "Nmap Dash"


#layout
 
app.layout = html.Div(className="dash-root", children=[

    html.Div(className="page-header", children=[
        html.Div(children=[
            html.H1("Nmap Scan Dashboard", className="header-title"),
            html.P(f"Scan time: {scan_time}", className="scan-time", id="scan-time"),
        ]),
        dcc.Upload(
            id="upload-scan",
            className="upload-zone",
            multiple=False,
            children=[
                html.Span("Drop scan file here", className="upload-label"),
                html.Div("or click to browse", className="upload-sub"),
            ],
        ),
    ]),

    html.Div(className="stats-row", children=[
        html.Div(className="stat-card", children=[
            html.Div("Hosts",        className="stat-label"),
            html.Div(str(hosts_up),  className="stat-val", id="stat-hosts"),
        ]),
        html.Div(className="stat-card", children=[
            html.Div("Total vulns",       className="stat-label"),
            html.Div(str(total_vulns),    className="stat-val danger", id="stat-total"),
        ]),
        html.Div(className="stat-card", children=[
            html.Div("High severity",  className="stat-label"),
            html.Div(str(high_count),  className="stat-val warn", id="stat-high"),
        ]),
        html.Div(className="stat-card", children=[
            html.Div("Clean hosts",    className="stat-label"),
            html.Div(str(clean_count), className="stat-val ok", id="stat-clean"),
        ]),
    ]),

    html.Div(className="table-wrap", children=[
        html.Table(className="host-table", children=[
            html.Thead(
                html.Tr(className="host-table-header", children=[
                    html.Th("",                 className="th-sev"),
                    html.Th("Host",             className="th-host"),
                    html.Th("Operating System", className="th-os"),
                    html.Th("Open Ports",       className="th-ports"),
                    html.Th("Vulnerabilities",  className="th-vulns"),
                ])
            ),
            html.Tbody(all_rows, id="host-tbody"),
        ]),
    ]),

])

@app.callback(
    Output({"type": "host-detail", "index": MATCH}, "style"),
    Input({"type": "host-btn",     "index": MATCH}, "n_clicks"),
    prevent_initial_call=True,
)
def toggle(n_clicks):
    if n_clicks % 2 == 1:
        return {"display": "table-row"}
    return {"display": "none"}

@app.callback(
    Output("host-tbody",  "children"),
    Output("stat-hosts",  "children"),
    Output("stat-total",  "children"),
    Output("stat-high",   "children"),
    Output("stat-clean",  "children"),
    Output("scan-time",   "children"),
    Input("upload-scan",  "contents"),
    prevent_initial_call=True,
)

def load_scan(contents):
    host_info, scan_time, hosts_up = parse_xml(contents)
    all_rows, total_vulns, high_count, clean_count = build_rows(host_info)
    return all_rows, str(hosts_up), str(total_vulns), str(high_count), str(clean_count), f"Scan time: {scan_time}"
 
if __name__ == "__main__":
    app.run(debug=True)