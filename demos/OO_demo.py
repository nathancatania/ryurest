from ryu_switch import RyuSwitch

# Instantiate a new switch
switch1 = RyuSwitch()

# If Ryu is running on an external host, you can redefine the API URI (the default is http://localhost:8080)
#       Example:
#           >> ryurest.API = "http://192.168.0.10:8080"
# You will need to do this for each switch instance.

# We will need to set the DPID.
# The DPID is the "Datapath ID" of an OpenFlow switch connected to a controller.

# As we did not specify the DPID of the switch when when created it,
#     we will need to get a list of all the DPIDs connected to the controller and assign one.

# If you already know the DPID, you can also pass it to the constructor. For example:
#     >> switch1 = RyuSwitch( 1234567890 )

# Get the DPIDs of all switches connected to the controller as an array.
DPID_list = switch1.get_switches()

# Lets assign the first DPID to switch1
switch1.DPID = DPID_list[0]

# Now that we have a list of DPIDs, we can also create other switches!
# switch2 = RyuSwitch( DPID_list[1] )
# switch3 = RyuSwitch( DPID_list[2] )
# switch4 = RyuSwitch( DPID_list[3] )
# ...
# etc

# Since we have now properly initialized our switch(es), we can start to work directly with the API!

# Get flow table of switches (JSON)
flows = switch1.get_flows()

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

# Get specific value, "duration_sec" == lifetime of flow rule
duration_sec = flows[ str(switch1.DPID) ][0][ 'duration_sec' ]

# Print data to screen
print "\nPARSING SPECIFIC VALUE FOR FLOW TABLE DUMP: 'duration_sec'"
print duration_sec


# Next, lets add a flow to the switch!

# Construct the flow rule as a dictionary. For example:
flow_rule = {
    "dpid": switch1.DPID,
    "idle_timeout": 30, "hard_timeout": 30, "priority": 100,
    "match":{ "in_port":1 },
    "actions":[{ "type":"OUTPUT", "port": 2 }]
}

# Now call the add_flow() method and pass the flow rule dictionary as an argument:
switch1.add_flow( flow_rule )

# Dump the flow table again to see the new flow added:
print "\nGET UPDATED FLOW TABLE FROM SWITCH:"
print switch1.get_flows()
