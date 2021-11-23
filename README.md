# minimal-neem-parser

## Prerequisites

ROS melodic, with the [rosbridge_server](http://wiki.ros.org/rosbridge_server) package installed.

1. KnowRob (https://github.com/benjaminalt/knowrob) @ c34012570f5c15e8e7950f5082bd18c8148995ef
   * Also follow the KnowRob installation instructions (for MongoDB, Prolog etc.)
2. neem-interface (https://github.com/benjaminalt/neem-interface) @ 80360fcd5c825a1b27d18ddb3a0ce5acf69d50e7

Clone this repo into your ROS workspace and run `pip3 install -r requirements.txt`.

## Using the parser

1. Source your ROS workspace and run `roslaunch minimal_neem_parser knowrob.launch`. Wait until `rosprolog service is running.` is displayed.
2. Use the NEEMParser class in neem_utils/neem_parser.py. It contains an example for parsing a NEEM. Additional test NEEMs are provided in the `testing/neems` directory.