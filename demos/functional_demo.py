import ryurest

# If Ryu is running on an external host, you can redefine the API URI (the default is http://localhost:8080)
#       Example:
#           >> ryurest.API = "http://192.168.0.10:8080"

# Get the DPIDs of all switches connected to the controller as an array.
# The DPID is the "Datapath ID" of an OpenFlow switch connected to a controller.
DPID_list = ryurest.get_switches()

# Save the first DPID for the demo
# Example, DPID = 123917682136708
DPID = DPID_list[0]

# Now lets get the flow table of our specific switch (DPID)

# Get flow table of switch
flows = ryurest.get_flows(DPID)

# Print data to screen
print "\nGET FLOW TABLE FROM SWITCH:"
print flows  # Dumps JSON data

# Example data dump (unicode JSON). Note DPID is a string.
# {u'123917682136708':
#     [{
#         u'priority': 0, u'hard_timeout': 0, u'byte_count': 0,
#         u'duration_sec': 2096, u'actions': [u'OUTPUT:CONTROLLER'],
#         u'duration_nsec': 0, u'packet_count': 0, u'idle_timeout': 0,
#         u'cookie': 0, u'flags': 0, u'length': 80, u'table_id': 0, u'match': {}
#     }]
# }

# If we want a specific value from the JSON data...

# Getspecific value, "duration_sec" == lifetime of flow rule
duration_sec = flows[ str(DPID) ][0][ 'duration_sec' ]

# Print data to screen
print "\nPARSING SPECIFIC VALUE FOR FLOW TABLE DUMP: 'duration_sec'"
print duration_sec


# Next, lets add a flow to the switch!

# Construct the flow rule as a dictionary. For example:
flow_rule = {
    "dpid": DPID,
    "idle_timeout": 30, "hard_timeout": 30, "priority": 100,
    "match":{ "in_port":1 },
    "actions":[{ "type":"OUTPUT", "port": 2 }]
}

# Now call the add_flow() method and pass the flow rule dictionary as an argument:
ryurest.add_flow( flow_rule )

# Dump the flow table again to see the new flow added:
print "\nGET UPDATED FLOW TABLE FROM SWITCH:"
print ryurest.get_flows(DPID)
