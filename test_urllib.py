#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import urllib2
import sys

if __name__ == "__main__":
    url = u"http://api.map.baidu.com/direction/v1/routematrix?tactics=11&output=json&" \
    + "origins=23.11216,113.25762&destinations=23.09931,113.30277" \
    + "&coord_type=wgs84&ak=OZPNC51CMPEyD65Qzk2L2x5y"
    url_utf8 = url.encode("utf-8")
    print url_utf8

    response = urllib2.urlopen(url_utf8)
    html = response.read()
    html = html.decode("utf-8")
    print html
