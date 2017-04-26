#####################################################
##               RYU SDN CONTROLLER                ##
##      PYTHON LIBRARY FOR NORTHBOUND REST API     ##
##            OBJECT-ORIENTATED MODULE             ##
##                     v1.0.0                      ##
#####################################################

# Copyright 2017 Nathan Catania
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


### RYU REST API DOCUMENTATION ###
#   http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html

### ABOUT ###
#   This a Python module that provides easy, Object-Orientated access to the Ryu REST API.
#   The module uses the Requests framework to interact with the RYU REST API.
#   For a functional approach, use the ryurest.py module which allows you to call the methods directly.

### REQUIREMENTS ###
#   "Requests" library: http://docs.python-requests.org/en/master/
#   Install using: pip install requests

### INSTALLATION ###
#   Place this file at the root of your project. PIP support is WIP.

### USAGE INSTRUCTIONS ###
#   1. Import this module and the RyuSwitch class into your script. For example:
#      >> from ryu_switch import RyuSwitch
#
#   2. Create one or more RyuSwitch objects. See demos/OO_demo.py for more info.
#        >> switch1 = RyuSwitch( DPID )
#
#        * If you do not know any of the DPIDs of the connected switches, you can initialize with no arguments:
#            >> switch0 = RyuSwitch()
#        * Call the .get_switches() method to return a list of DPIDs:
#            >> DPID_list = switch0.get_switches()
#        * Be sure to assign any object created in this way a DPID manually:
#            >> switch0.DPID = DPID_list[0]
#
#   3. [OPTIONAL] The default location for the Ryu REST API is: http://localhost:8080
#      * If Ryu is running on this PC (localhost), then there is no need to change anything.
#      * If the Ryu controller is running on a different machine and/or port, you MUST set the API path within each RyuSwitch object created.
#      * For example:
#           >> switch1 = RyuSwitch( DPID )
#           >> switch1.API = "http://192.168.1.30:8080"
#           >> switch2 = RyuSwitch( DPID )
#           >> switch2.API = "http://192.168.1.30:8080"
#           (WARNING: If altering the API path, DO NOT add a trailing '/' at the end or the API call will fail!)
#
#   4. Execute the class methods as required. Example:
#           >> flows = switch1.get_flows()
#      * Some methods have optional filters as well. Consult the ryu_switch.py module or the Ryu REST API documentation for more info.
#
#   5. Return Formats
#       * If successful...
#           * All the .get_x() methods will return JSON formatted data; EXCEPT .get_switches() which will return an array of DPIDs.
#           * All the .set_x(), .delete_x(), .modify_X() methods will return boolean True.
#       * If unsuccessful...
#           * ALL methods will return boolean False.




# Use Requests library (required)
import requests

