# ryu-rest-python
A Python module to interact with the REST API of the Ryu SDN controller.

# ABOUT
These are two Python modules that individually provide either a functional or object-orientated approach to using the Ryu REST API.

The modules make use of the Requests framework to interact with the RYU REST API.

# MODULES
Both the modules contain identical functions/methods. Which one you should use depends entirely on how comfortable you are with Python (although it is generally seen as better practice in the community to use OO approaches where possible)
### ryu_switch
Object-orientated approach.
Provides the `RyuSwitch` class to instantiate the physical switches connected to the controller as objects.
### ryurest
Functional approach
Allows you to call the RyuSwitch methods directly (although a switch Datapath ID (DPID) must be passed as an argument in most cases).

# REQUIREMENTS
**1. Install the [*Requests*][requests] library**

   `$ pip install requests`


**2. Run the Ryu controller with REST API enabled.**

     For example, enable REST with the Ryu program `simple_switch`:

     `$ sudo ryu-manager ryu.app.simple_switch_13 ryu.app.ofctl_rest`

# INSTALLATION
PIP support is WIP.

In the interim:

**1. Clone this repository:**

   `$ git clone https://github.com/nathancatania/ryu-rest-python`
   
**2. Copy either the `ryurest.py` or `ryu_switch.py` modules to your project directory.**

# DEMO
A demo for each module has been created to assist in usage.
These can be found in the `demos` folder of this repository.

# USAGE
## ryu_switch (Object-Orientated module)
**1. Import this module and the RyuSwitch class into your script**

   ```python
   from ryu_switch import RyuSwitch
   ```

**2. Create one or more RyuSwitch objects**

   ```python
   switch1 = RyuSwitch( DPID )
   ```
   If you do not know any of the DPIDs of the connected switches, you can initialize with no arguments and call the .get_switches() method to return an array of DPIDs. Be sure so assign any object created in this way a DPID manually:
   ```python
   # Create a switch
   switch0 = RyuSwitch()

   # Get an array of Datapath IDs (DPIDs) for all connected switches
   DPID_list = switch0.get_switches()

   # Assign a DPID manually to the switch created
   switch0.DPID = DPID_list[0]
   ```

**3. [OPTIONAL] Change the REST API URI**
   * The default location for the Ryu REST API is: `http://localhost:8080`
   * If Ryu is running on this PC (localhost), then there is no need to change anything.
   * If the Ryu controller is running on a different machine and/or port, you MUST set the API path within each `RyuSwitch` object created.
     * For example:
     ```python
     switch1 = RyuSwitch( DPID_list[0] )
     switch1.API = "http://192.168.1.30:8080"
     switch2 = RyuSwitch( DPID_list[1] )
     switch2.API = "http://192.168.1.30:8080"
     ```
     * **Warning!** If altering the API path, DO NOT add a trailing '/' at the end or the API call will fail!

**4. Execute the class methods as required**

   ```python
   # Gets all flows in flowtable
   flows = switch1.get_flows()
   ```
   * Some methods have optional filters as well.
   * Consult the `ryu_switch.py` module or the [Ryu REST API documentation][ryu_rest_docs] for more info.

## ryurest (functional module)
TBA



# RETURN FORMATS
* If API call was **successful**...
  * All the .get_x() methods will return **JSON formatted data**; EXCEPT .get_switches() which will return an array of DPIDs.
  * All the .set_x(), .delete_x(), .modify_X() methods will return boolean **True**.
* If the API call **fails**...
  * ALL methods/functions will return boolean **False**.

This means that you can use `if` statements to check for and handle errors accordingly.




[requests]: http://docs.python-requests.org/en/master/
[ryu_rest_docs]: http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html
