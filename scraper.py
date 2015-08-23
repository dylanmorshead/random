# Copyright Revealed Torrent Scraper
import urllib2
import urllib
import bencode
import hashlib # to generate SHA1 hash based on torrent
import locale
from random import randrange #to generate random transaction_id
import re
import socket
import struct
from urlparse import urlparse, urlunsplit
import binascii
import zlib


def number_format(num, places=0):
    return locale.format("%.*f", (places, num), True)

if __name__ == '__main__':
    locale.setlocale(locale.LC_NUMERIC, '')
    number_format(12345.6789, 2)

# to convert GB > MB > KB ect
def formatSizeUnits(filesize):
    if filesize >= 1073741824:
        filesize = str(number_format(filesize / 1073741824, 2)) + ' GB'
    elif filesize >= 1048576:
        filesize = str(number_format(filesize / 1048576, 2)) + ' MB'
    elif filesize >= 1024:
        filesize = str(number_format(filesize / 1024, 2)) + ' KB'
    elif filesize > 1:
        filesize = str(filesize) + ' bytes'
    elif filesize == 1:
        filesize = str(filesize) + ' byte'
    else:
        filesize = '0 bytes'
    return filesize

# Scrape Tracker, get the seeders and leechers UDP Only

def ScrapeTrackerUDP(tracker, port, infohash): #only for UDP
    try:
        clisocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clisocket.settimeout(5)
        clisocket.connect((tracker, port))
        #Protocol says to keep it that way
        connection_id=0x41727101980
        #We should get the same in response
        transaction_id = randrange(1,65535)
        packet=struct.pack(">QLL",connection_id, 0,transaction_id)
        clisocket.send(packet)
        res = clisocket.recv(16)
        action,transaction_id,connection_id=struct.unpack(">LLQ",res)
        packet_hashes = infohash.decode('hex')
        packet = struct.pack(">QLL", connection_id, 2, transaction_id) + packet_hashes
        clisocket.send(packet)
        res = clisocket.recv(8 + 12*len(infohash))
        index = 8
        seeders, completed, leechers = struct.unpack(">LLL", res[index:index+12])

        torrent_details = (seeders, leechers)

        return torrent_details
      
    except Exception, e:
        if e.errno == 10054:
            print "Cannot connect to tracker: " + tracker
            return "Error: " + str(10054)
        else:
            print e
            return "Error: " + str(e)

# Scrape Tracker, get the seeders and leachers TCP Only

def ScrapeTrackerTCP(tracker, torrent_hash):
    try:
        hashed = binascii.a2b_hex(torrent_hash)
        hashed = urllib.quote_plus(hashed)
        url = tracker + "?info_hash=" + hashed
        txt = urllib2.urlopen(url, timeout=1).read()
        data = bencode.bdecode(txt)
        torrent_details = (data["complete"], data["incomplete"])
        return torrent_details
  
    except Exception as e:
        print e


class TorrentScraper:

    """ Usage TorrentScraper("url", True) """
    def __init__(self, infohash, light=True):
        try:
            torrent = bencode.bdecode(zlib.decompress(urllib2.urlopen('http://torcache.net/torrent/' + infohash + '.torrent', timeout=10).read(),16+zlib.MAX_WBITS ))
            #urllib2.urlopen

            # we need to generate a SHA1 hash then convert it to a uppercase string
            torrent_hash = str(hashlib.sha1(bencode.bencode(torrent['info'])).hexdigest()).upper()
            print "Infohash: " + torrent_hash
          
            # Get the filename
            print torrent['info']['name']
            # Get the trackers
            print "Trackers: "
            udp_port = '(?:udp.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
            http_port = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
          
            for trackers in torrent['announce-list']:
                # print the tracker
                tracker = str(trackers).strip("['").strip("']")
                print tracker
                http_url = re.search(http_port, str(tracker))
                udp_url = re.search(udp_port, str(tracker))
                if "udp://" in tracker:
                    print(ScrapeTrackerUDP(udp_url.group('host'), int(udp_url.group('port')), torrent_hash))
                if "http://" in tracker:
                       print(ScrapeTrackerTCP(tracker, torrent_hash))
                      
            torrent = bencode.bdecode(zlib.decompress(urllib2.urlopen('http://torcache.net/torrent/' + infohash + '.torrent', timeout=10).read(),16+zlib.MAX_WBITS ))
            #urllib2.urlopen


            if torrent['info']['files'] != None:
                   print "Multible Files"
                   for files in torrent['info']['files']:
                       path = str(files['path']).strip("['").strip("']")
                       length = int(files['length'])
                       #print files['path'] + ''.join(files['length'])
                       print path + " " + formatSizeUnits(length)
                      
            else:
                print "Single File"

          
            print "magnet:?xt=urn:btih:" + torrent_hash + "&dn=" + torrent['info']['name']
              
        except Exception as e:
            print e
