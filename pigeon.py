#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import urllib2
import urllib
import csv
import sys

AK = "OZPNC51CMPEyD65Qzk2L2x5y"

def get_distance(points, tactics = 12, ak = AK, mode='driving', coord_type = 'wgs84'):
    '''调用百度地图 API 计算路径
    
    Args:
        points: 路径经过点的经纬度列表；
        mode: 导航模式；
        coord_type: 坐标类型，默认wgs84;
        tactics: 导航策略，10表示不走高速，11表示最少时间，12表示最短路径，默认最短路径;
        ak: 百度地图访问密钥；
    '''
    api_url = "http://api.map.baidu.com/direction/v1/routematrix"
    for i in range(len(points)-1):
        origin_str = str(points[i]['n']) + ',' + str(points[i]['e'])
        dest_str = str(points[i+1]['n']) + ',' + str(points[i+1]['e'])
        values = {
                'output':       'json',
                'tactics':      str(tactics),
                'mode':         'driving',
                'coord_type':   coord_type,
                'ak':           ak,
                'origins':      origin_str,
                'destinations': dest_str
                }

        data = urllib.urlencode(values)
        url = api_url + '?' + data
        print url
        response = urllib2.urlopen(url)
        res = response.read()
        print res 
        
    return 10, 21

if __name__ == "__main__":
    reader = csv.reader(open("./data/test.csv"))
    writer = csv.writer(sys.stdout)

    cnt = -1 
    points = []
    start_date = 0
    start_time = 0
    current_car_id = ""
    for car_id, gps_date, gps_time, e, n, height, speed, direction, eff, car_state, flag in reader:
        if flag == cnt:
            pass
        else:
            if cnt != -1:           #排除未处理数据前
                best_time_distance, best_time_duration = get_distance(points, tactics = 11)             #计算最少时间导航策略的时间和距离（ak, mode, coord_type使用默认参数）
                best_distance_distance, best_distance_duration = get_distance(points, tactics = 12)     #计算最短路径导航策略的时间和距离（同上）
                no_highspeed_distance, no_highspeed_duration = get_distance(points, tactics = 10)       #计算不走高速导航策略的时间和距离（同上）
    
                # 结果写入CSV
                writer.writerow((current_car_id, start_date, start_time, cnt,  
                        best_time_distance, best_time_duration,         
                        best_distance_distance, best_distance_duration, 
                        no_highspeed_distance, no_highspeed_duration))
    
            # 开始计算新的路径
            current_car_id = car_id
            start_date = gps_date
            start_time = gps_time
            cnt = flag
            points = []

        point = {'n': n, 'e': e}
        points.append(point)
    
    best_time_distance, best_time_duration = get_distance(points, tactics = 11)             #计算最少时间导航策略的时间和距离（ak, mode, coord_type使用默认参数）
    best_distance_distance, best_distance_duration = get_distance(points, tactics = 12)     #计算最短路径导航策略的时间和距离（同上）
    no_highspeed_distance, no_highspeed_duration = get_distance(points, tactics = 10)       #计算不走高速导航策略的时间和距离（同上）
    
    # 结果写入CSV
    writer.writerow((current_car_id, start_date, start_time, cnt,  
            best_time_distance, best_time_duration,         
            best_distance_distance, best_distance_duration, 
            no_highspeed_distance, no_highspeed_duration))

