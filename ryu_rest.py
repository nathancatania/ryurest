#!/usr/bin/env python
import requests
import sys

import json

# From docs: http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html



class ryuRest(object):


    def __init__(self):
        # Base REST API URI
        self.API = "http://localhost:8080"

        # DEBUG MODE
        self.debug = False
        # Set debug mode (dump REST URI + content)
        if len(sys.argv) > 1:
            if sys.argv[1] == "debug":
                self.debug = True


    def debug_dump(self, rest_uri, r, title=None):
        if title is not None:
            print "#### " + title + " ####"
        print "REST URI:"
        print rest_uri
        print "OUTPUT:"
        print str(r.json()) + '\n'



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
        R = ryuRest()
        content = R.list_switches()
        print content[0]
        '''

        # Path: /stats/switches
        rest_uri = self.API + "/stats/switches"

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # DEBUG MODE
        if self.debug: self.debug_dump(rest_uri, r, "GET SWITCH INFO")

        return r.json()



    ## Get hardware stats of a specified switch DPID ##
    def get_switch_stats(self, DPID):

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
        R = ryuRest()
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
        rest_uri = self.API + "/stats/desc/" + DPID

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # DEBUG MODE
        if self.debug: self.debug_dump(rest_uri, r, "GET SWITCH STATS")

        return r.json()



    ###### Retrieve Flow Information ######

    ## Get the flow table of a specified switch (DPID). Optionally give a filter. ##
    def get_flows(self, DPID, filters={}):

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
        R = ryuRest()
        content = R.get_flows('123917682136708')
        print content      # See link for output and field descriptions
        '''

        # Path: /stats/flow/<DPID>
        rest_uri = self.API + "/stats/flow/" + DPID

        # If no filter defined, use GET. If filter defined, use POST.
        if not filters:
            # No filter specified, dump ALL flows.
            # Make call to REST API (GET)
            r = requests.get(rest_uri)

            # DEBUG MODE
            if self.debug: self.debug_dump(rest_uri, r, "GET FLOWS")

            return r.json()
        else:
            # Filter is present, dump only matched flows.
            # Make call to REST API (POST)
            r = requests.post(rest_uri, data=filters)

            # DEBUG MODE
            if self.debug: self.debug_dump(rest_uri, r, "GET FLOWS")

            return r.json()



    ## Get the aggregated stats of the specified switch's flow table. Optionally give a filter. ##
    def get_flow_stats(self, DPID, filters={}):

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
        R = ryuRest()
        content = R.get_flow_stats('123917682136708')
        print content      # See link for output and field descriptions
        '''

        # Path: /stats/aggregateflow/<DPID>
        rest_uri = self.API + "/stats/aggregateflow/" + DPID

        # If no filter defined, use GET. If filter defined, use POST.
        if not filters:
            # No filter specified, dump ALL flows.
            # Make call to REST API (GET)
            r = requests.get(rest_uri)

            # DEBUG MODE
            if self.debug: self.debug_dump(rest_uri, r, "GET FLOW STATS")

            return r.json()
        else:
            # Filter is present, dump only matched flows.
            # Make call to REST API (POST)
            r = requests.post(rest_uri, data=filters)

            # DEBUG MODE
            if self.debug: self.debug_dump(rest_uri, r)

            return r.json()



    ###### Retrieve Flow Table Information ######

    ## Get statistics for all flow tables for a switch DPID ##
    def get_table_stats(self, DPID):

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
        R = ryuRest()
        content = R.get_table_stats('123917682136708')
        print content     # See link for output and field descriptions
        '''

        # Path: /stats/table/<DPID>
        rest_uri = self.API + "/stats/table/" + DPID

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # DEBUG MODE
        if self.debug: self.debug_dump(rest_uri, r, "GET TABLE STATS")

        return r.json()



    ## ##
    def get_table_features(self, DPID):

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
        R = ryuRest()
        content = R.get_table_features('123917682136708')
        print content     # See link for output and field descriptions
        '''

        # Path: /stats/tablefeatures/<DPID>
        rest_uri = self.API + "/stats/tablefeatures/" + DPID

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # DEBUG MODE
        if self.debug: self.debug_dump(rest_uri, r, "GET TABLE FEATURES")

        return r.json()



    ###### Retrieve Port Information ######

    ## ##
    def get_port_stats(self, DPID, port=None):

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
        R = ryuRest()
        content1 = R.get_port_stats('123917682136708', 3)    # Will get stats for ONLY Port #3.
        content1 = R.get_port_stats('123917682136708')       # Will get stats for ALL ports

        ****** KNOWN ISSUES ******
        Specifying a specific port crashes the switch - this is a FW issue. Awaiting patch.
        Workaround: Parse port info using lookup/JSON module on method return.
        '''

        # Path: /stats/port/<DPID>[/portnumber]
        rest_uri = self.API + "/stats/port/" + DPID

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # DEBUG MODE
        if self.debug: self.debug_dump(rest_uri, r, "GET PORT STATS: NO PORT SPECIFIED")

        return r.json()

        # if port is None:
        #     # No port# specified. Get info for all ports.
        #
        #     # Make call to REST API (GET)
        #     r = requests.get(rest_uri)
        #
        #     # DEBUG MODE
        #     if self.debug: self.debug_dump(rest_uri, r, "GET PORT STATS: NO PORT SPECIFIED")
        #
        #     return r.json()
        # else:
        #     # Port# has been specified. Retrieve info for this port only.
        #
        #     # Modify URI to filter port
        #     rest_uri = rest_uri + '/' + str(port)   # TODO: Add try/catch in case port does not exist.
        #
        #     # Make call to REST API (GET)
        #     r = requests.get(rest_uri)
        #
        #     # DEBUG MODE
        #     if self.debug: self.debug_dump(rest_uri, r, "GET PORT STATS: PORT #" + str(port) + " SPECIFIED")
        #
        #     return r.json()



    ## ##
    #TODO: Handle Openflow versions
    def get_port_description(self, DPID, port=None):

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
        R = ryuRest()
        content1 = R.get_port_description('123917682136708', 3)    # Will get desc for ONLY Port #3. Switch must be OpenFlow v1.5+
        content1 = R.get_port_description('123917682136708')       # Will get desc for ALL ports. OpenFlow v1.0+

        Restrictions:
        Specifying a specific port is limited to OpenFlow v1.5 and later.
        '''

        # Path: /stats/portdesc/<DPID>[/portnumber] (Port number usage restricted to OpenFlow v1.5+)
        rest_uri = self.API + "/stats/portdesc/" + DPID

        if port is None:
            # No port# specified, or OpenFlow v1.0-1.4. Get info for all ports.

            # Make call to REST API (GET)
            r = requests.get(rest_uri)

            # DEBUG MODE
            if self.debug: self.debug_dump(rest_uri, r, "GET PORT DESCRIPTION: NO PORT SPECIFIED OR OPENFLOW v1.0-1.4")

            return r.json()
        else:
            # Port# has been specified. Retrieve info for this port only.

            # Modify URI to filter port
            rest_uri = rest_uri + '/' + str(port)   # TODO: Add try/catch in case port does not exist.

            # Make call to REST API (GET)
            r = requests.get(rest_uri)

            # DEBUG MODE
            if self.debug: self.debug_dump(rest_uri, r, "GET PORT DESCRIPTION: PORT #" + str(port) + " SPECIFIED")

            return r.json()



    ###### Retrieve Queue Information ######

    ## ##
    def get_queue_stats(self, DPID, port=None, queue=None):

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
        R = ryuRest()
        content = R.get_queue_stats('123917682136708', port=3, queue=1)    # Will get stats for Queue ID == '1' on Port #3 only.
        content = R.get_queue_stats('123917682136708', port=3)        # Will get stats for ALL Queue IDs on Port #3 only.
        content = R.get_queue_stats('123917682136708', queue=1)       # Will get stats for Queue ID == '1' on ALL ports.
        content = R.get_queue_stats('123917682136708')                # Will get stats for ALL Queue IDs on ALL ports.
        '''

        # Path: /stats/queue/<DPID>[/portnumber[/<queue_id>]]
        rest_uri = self.API + "/stats/queue/" + DPID

        if all(arg is None for arg in [port, queue]):
            # No port# or queueID# specified. Dump ALL.

            # Make call to REST API (GET)
            r = requests.get(rest_uri)

            # DEBUG MODE
            if self.debug: self.debug_dump(rest_uri, r, "GET QUEUE STATS: NO PORT# OR QUEUE ID# SPECIFIED")

            return r.json()

        elif any(arg is None for arg in [port, queue]):
            # Only one of either queueID# or port# has been specified...

            if queue is None:
                # Port# has been specified. QueueID# has NOT been specified. Dump ALL queue stats for specified port.

                # Modify URI to filter port only
                    # Example (DPID == 1, Port == 2): http://localhost:8080/stats/queue/1/2
                rest_uri = rest_uri + '/' + str(port)   # TODO: Add try/catch in case port does not exist.

                # Make call to REST API (GET)
                r = requests.get(rest_uri)

                # DEBUG MODE
                if self.debug: self.debug_dump(rest_uri, r, "GET QUEUE STATS: PORT #" + str(port) + ", NO QUEUE ID# SPECIFIED")

                return r.json()
            elif port is None:
                # QueueID has been specified. Port# has NOT been specified. Dump matched QueueID for ALL ports.

                # Modify URI to filter QueueID# only
                    # Example (DPID == 1, QueueID == 4): http://localhost:8080/stats/queue/1/ALL/4
                rest_uri = rest_uri + '/ALL/' + str(queue)   # TODO: Add try/catch in case queue does not exist.

                # Make call to REST API (GET)
                r = requests.get(rest_uri)

                # DEBUG MODE
                if self.debug: self.debug_dump(rest_uri, r, "GET QUEUE STATS: QUEUE ID #" + str(queue) + ", NO PORT# SPECIFIED")

                return r.json()
        else:
            # Both Port# AND QueueID have been specified. Dump required data only.

            # Modify URI to filter both Port# and QueueID#
                # Example (DPID == 1, Port == 2, QueueID == 4): http://localhost:8080/stats/queue/1/2/4
            rest_uri = rest_uri + '/' + str(port) + '/' + str(queue)   # TODO: Add try/catch in case port and/or queue does not exist.

            # Make call to REST API (GET)
            r = requests.get(rest_uri)

            # DEBUG MODE
            if self.debug: self.debug_dump(rest_uri, r, "GET QUEUE STATS: QUEUE ID #" + str(queue) + ", PORT #" + str(port))

            return r.json()



    ## ##
    #TODO: Handle Openflow versions
    # OPENFLOW VERSION 1.0-1.3 ONLY
    def get_queue_config(self, DPID, port=None):

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
        R = ryuRest()
        content1 = R.get_queue_config('123917682136708', 3)    # Will get queue config for ONLY Port #3.
        content1 = R.get_queue_config('123917682136708')       # Will get queue config for ALL ports.

        Restrictions:
        This API is depreciated in OpenFlow v1.4+. For v1.4+, use: get_queue_description()
        '''

        # Path: /stats/queueconfig/<DPID>[/portnumber] (API is DEPRECIATED in OpenFlow v1.4+)
        rest_uri = self.API + "/stats/queueconfig/" + DPID

        if port is None:
            # No port# specified. Get queue info for all ports.

            # Make call to REST API (GET)
            r = requests.get(rest_uri)

            # DEBUG MODE
            if self.debug: self.debug_dump(rest_uri, r, "(OPENFLOW v1.0-1.3) GET QUEUE CONFIG: NO PORT SPECIFIED")

            return r.json()
        else:
            # Port# has been specified. Retrieve info for this port only.

            # Modify URI to filter port
            rest_uri = rest_uri + '/' + str(port)   # TODO: Add try/catch in case port does not exist.

            # Make call to REST API (GET)
            r = requests.get(rest_uri)

            # DEBUG MODE
            if self.debug: self.debug_dump(rest_uri, r, "(OPENFLOW v1.0-1.3) GET QUEUE CONFIG: PORT #" + str(port) + " SPECIFIED")

            return r.json()



    ## ##
    #TODO: Handle Openflow versions
    # OPENFLOW VERSION 1.4+ ONLY
    def get_queue_decription(self, DPID, port=None, queue=None):

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
        R = ryuRest()
        content = R.get_queue_description('123917682136708', port=3, queue=1)    # Will get desc for Queue ID == '1' on Port #3 only.
        content = R.get_queue_description('123917682136708', port=3)        # Will get desc for ALL Queue IDs on Port #3 only.
        content = R.get_queue_description('123917682136708', queue=1)       # Will get desc for Queue ID == '1' on ALL ports.
        content = R.get_queue_description('123917682136708')                # Will get desc for ALL Queue IDs on ALL ports.

        Restrictions:
        This API is only compatible with OpenFlow v1.4+. For v1.0 - v1.3, use: get_queue_config()
        '''

        # Path: /stats/queuedesc/<DPID>[/portnumber[/<queue_id>]]
        rest_uri = self.API + "/stats/queuedesc/" + DPID

        if all(arg is None for arg in [port, queue]):
            # No port# or queueID# specified. Dump ALL.

            # Make call to REST API (GET)
            r = requests.get(rest_uri)

            # DEBUG MODE
            if self.debug: self.debug_dump(rest_uri, r, "(OPENFLOW v1.4+) GET QUEUE DESCRIPTION: NO PORT# OR QUEUE ID# SPECIFIED")

            return r.json()

        elif any(arg is None for arg in [port, queue]):
            # Only one of either queueID# or port# has been specified...

            if queue is None:
                # Port# has been specified. QueueID# has NOT been specified. Dump ALL queue descriptions for specified port.

                # Modify URI to filter port only
                    # Example (DPID == 1, Port == 2): http://localhost:8080/stats/queuedesc/1/2
                rest_uri = rest_uri + '/' + str(port)   # TODO: Add try/catch in case port does not exist.

                # Make call to REST API (GET)
                r = requests.get(rest_uri)

                # DEBUG MODE
                if self.debug: self.debug_dump(rest_uri, r, "(OPENFLOW v1.4+) GET QUEUE DESCRIPTION: PORT #" + str(port) + ", NO QUEUE ID# SPECIFIED")

                return r.json()
            elif port is None:
                # QueueID has been specified. Port# has NOT been specified. Dump matched QueueID for ALL ports.

                # Modify URI to filter QueueID# only
                    # Example (DPID == 1, QueueID == 4): http://localhost:8080/stats/queuedesc/1/ALL/4
                rest_uri = rest_uri + '/ALL/' + str(queue)   # TODO: Add try/catch in case queue does not exist.

                # Make call to REST API (GET)
                r = requests.get(rest_uri)

                # DEBUG MODE
                if self.debug: self.debug_dump(rest_uri, r, "(OPENFLOW v1.4+) GET QUEUE DESCRIPTION: QUEUE ID #" + str(queue) + ", NO PORT# SPECIFIED")

                return r.json()
        else:
            # Both Port# AND QueueID have been specified. Dump required data only.

            # Modify URI to filter both Port# and QueueID#
                # Example (DPID == 1, Port == 2, QueueID == 4): http://localhost:8080/stats/queuedesc/1/2/4
            rest_uri = rest_uri + '/' + str(port) + '/' + str(queue)   # TODO: Add try/catch in case port and/or queue does not exist.

            # Make call to REST API (GET)
            r = requests.get(rest_uri)

            # DEBUG MODE
            if self.debug: self.debug_dump(rest_uri, r, "(OPENFLOW v1.4+) GET QUEUE DESCRIPTION: QUEUE ID #" + str(queue) + ", PORT #" + str(port))

            return r.json()



    ###### Retrieve Group Information ######

    ## ##
    def get_group_stats(self, DPID, group=None):

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
        R = ryuRest()
        content1 = R.get_group_stats('123917682136708', 3)    # Will get stats for ONLY group #3.
        content1 = R.get_group_stats('123917682136708')       # Will get stats for ALL groups
        '''

        # Path: /stats/port/<DPID>[/portnumber]
        rest_uri = self.API + "/stats/group/" + DPID

        if group is None:
            # No groupID# specified. Get info for all groups.

            # Make call to REST API (GET)
            r = requests.get(rest_uri)

            # DEBUG MODE
            if self.debug: self.debug_dump(rest_uri, r, "GET GROUP STATS: NO GROUP ID# SPECIFIED")

            return r.json()
        else:
            # GroupID# has been specified. Retrieve info for this groupID only.

            # Modify URI to filter port
            rest_uri = rest_uri + '/' + str(group)   # TODO: Add try/catch in case groupID# does not exist.

            # Make call to REST API (GET)
            r = requests.get(rest_uri)

            # DEBUG MODE
            if self.debug: self.debug_dump(rest_uri, r, "GET GROUP STATS: GROUP ID #" + str(group) + " SPECIFIED")

            return r.json()









if __name__ == "__main__":
    DPID = "123917682136708"
    R = ryuRest()

    content = R.get_switches()
    print str(content[0]) + '\n'

    R.get_switch_stats(DPID)

    R.get_flows(DPID)

    R.get_flow_stats(DPID)
    R.get_table_stats(DPID)
    #R.get_table_features(DPID)
    R.get_port_stats(DPID)
    #R.get_port_stats(DPID, 3) # DISABLED [BUG]
    #R.get_port_stats(DPID, 4) # DISABLED [BUG]
    #R.get_port_description(DPID)
    #R.get_queue_stats(DPID)
    #R.get_queue_stats(DPID, port=3)
    #R.get_queue_stats(DPID, queue=1)
    #R.get_queue_stats(DPID, port=2, queue=2)
    #R.get_queue_config(DPID)            # Restricted to OpenFlow <v1.0 - 1.3
    #R.get_queue_config(DPID, 3)         # Restricted to OpenFlow <v1.0 - 1.3
    #R.get_queue_description(DPID)       # Requires OpenFlow v1.4+
    #R.get_queue_description(DPID, 3)    # Requires OpenFlow v1.4+
    R.get_group_stats(DPID)
    R.get_group_stats(DPID, 3)


    R.get_flows(DPID)
