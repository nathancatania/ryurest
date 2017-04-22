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



    ### Retrieve Switch Stats

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

        # Path: stats/switches
        api_path = self.API + "/stats/switches"

        # Make call to REST API (GET)
        r = requests.get(api_path)

        # DEBUG MODE
        if self.debug:
            print "REST call to URI:"
            print api_path
            print "Output:"
            print str(r.json()) + '\n'

        return r.json()


    ## Get hardware stats of a specified switch DPID ##
    def get_stats(self, DPID):

        '''
        Description:
        Get the desc stats of the switch which specified with Datapath ID in URI.

        Link:
        http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-the-desc-stats

        Arguments:
        Datapath ID (DPID) of the target switch.

        Return value:
        JSON structure containing the following switch information (ordered by DPID):

        Usage:
        R = ryuRest()
        content = R.get_stats('123917682136708')
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

        # Path: stats/switches
        api_path = self.API + "/stats/desc/" + DPID

        # Make call to REST API (GET)
        r = requests.get(api_path)

        # DEBUG MODE
        if self.debug:
            print "REST call to URI:"
            print api_path
            print "Output:"
            print str(r.json()) + '\n'

        return r.json()



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

        # Path: stats/switches
        api_path = self.API + "/stats/flow/" + DPID

        if not filters:
            # No filter specified, dump ALL flows.
            # Make call to REST API (GET)
            r = requests.get(api_path)

            # DEBUG MODE
            if self.debug:
                print "NO FILTERS SPECIFIED"
                print "REST call to URI:"
                print api_path
                print "Output:"
                print str(r.json()) + '\n'

            return r.json()
        else:
            # Filter is present, dump only matched flows.
            # Make call to REST API (POST)
            r = requests.post(api_path, data=filters)

            # DEBUG MODE
            if self.debug:
                print "Filters specified!"
                print "REST call to URI:"
                print api_path
                print "Output:"
                print str(r.json()) + '\n'

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

        # Path: stats/switches
        api_path = self.API + "/stats/aggregateflow/" + DPID

        if not filters:
            # No filter specified, dump ALL flows.
            # Make call to REST API (GET)
            r = requests.get(api_path)

            # DEBUG MODE
            if self.debug:
                print "NO FILTERS SPECIFIED"
                print "REST call to URI:"
                print api_path
                print "Output:"
                print str(r.json()) + '\n'

            return r.json()
        else:
            # Filter is present, dump only matched flows.
            # Make call to REST API (POST)
            r = requests.post(api_path, data=filters)

            # DEBUG MODE
            if self.debug:
                print "Filters specified!"
                print "REST call to URI:"
                print api_path
                print "Output:"
                print str(r.json()) + '\n'

            return r.json()






if __name__ == "__main__":
    R = ryuRest()

    content = R.get_switches()
    print str(content[0]) + '\n'

    R.get_stats('123917682136708')

    R.get_flows('123917682136708')

    R.get_flow_stats('123917682136708')