class RyuSwitch(object):

    def __init__(self, DPID=None):
        # Set switch DPID
        self.DPID = DPID

        ### Base REST API URI ###
        # DO NOT alter this path in this file unless you know what you are doing!
        # Warning: DO NOT add a trailing '/' at the end or API will fail.
        self.API = "http://localhost:8080"



    #########################################
    ###     GET DATA FROM THE SWITCH      ###
    #########################################

    ###### Retrieve Switch Information ######

    ## Get DPIDs of all switches ##
    def get_switches(self):

        '''
        Description:
        Get the list of all switch DPIDs that are connected to the controller.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-all-switches

        Arguments:
        None.

        Return value:
        Returns an ARRAY of Datapath IDs (DPID) - one for each connected switch.

        Usage:
        R = RyuSwitch()
        content = R.list_switches()
        print content[0]
        '''

        # Path: /stats/switches
        rest_uri = self.API + "/stats/switches"

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return r.json()
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## Get hardware stats of the switch ##
    def get_stats(self):

        '''
        Description:
        Get the desc stats of the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-the-desc-stats

        Arguments:
        Datapath ID (DPID) of the target switch.

        Return value:
        JSON structure containing information about the switch hardware.

        Usage:
        R = RyuSwitch()
        content = R.get_switch_stats('123917682136708')
        print content
        {
          "123917682136708": {
            "mfr_desc": "Nicira, Inc.",
            "hw_desc": "Open vSwitch",
            "sw_desc": "2.3.90",
            "serial_num": "None",
            "dp_desc": "None"
          }
        }
        '''

        # Path: /stats/desc/<DPID>
        rest_uri = self.API + "/stats/desc/" + str(self.DPID)

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return r.json()
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ###### Retrieve Flow Information ######

    ## Get the flow table of a specified switch (DPID). Optionally give a filter. ##
    def get_flows(self, filters={}):

        '''
        Description:
        Get all flows stats of the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-all-flows-stats

        Arguments:
        DPID: Datapath ID (DPID) of the target switch.
        filter: [OPTIONAL] dictionary to filter the results returned. See above link.

        Return value:
        JSON structure containing the flows in the flow table.

        Usage:
        R = RyuSwitch()
        content = R.get_flows('123917682136708')
        print content      # See link for output and field descriptions
        '''

        # Path: /stats/flow/<DPID>
        rest_uri = self.API + "/stats/flow/" + str(self.DPID)

        # If no filter defined, use GET. If filter defined, use POST.
        if not filters:
            # No filter specified, dump ALL flows.
            # Make call to REST API (GET)
            r = requests.get(rest_uri)

            # Ryu returns HTTP 200 status if successful
            if r.status_code == 200:
                return r.json()
            else:
                return False
                # If submission fails, Ryu returns HTTP 400 status.
                # Catch all for HTTP errors.
        else:
            # Filter is present, dump only matched flows.
            # Make call to REST API (POST)
            r = requests.post(rest_uri, data=filters)

            # Ryu returns HTTP 200 status if successful
            if r.status_code == 200:
                return r.json()
            else:
                return False
                # If submission fails, Ryu returns HTTP 400 status.
                # Catch all for HTTP errors.



    ## Get the aggregated stats of the specified switch's flow table. Optionally give a filter. ##
    def get_flow_stats(self, filters={}):

        '''
        Description:
        Get aggregate flow stats of the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-aggregate-flow-stats

        Arguments:
        DPID: Datapath ID (DPID) of the target switch.
        filter: [OPTIONAL] dictionary to filter the results returned. See above link.

        Return value:
        JSON structure containing the aggregated flow stats.

        Usage:
        R = RyuSwitch()
        content = R.get_flow_stats('123917682136708')
        print content      # See link for output and field descriptions
        '''

        # Path: /stats/aggregateflow/<DPID>
        rest_uri = self.API + "/stats/aggregateflow/" + str(self.DPID)

        # If no filter defined, use GET. If filter defined, use POST.
        if not filters:
            # No filter specified, dump ALL flows.
            # Make call to REST API (GET)
            r = requests.get(rest_uri)

            return r.json()
        else:
            # Filter is present, dump only matched flows.
            # Make call to REST API (POST)
            r = requests.post(rest_uri, data=filters)

            return r.json()



    ###### Retrieve Flow Table Information ######

    ## Get statistics for all flow tables for a switch DPID ##
    def get_table_stats(self):

        '''
        Description:
        Get table stats of the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-table-stats

        Arguments:
        Datapath ID (DPID) of the target switch.

        Return value:
        JSON structure containing information and stats for EVERY flow table on the specified switch.

        Usage:
        R = RyuSwitch()
        content = R.get_table_stats('123917682136708')
        print content     # See link for output and field descriptions
        '''

        # Path: /stats/table/<DPID>
        rest_uri = self.API + "/stats/table/" + str(self.DPID)

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return r.json()
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    def get_table_features(self):

        '''
        Description:
        Get table features of the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-table-features

        Arguments:
        Datapath ID (DPID) of the target switch.

        Return value:
        JSON structure containing feature information for EVERY flow table on the specified switch.

        Usage:
        R = RyuSwitch()
        content = R.get_table_features('123917682136708')
        print content     # See link for output and field descriptions
        '''

        # Path: /stats/tablefeatures/<DPID>
        rest_uri = self.API + "/stats/tablefeatures/" + str(self.DPID)

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return r.json()
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ###### Retrieve Port Information ######

    ## ##
    def get_port_stats(self, port=None):

        '''
        Description:
        Get ports stats of the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-ports-stats

        Arguments:
        DPID: Datapath ID (DPID) of the target switch.
        port: [OPTIONAL] Specific port# to grab stats for. If not specfied, info for all ports is returned.

        Return value:
        JSON structure containing the port statistics. See link above for description of stats.

        Usage:
        R = RyuSwitch()
        content = R.get_port_stats('123917682136708', 3)    # Will get stats for ONLY Port #3.
        content = R.get_port_stats('123917682136708')       # Will get stats for ALL ports

        ****** KNOWN ISSUES ******
        Specifying a specific port crashes the switch - this is a FW issue. Awaiting patch.
        Workaround: Parse port info using lookup/JSON module on method return.
        '''

        # Path: /stats/port/<DPID>[/portnumber]
        rest_uri = self.API + "/stats/port/" + str(self.DPID)

        ########## SPECIFYING A PORT IS DISABLED DUE TO BUG ##########
        # # If ID is specified to filter/match results, alter URI accordingly.
        # if port is not None:
        #     # Modify URI to filter port
        #     rest_uri = rest_uri + '/' + str(port)

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return r.json()
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    def get_port_description(self, port=None, openflow=None):

        '''
        Description:
        Get ports description of the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-ports-description

        Arguments:
        DPID: Datapath ID (DPID) of the target switch.
        port: [OPTIONAL] Specific port# to grab description for. If not specfied, info for all ports is returned. (Restricted to OpenFlow v1.5+)

        Return value:
        JSON structure containing the port decriptions. See link above for example message body.

        Usage:
        R = RyuSwitch()
        content = R.get_port_description('123917682136708', 3)    # Will get desc for ONLY Port #3. Switch must be OpenFlow v1.5+
        content = R.get_port_description('123917682136708')       # Will get desc for ALL ports. OpenFlow v1.0+

        Restrictions:
        Specifying a specific port is limited to OpenFlow v1.5 and later.
        '''

        # Path: /stats/portdesc/<DPID>[/portnumber] (Port number usage restricted to OpenFlow v1.5+)
        rest_uri = self.API + "/stats/portdesc/" + str(self.DPID)

        if port is not None and openflow is None:
            print "[ WARNING ]: Port filter specified, but OpenFlow version was not. Filtering is only compatible with OpenFlow v1.5+. Defaulting to no filter & dumping all ports."
        elif port is not None and openflow < 1.5:
            print "[ WARNING ]: Port filter specified, but REST API does not allow filtering with specified OpenFlow version (v" + str(openflow) + "). Filtering is only compatible with OpenFlow v1.5+. Defaulting to no filter & dumping all ports."
        elif port is not None and openflow >= 1.5:
            # If ID is specified to filter/match results, and compatible OpenFlow version...
            # Modify URI to filter port
            rest_uri = rest_uri + '/' + str(port)

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return r.json()
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ###### Retrieve Queue Information ######

    ## ##
    def get_queue_stats(self, port=None, queue=None):

        '''
        Description:
        Get queues stats of the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-queues-stats

        Arguments:
        DPID: Datapath ID (DPID) of the target switch.
        port: [OPTIONAL] Specific port# to grab queue stats for.
        queue: [OPTIONAL] Specific Queue ID# to grab stats for. If not specified, get all Queue IDs. If no port specified, will return stats for Queue ID matched on ALL ports.

        Return value:
        JSON structure containing the queue stats of specified ports. See link above for example message body.

        Usage:
        R = RyuSwitch()
        content = R.get_queue_stats('123917682136708', port=3, queue=1)    # Will get stats for Queue ID == '1' on Port #3 only.
        content = R.get_queue_stats('123917682136708', port=3)        # Will get stats for ALL Queue IDs on Port #3 only.
        content = R.get_queue_stats('123917682136708', queue=1)       # Will get stats for Queue ID == '1' on ALL ports.
        content = R.get_queue_stats('123917682136708')                # Will get stats for ALL Queue IDs on ALL ports.
        '''

        # Path: /stats/queue/<DPID>[/portnumber[/<queue_id>]]
        rest_uri = self.API + "/stats/queue/" + str(self.DPID)

        # Set URI based on which parameters/filters have been passed in
        if any(arg is None for arg in [port, queue]):
            # Only one of either queueID# or port# has been specified...

            if port is not None:
                # Port# has been specified. QueueID# has NOT been specified. Dump ALL queue stats for specified port.

                # Modify URI to filter port only
                    # Example (DPID == 1, Port == 2): http://localhost:8080/stats/queuedesc/1/2
                rest_uri = rest_uri + '/' + str(port)

            elif queue is not None:
                # QueueID has been specified. Port# has NOT been specified. Dump matched QueueID for ALL ports.

                # Modify URI to filter QueueID only
                    # Example (DPID == 1, QueueID == 4): http://localhost:8080/stats/queuedesc/1/ALL/4
                rest_uri = rest_uri + '/ALL/' + str(queue)

        elif all(arg is not None for arg in [port, queue]):
            # Both Port# AND QueueID have been specified. Dump required data only.

            # Modify URI to filter both Port# and QueueID#
                # Example (DPID == 1, Port == 2, QueueID == 4): http://localhost:8080/stats/queuedesc/1/2/4
            rest_uri = rest_uri + '/' + str(port) + '/' + str(queue)

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return r.json()
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    # OPENFLOW v1.0-1.3 ONLY
    def get_queue_config(self, port=None):

        '''
        Description:
        Get queues config of the switch which specified with Datapath ID and Port in URI. OpenFlow v1.0 - v1.3 ONLY.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-queues-config

        Arguments:
        DPID: Datapath ID (DPID) of the target switch.
        port: [OPTIONAL] Specific port# to queue config for. If not specfied, info for all ports is returned.

        Return value:
        JSON structure containing the queue config. See link above for example message body.

        Usage:
        R = RyuSwitch()
        content1 = R.get_queue_config('123917682136708', 3)    # Will get queue config for ONLY Port #3.
        content1 = R.get_queue_config('123917682136708')       # Will get queue config for ALL ports.

        Restrictions:
        This API is depreciated in OpenFlow v1.4+. For v1.4+, use: get_queue_description()
        '''

        # Path: /stats/queueconfig/<DPID>[/portnumber] (API is DEPRECIATED in OpenFlow v1.4+)
        rest_uri = self.API + "/stats/queueconfig/" + str(self.DPID)

        # If ID is specified to filter/match results, alter URI accordingly.
        if port is not None:
            # Modify URI to filter port
            rest_uri = rest_uri + '/' + str(port)

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return r.json()
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    # OPENFLOW v1.4+ ONLY
    def get_queue_description(self, port=None, queue=None):

        '''
        Description:
        Get queues description of the switch which specified with Datapath ID, Port and Queue_id in URI. OpenFlow v1.4+ ONLY.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-queues-description

        Arguments:
        DPID: Datapath ID (DPID) of the target switch.
        port: [OPTIONAL] Specific port# to grab queue descriptions for.
        queue: [OPTIONAL] Specific Queue ID# to grab desc for. If not specified, get desc for ALL Queue IDs. If no port specified, will return desc for Queue ID matched on ALL ports.

        Return value:
        JSON structure containing queue descriptions on specified ports. See link above for example message body.

        Usage:
        R = RyuSwitch()
        content = R.get_queue_description('123917682136708', port=3, queue=1)    # Will get desc for Queue ID == '1' on Port #3 only.
        content = R.get_queue_description('123917682136708', port=3)        # Will get desc for ALL Queue IDs on Port #3 only.
        content = R.get_queue_description('123917682136708', queue=1)       # Will get desc for Queue ID == '1' on ALL ports.
        content = R.get_queue_description('123917682136708')                # Will get desc for ALL Queue IDs on ALL ports.

        Restrictions:
        This API is only compatible with OpenFlow v1.4+. For v1.0 - v1.3, use: get_queue_config()
        '''

        # Path: /stats/queuedesc/<DPID>[/portnumber[/<queue_id>]]
        rest_uri = self.API + "/stats/queuedesc/" + str(self.DPID)

        # Set URI based on which parameters/filters have been passed in
        if any(arg is None for arg in [port, queue]):
            # Only one of either queueID# or port# has been specified...

            if port is not None:
                # Port# has been specified. QueueID# has NOT been specified. Dump ALL queue descriptions for specified port.

                # Modify URI to filter port only
                    # Example (DPID == 1, Port == 2): http://localhost:8080/stats/queuedesc/1/2
                rest_uri = rest_uri + '/' + str(port)

            elif queue is not None:
                # QueueID has been specified. Port# has NOT been specified. Dump matched QueueID for ALL ports.

                # Modify URI to filter QueueID only
                    # Example (DPID == 1, QueueID == 4): http://localhost:8080/stats/queuedesc/1/ALL/4
                rest_uri = rest_uri + '/ALL/' + str(queue)

        elif all(arg is not None for arg in [port, queue]):
            # Both Port# AND QueueID have been specified. Dump required data only.

            # Modify URI to filter both Port# and QueueID#
                # Example (DPID == 1, Port == 2, QueueID == 4): http://localhost:8080/stats/queuedesc/1/2/4
            rest_uri = rest_uri + '/' + str(port) + '/' + str(queue)

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return r.json()
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ###### Retrieve Group Information ######

    ## ##
    def get_group_stats(self, group=None):

        '''
        Description:
        Get groups stats of the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-groups-stats

        Arguments:
        DPID: Datapath ID (DPID) of the target switch.
        group: [OPTIONAL] Specific groupID# to grab stats for. If not specfied, info for all groups are returned.

        Return value:
        JSON structure containing the group statistics. See link above for description of stats.

        Usage:
        R = RyuSwitch()
        content = R.get_group_stats('123917682136708', 3)    # Will get stats for ONLY group #3.
        content = R.get_group_stats('123917682136708')       # Will get stats for ALL groups
        '''

        # Path: /stats/group/<DPID>[/portnumber]
        rest_uri = self.API + "/stats/group/" + str(self.DPID)

        # If ID is specified to filter/match results, alter URI accordingly.
        if group is not None:
            # Modify URI to filter meters
            rest_uri = rest_uri + '/' + str(group)

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return r.json()
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    def get_group_description(self, port=None, openflow=None):

        '''
        Description:
        Get group description stats of the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-group-description-stats

        Arguments:
        DPID: Datapath ID (DPID) of the target switch.
        port: [OPTIONAL] Specific group# to grab description for. If not specfied, info for all groups is returned. (Restricted to OpenFlow v1.5+)

        Return value:
        JSON structure containing the group decription. See link above for example message body.

        Usage:
        R = RyuSwitch()
        content = R.get_group_description('123917682136708', 3)    # Will get desc for ONLY Group ID #3. Switch must be OpenFlow v1.5+
        content = R.get_group_description('123917682136708')       # Will get desc for ALL groups. OpenFlow v1.0 - v1.4

        Restrictions:
        Specifying a specific groupID is limited to OpenFlow v1.5 and later.
        '''

        # Path: /stats/groupdesc/<DPID>[/portnumber] (Port number usage restricted to OpenFlow v1.5+)
        rest_uri = self.API + "/stats/groupdesc/" + str(self.DPID)

        if port is not None and openflow is None:
            print "[ WARNING ]: Port filter specified, but OpenFlow version was not. Filtering is only compatible with OpenFlow v1.5+. Defaulting to no filter & dumping all ports."
        elif port is not None and openflow < 1.5:
            print "[ WARNING ]: Port filter specified, but REST API does not allow filtering with specified OpenFlow version (v" + str(openflow) + "). Filtering is only compatible with OpenFlow v1.5+. Defaulting to no filter & dumping all ports."
        elif port is not None and openflow >= 1.5:
            # If ID is specified to filter/match results, and compatible OpenFlow version...
            # Modify URI to filter port
            rest_uri = rest_uri + '/' + str(port)

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return r.json()
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    def get_group_features(self):

        '''
        Description:
        Get group features stats of the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-group-features-stats

        Arguments:
        Datapath ID (DPID) of the target switch.

        Return value:
        JSON structure containing aggregated feature information for all groups on the specified switch.

        Usage:
        R = RyuSwitch()
        content = R.get_group_features('123917682136708')
        '''

        # Path: /stats/groupfeatures/<DPID>
        rest_uri = self.API + "/stats/groupfeatures/" + str(self.DPID)

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return r.json()
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ###### Retrieve Meter Information ######

    ## ##
    def get_meter_stats(self, meter=None):

        '''
        Description:
        Get meters stats of the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-meters-stats

        Arguments:
        DPID: Datapath ID (DPID) of the target switch.
        meter: [OPTIONAL] Specific meter ID# to grab stats for. If not specfied, info for all meters are returned.

        Return value:
        JSON structure containing the meter statistics. See link above for description of stats.

        Usage:
        R = RyuSwitch()
        content1 = R.get_meter_stats('123917682136708', 3)    # Will get stats for ONLY meter ID #3.
        content1 = R.get_meter_stats('123917682136708')       # Will get stats for ALL meters
        '''

        # Path: /stats/group/<DPID>[/portnumber]
        rest_uri = self.API + "/stats/meter/" + str(self.DPID)

        # If ID is specified to filter/match results, alter URI accordingly.
        if meter is not None:
            # Modify URI to filter meters
            rest_uri = rest_uri + '/' + str(meter)

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return r.json()
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    #TODO: Handle Openflow versions
    #NOTE: THIS CODE IS OK FORMAT.
    def get_meter_description(self, meter=None, openflow=1.0):

        '''
        Description:
        Get meter config stats of the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-meter-description-stats

        Arguments:
        DPID: Datapath ID (DPID) of the target switch.
        meter: [OPTIONAL] Specific meter ID# to grab description for. If not specfied, info for all meters is returned.
        openflow: [OPTIONAL] The OpenFlow version of the switch. If not specified, will default to v1.0. This method returns differently if OpenFlow version is 1.5+

        Return value:
        JSON structure containing the meter decriptions. See link above for example message body.

        Usage:
        R = RyuSwitch()
        DPID = "123917682136708"
        content = R.get_meter_description(DPID, 3)    # Will get desc for Meter ID #3 ONLY. Assumes OpenFlow v1.0-1.4 for calling API.
        content = R.get_meter_description(DPID)       # Will get desc for ALL meters. Assumes OpenFlow v1.0-1.4 for calling API.
        content = R.get_meter_description(DPID, meter=3, openflow=1.5)   # Will get desc for Meter ID #3. Runs API call for Openflow 1.5+.

        Restrictions:
        API URI was renamed for OpenFlow v1.5+ :
        /stats/meterconfig/<dpid>[/<meter_id>] - OpenFlow 1.0 - 1.4
        /stats/meterdesc/<dpid>[/<meter_id>]   - OpenFlow 1.5+
        Pass in OpenFlow version as argument if using 1.5+, else method will execute v1.0-1.4 call.
        '''

        # Set URI based on OpenFlow version
        if openflow < 1.5:
            # OpenFlow v1.0 - 1.4
            # REST API path: /stats/meterconfig/<dpid>[/<meter_id>]
            rest_uri = self.API + "/stats/meterconfig/" + str(self.DPID)
        else:
            # OpenFlow v1.5+
            # REST API path: /stats/meterdesc/<dpid>[/<meter_id>]
            rest_uri = self.API + "/stats/meterdesc/" + str(self.DPID)

        # If ID is specified to filter/match results, alter URI accordingly.
        if meter is not None:
            # Modify URI to filter meters
            rest_uri = rest_uri + '/' + str(meter)   # TODO: Add try/catch in case meter does not exist.

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return r.json()
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    def get_meter_features(self):

        '''
        Description:
        Get meter features stats of the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-meter-features-stats

        Arguments:
        Datapath ID (DPID) of the target switch.

        Return value:
        JSON structure containing aggregated feature information for all meters on the specified switch.

        Usage:
        R = RyuSwitch()
        content = R.get_meter_features('123917682136708')
        '''

        # Path: /stats/meterfeatures/<DPID>
        rest_uri = self.API + "/stats/meterfeatures/" + str(self.DPID)

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return r.json()
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ###### Retrieve Controller Information ######

    ## ##
    def get_role(self):

        '''
        Description:
        Get the current role of the controller from the switch.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-role

        Arguments:
        Datapath ID (DPID) of the target switch.

        Return value:
        JSON structure containing the role information of the controller in respect to the switch.

        Usage:
        R = RyuSwitch()
        content = R.get_role('123917682136708')

        ****** KNOWN ISSUES ******
        Calling this REST API returns a 404 error which indicates the API does not exist in RYU.
        '''
        # This method is currently disabled due to RYU bug in REST API (404 error)
        return None

        # # Path: /stats/role/<DPID>
        # rest_uri = self.API + "/stats/role/" + str(self.DPID)
        #
        # # Make call to REST API (GET)
        # r = requests.get(rest_uri)
        #
        # # Ryu returns HTTP 200 status if successful
        # if r.status_code == 200:
        #     return r.json()
        # else:
        #     return False
        #     # If submission fails, Ryu returns HTTP 400 status.
        #     # Catch all for HTTP errors.



    #########################################
    ###       SET DATA ON THE SWITCH      ###
    #########################################

    ###### Modify Flow Entries ######

    ## ##
    def add_flow(self, payload):

        '''
        Description:
        Add a flow entry to the switch.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#add-a-flow-entry

        Arguments:
        payload: Data payload containing flow information to add to the flowtable.

        Payload structure:
        Dictionary format. DPID of target is specified in payload. Example:
            payload = {
                "dpid": 123456789, "cookie": 1, "cookie_mask": 1, "table_id": 0,
                "idle_timeout": 30, "hard_timeout": 30, "priority": 100,
                "flags": 1, "match":{ "in_port":1 },
                "actions":[{ "type":"OUTPUT", "port": 2 }]
             }
         See link for details on how to construct payload.

        Return value:
        Boolean. True if successful, False if error.

        Usage:
        R = RyuSwitch()
        R.add_flow(payload)   # Use if statement to check if successful.
        '''

        # Path: /stats/flowentry/add
        rest_uri = self.API + "/stats/flowentry/add"

        # Make call to REST API (POST)
        r = requests.post(rest_uri, json=payload) # payload encoded to JSON

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return True
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    def modify_flow(self, payload):

        '''
        Description:
        Modify ** ALL ** matching flow entries of the switch.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#modify-all-matching-flow-entries

        Arguments:
        payload: Data payload containing flow information to match and modify.

        Payload structure:
        Dictionary format. DPID of target is specified in payload. Example:
            payload = {
                "dpid": 123456789, "cookie": 1, "cookie_mask": 1, "table_id": 0,
                "idle_timeout": 30, "hard_timeout": 30, "priority": 100,
                "flags": 1, "match":{ "in_port":1 },
                "actions":[{ "type":"OUTPUT", "port": 2 }]
             }
        See link for details on how to construct payload.

        Return value:
        Boolean. True if successful, False if error.

        Usage:
        R = RyuSwitch()
        R.modify_flow(payload)   # Use if statement to check if successful.
        '''

        # Path: /stats/flowentry/modify
        rest_uri = self.API + "/stats/flowentry/modify"

        # Make call to REST API (POST)
        r = requests.post(rest_uri, json=payload) # payload encoded to JSON

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return True
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    def modify_flow_strict(self, payload):

        '''
        Description:
        Modify flow entry strictly matching wildcards and priority

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#modify-flow-entry-strictly

        Arguments:
        payload: Data payload containing flow information to match and modify.

        Payload structure:
        Dictionary format. DPID of target is specified in payload. Example:
            payload = {
                "dpid": 123456789, "cookie": 1, "cookie_mask": 1, "table_id": 0,
                "idle_timeout": 30, "hard_timeout": 30, "priority": 100,
                "flags": 1, "match":{ "in_port":1 },
                "actions":[{ "type":"OUTPUT", "port": 2 }]
            }
        See link for details on how to construct payload.

        Return value:
        Boolean. True if successful, False if error.

        Usage:
        R = RyuSwitch()
        R.modify_flow_strict(payload)   # Use if statement to check if successful.
        '''

        # Path: /stats/flowentry/modify_strict
        rest_uri = self.API + "/stats/flowentry/modify_strict"

        # Make call to REST API (POST)
        r = requests.post(rest_uri, json=payload) # payload encoded to JSON

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return True
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    def delete_flow(self, payload):

        '''
        Description:
        Delete ** ALL ** matching flow entries of the switch.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#delete-all-matching-flow-entries

        Arguments:
        payload: Data payload containing flow information to match and delete.

        Payload structure:
        Dictionary format. DPID of target is specified in payload. Example:
            payload = {
                "dpid": 123456789, "cookie": 1, "cookie_mask": 1, "table_id": 0,
                "idle_timeout": 30, "hard_timeout": 30, "priority": 100,
                "flags": 1, "match":{ "in_port":1 },
                "actions":[{ "type":"OUTPUT", "port": 2 }]
            }
        See link for details on how to construct payload.

        Return value:
        Boolean. True if successful, False if error.

        Usage:
        R = RyuSwitch()
        R.delete_flow(payload)   # Use if statement to check if successful.
        '''

        # Path: /stats/flowentry/modify_strict
        rest_uri = self.API + "/stats/flowentry/delete"

        # Make call to REST API (POST)
        r = requests.post(rest_uri, json=payload) # payload encoded to JSON

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return True
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    def delete_flow_strict(self, payload):

        '''
        Description:
        Delete flow entry strictly matching wildcards and priority.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#delete-flow-entry-strictly

        Arguments:
        payload: Data payload containing flow information to match and delete.

        Payload structure:
        Dictionary format. DPID of target is specified in payload. Example:
            payload = {
                "dpid": 123456789, "cookie": 1, "cookie_mask": 1, "table_id": 0,
                "idle_timeout": 30, "hard_timeout": 30, "priority": 100,
                "flags": 1, "match":{ "in_port":1 },
                "actions":[{ "type":"OUTPUT", "port": 2 }]
            }
        See link for details on how to construct payload.

        Return value:
        Boolean. True if successful, False if error.

        Usage:
        R = RyuSwitch()
        R.delete_flow_strict(payload)   # Use if statement to check if successful.
        '''

        # Path: /stats/flowentry/modify_strict
        rest_uri = self.API + "/stats/flowentry/delete_strict"

        # Make call to REST API (POST)
        r = requests.post(rest_uri, json=payload) # payload encoded to JSON

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return True
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    def delete_flow_all(self):

        '''
        Description:
        Delete ** ALL ** flow entries of the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#delete-flow-entry-strictly

        Arguments:
        DPID: Datapath ID (DPID) of the target switch.

        Return value:
        Boolean. True if successful, False if error.

        Usage:
        R = RyuSwitch()
        R.delete_flow_all(DPID)   # Use if statement to check if successful.
        '''

        # Path: /stats/flowentry/modify_strict
        rest_uri = self.API + "/stats/flowentry/clear/" + str(self.DPID)

        # Make call to REST API (DELETE)
        r = requests.delete(rest_uri)

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return True
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ###### Modify Group Entries ######

    ## ##
    def add_group(self, payload):

        '''
        Description:
        Add a group entry to the switch.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#add-a-group-entry

        Arguments:
        payload: Data payload containing group information to add to the switch.

        Payload structure:
        Dictionary format. DPID of target is specified in payload. Example:
            payload = {
                "dpid": 123456789, "type": "ALL", "group_id": 1,
                "buckets": [{
                        "actions": [{
                                "type": "OUTPUT",
                                "port": 1
                            }] }]
            }
        See link for details on how to construct payload.

        Return value:
        Boolean. True if successful, False if error.

        Usage:
        R = RyuSwitch()
        R.add_group(payload)   # Use if statement to check if successful.
        '''

        # Path: /stats/groupentry/add
        rest_uri = self.API + "/stats/groupentry/add"

        # Make call to REST API (POST)
        r = requests.post(rest_uri, json=payload) # payload encoded to JSON

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return True
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    def modify_group(self, payload):

        '''
        Description:
        Modify a group entry to the switch.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#modify-a-group-entry

        Arguments:
        payload: Data payload containing group information to match and modify.

        Payload structure:
        Dictionary format. DPID of target is specified in payload. Example:
            payload = {
                "dpid": 123456789, "type": "ALL", "group_id": 1,
                "buckets": [{
                        "actions": [{
                                "type": "OUTPUT",
                                "port": 1
                            }] }]
            }
        See link for details on how to construct payload.

        Return value:
        Boolean. True if successful, False if error.

        Usage:
        R = RyuSwitch()
        R.modify_group(payload)   # Use if statement to check if successful.
        '''

        # Path: /stats/groupentry/modify
        rest_uri = self.API + "/stats/groupentry/modify"

        # Make call to REST API (POST)
        r = requests.post(rest_uri, json=payload) # payload encoded to JSON

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return True
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    def delete_group(self, payload):

        '''
        Description:
        Delete a group entry to the switch.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#delete-a-group-entry

        Arguments:
        payload: Data payload containing group information to match and delete.

        Payload structure:
        Dictionary format. DPID of target is specified in payload. Example:
            payload = {
                "dpid": 123456789, "group_id": 1,
            }

        Return value:
        Boolean. True if successful, False if error.

        Usage:
        R = RyuSwitch()
        R.delete_group(payload)   # Use if statement to check if successful.
        '''

        # Path: /stats/groupentry/delete
        rest_uri = self.API + "/stats/groupentry/delete"

        # Make call to REST API (POST)
        r = requests.post(rest_uri, json=payload) # payload encoded to JSON

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return True
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ###### Modify Port Entries ######

    ## ##
    def modify_port(self, payload):

        '''
        Description:
        Modify the behavior of the physical port.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#modify-the-behavior-of-the-port

        Arguments:
        payload: Data payload containing port information to modify.

        Payload structure:
        Dictionary format. DPID of target is specified in payload. Example:
            payload = {
                "dpid": 123456789, "port_no": 1, "config": 1, "mask": 1
            }
        See link for details on how to construct payload.

        Return value:
        Boolean. True if successful, False if error.

        Usage:
        R = RyuSwitch()
        R.modify_port(payload)   # Use if statement to check if successful.
        '''

        # Path: /stats/portdesc/modify
        rest_uri = self.API + "/stats/portdesc/modify"

        # Make call to REST API (POST)
        r = requests.post(rest_uri, json=payload) # payload encoded to JSON

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return True
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ###### Modify Meter Entries ######

    ## ##
    def add_meter(self, payload):

        '''
        Description:
        Add a meter entry to the switch.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#add-a-meter-entry

        Arguments:
        payload: Data payload containing meter information to add to the switch.

        Payload structure:
        Dictionary format. DPID of target is specified in payload. Example:
            payload = {
                "dpid": 123456789, "flags": "KBPS", "meter_id": 1,
                "bands": [{
                    "type": "DROP", "rate": 1000
                }]
            }
        See link for details on how to construct payload.

        Return value:
        Boolean. True if successful, False if error.

        Usage:
        R = RyuSwitch()
        R.add_meter(payload)   # Use if statement to check if successful.
        '''

        # Path: /stats/meterentry/add
        rest_uri = self.API + "/stats/meterentry/add"

        # Make call to REST API (POST)
        r = requests.post(rest_uri, json=payload) # payload encoded to JSON

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return True
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    def modify_meter(self, payload):

        '''
        Description:
        Modify a meter entry to the switch.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#modify-a-meter-entry

        Arguments:
        payload: Data payload containing meter information to match and modify.

        Payload structure:
        Dictionary format. DPID of target is specified in payload. Example:
            payload = {
                "dpid": 123456789, "flags": "KBPS", "meter_id": 1,
                "bands": [{
                    "type": "DROP", "rate": 1000
                }]
            }
        See link for details on how to construct payload.

        Return value:
        Boolean. True if successful, False if error.

        Usage:
        R = RyuSwitch()
        R.modify_meter(payload)   # Use if statement to check if successful.
        '''

        # Path: /stats/meterentry/modify
        rest_uri = self.API + "/stats/meterentry/modify"

        # Make call to REST API (POST)
        r = requests.post(rest_uri, json=payload) # payload encoded to JSON

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return True
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ## ##
    def delete_meter(self, payload):

        '''
        Description:
        Delete a meter entry to the switch.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#delete-a-meter-entry

        Arguments:
        payload: Data payload containing meter information to match and delete.

        Payload structure:
        Dictionary format. DPID of target is specified in payload. Example:
            payload = {
                "dpid": 123456789, "meter_id": 1,
            }

        Return value:
        Boolean. True if successful, False if error.

        Usage:
        R = RyuSwitch()
        R.delete_meter(payload)   # Use if statement to check if successful.
        '''

        # Path: /stats/meterentry/delete
        rest_uri = self.API + "/stats/meterentry/delete"

        # Make call to REST API (POST)
        r = requests.post(rest_uri, json=payload) # payload encoded to JSON

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return True
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    ###### Modify Controller Role ######

    ## ##
    def modify_role(self, payload):

        '''
        Description:
        Modify the role of the switch.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#modify-role

        Arguments:
        payload: Data payload containing role information to modify.

        Payload structure:
        Dictionary format. DPID of target is specified in payload. Example:
            payload = {
                "dpid": 123456789, "role": "MASTER",
            }

        Return value:
        Boolean. True if successful, False if error.

        Usage:
        R = RyuSwitch()
        R.set_role(payload)   # Use if statement to check if successful.
        '''

        # Path: /stats/role
        rest_uri = self.API + "/stats/role"

        # Make call to REST API (POST)
        r = requests.post(rest_uri, json=payload) # payload encoded to JSON

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return True
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.



    #########################################
    ###        EXPERIMENTER SUPPORT       ###
    #########################################

    ###### Send a experimenter message ######

    ## ##
    def send_experimenter(self, payload):

        '''
        Description:
        Send a experimenter message to the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#send-a-experimenter-message

        Arguments:
        DPID: Datapath ID (DPID) of the target switch.
        payload: payload: Data payload containing the experimenter message to send.

        Payload structure:
        Dictionary format. DPID of target is specified in payload. Example:
            payload = {
                "dpid": 123456789, "experimenter": 1, "exp_type": 1,
                "data_type": "ascii", "data": "Hello world!"
             }
        See link for details on how to construct payload.

        Return value:
        Boolean. True if successful, False if error.

        Usage:
        R = RyuSwitch()
        R.add_flow(payload)   # Use if statement to check if successful.
        '''

        # Path: /stats/experimenter/<dpid>
        rest_uri = self.API + "/stats/flowentry/add/" + str(self.DPID)

        # Make call to REST API (POST)
        r = requests.post(rest_uri, json=payload) # payload encoded to JSON

        # Ryu returns HTTP 200 status if successful
        if r.status_code == 200:
            return True
        else:
            return False
            # If submission fails, Ryu returns HTTP 400 status.
            # Catch all for HTTP errors.
