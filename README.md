# Net-Eye

Tired of seeing the bland traffic capture of the Wireshark ? Want to see where is the source and destination of the traffic in a world map for simplicity?

This script will read network traffic from the pcap file and plot the source and destination IP in a KML file. 
KML is a file format used to display geographic data in an Earth browser such as Google Earth. 
You can create KML files to pinpoint locations, add image overlays, and expose rich data in new ways.
KML file will generated as "output.KML" in the same directory where this exe is located.
After succesfull generation open google.mymaps and import the KML file there. 


Note : There are some hard requirements for this script to run. Some third party modules are necessary. 
These are:
dpkt
pygeoip

Source and destinations are resolved by referencing to GeoLiteCity.dat 
