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


    def debug_dump(self, rest_uri, r, title=""):
        if title:
            print title
        print "REST call to URI:"
        print rest_uri
        print "Output:"
        print str(r.json()) + '\n'



    ###### Retrieve Switch Information ######

    ## Get DPIDs of all switches ##
    def get_switches(self):

        '''
        Description:
        Get the list of all switches which connected to the controller.

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
    def get_stats_switch(self, DPID):

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
        content = R.get_stats_switch('123917682136708')
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
            if self.debug: self.debug_dump(rest_uri, r)

            return r.json()
        else:
            # Filter is present, dump only matched flows.
            # Make call to REST API (POST)
            r = requests.post(rest_uri, data=filters)

            # DEBUG MODE
            if self.debug: self.debug_dump(rest_uri, r, "GET FLOWS")

            return r.json()



    ## Get the aggregated stats of the specified switch's flow table. Optionally give a filter. ##
    def get_stats_flow(self, DPID, filters={}):

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
        content = R.get_stats_flow('123917682136708')
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
    def get_stats_table(self, DPID):

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
        content = R.get_stats_table('123917682136708')
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
    def get_stats_port(self, DPID, port=0):

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
        content1 = R.get_stats_port('123917682136708', 3)    # Will get stats for ONLY Port #3.
        content1 = R.get_stats_port('123917682136708')       # Will get stats for ALL ports

        ****** KNOWN ISSUES ******
        Specifying a specific port crashes the switch - this is a FW issue. Awaiting patch.
        Workaround: Parse port info using lookup/JSON module on method return.
        '''

        # Path: /stats/aggregateflow/<DPID>[/portnumber]
        rest_uri = self.API + "/stats/port/" + DPID

        # Make call to REST API (GET)
        r = requests.get(rest_uri)

        # DEBUG MODE
        if self.debug: self.debug_dump(rest_uri, r, "GET PORT STATS: NO PORT SPECIFIED")

        return r.json()

        # if port == 0:
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









if __name__ == "__main__":
    DPID = "123917682136708"
    R = ryuRest()

    content = R.get_switches()
    print str(content[0]) + '\n'

    R.get_stats_switch(DPID)

    R.get_flows(DPID)

    R.get_stats_flow(DPID)
    R.get_stats_table(DPID)
    R.get_table_features(DPID)
    R.get_stats_port(DPID)
    R.get_stats_port(DPID, 3)
    R.get_stats_port(DPID, 4)
