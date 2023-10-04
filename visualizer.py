import socket 
import dpkt
import pygeoip
import tkinter
import requests
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import re


gi = pygeoip.GeoIP('GeoLiteCity.dat')
publicIP = requests.get('https://api.ipify.org').content.decode('utf8')


def retKML(dstip, srcip):
    
    dst = gi.record_by_name(dstip)
    src = gi.record_by_name(publicIP) # TO-DO: Add the functionality to automatically fetch the public IP
    try:
        dstlongitude = dst['longitude']
        dstlatitude = dst['latitude']
        
        srclongitude = src['longitude']
        srclatitude = src['latitude']

        kml = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<extrude>1</extrude>\n'
            '<tessellate>1</tessellate>\n'
            '<styleUrl>#transBluePoly</styleUrl>\n'
            '<LineString>\n'
            '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
            '</LineString>\n'
            '</Placemark>\n'
        )%(dstip, dstlongitude, dstlatitude, srclongitude, srclatitude)
        return kml
    except:
        return ''






def plotIPs(pcap):
    kmlPts = ''
    for(ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            KML = retKML(dst,src)
            kmlPts = kmlPts+KML
        except:
            pass
    return kmlPts







def main():
    
    try:
      
        filename = askopenfilename(initialdir="C:/Users",title="Choose pcap file", filetypes=(("Wireshark pcap","*.pcap"),("All files","*.*")))      
        pcapFile = open(filename,'rb')  # TO-DO: Add the functionality to choose pcap files from the system
        pcap = dpkt.pcap.Reader(pcapFile)
        kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'\
            '<Style id="transBluePoly">'\
            '<LineStyle>'\
            '<width>1.5</width>'\
            '<color>501400E6</color>'\
            '</LineStyle>'\
            '</Style>'

        kmlfooter = '</Document>\n</kml>\n'
        kmldoc = kmlheader + plotIPs(pcap) + kmlfooter

        with open('output.KML','w') as outputFile:
                outputFile.write(kmldoc)
                outputFile.close()

        messagebox.showinfo(title="KML generated successfuly.",message=kmldoc)
        
            
    except re.error:
            messagebox.showerror(title="Status",message="File format is not supported.")
    
    

    
            
    
    
        

    

def findIP():
     ip = requests.get('https://api.ipify.org').content.decode('utf8')
     messagebox.showinfo(title="Public IP",message="Your public IP address is: "+ip+".Address resolution is done by https://api.ipify.org ")


def readme():
     msg = ''
     with open('README.txt','r') as readme:
          msg = readme.read()
        
     messagebox.showinfo(title="Manual",message=msg)



if __name__ == '__main__':
    window = tkinter.Tk()
    window.geometry("600x400")
    window.title("KML Generator")
    
   
    labelWindow = tkinter.Label(window,text="Welcome. Ensure internet connectivity in order to resolve the public IP. ",font=('Arial 10 bold')).pack(pady=20)

    readmeButton = tkinter.Button(window,text="What the hell is this?",command=readme,font=('Arial 10 bold'),bg='green').pack(padx=30,pady=30)

    ipButton = tkinter.Button(window,text="Find my public IP.",command=findIP,font=('Arial 10 bold'),bg='blue').pack(pady=30,padx=30)

    openFileButton = tkinter.Button(window,text="Select packet capture file.",command=main,bg="red",font=('Arial 10 bold')).pack(pady=30,padx=30)
    
    


    

    

    window.mainloop()
