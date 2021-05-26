
import datetime
import math
from decimal import Decimal

EARTH_RADIUS = 6371.0008

class User:
    def __init__(self, name, birth_day, birth_month, birth_year):
        self.name = name
        self.my_routes = []
        self.friends = []
        self.friends_routes = []
        self.birth_day = datetime.date(int(birth_year), int(birth_month), int(birth_day))
        self.age = datetime.date.today() - self.birth_day



    def get_routes(self):
        file = str(self.name)+".txt"
        with open(file, encoding="utf8") as f:
            next(f)
            for line in f:
                table = line.split("\t")
                if len(table) == 7:
                    r = Route(table[0], table[1], table[2], table[3], table[4], table[5])
                    if table[0] == self.name:
                        self.my_routes.append(r)
                    else:
                        self.friends_routes.append(r)




    def add_route(self, route_name, gpx_file):
        with open(gpx_file, encoding="utf8") as f:
            lat = []
            lon = []
            times = []
            for line in f:
                line_tab = line.split(' ')
                for i in line_tab:
                    if i[0:3] == "lat":
                        i += "."
                        i = i.split('"')
                        lat.append(i[1])
                    if i[0:3] == "lon":
                        i = i.split('"')
                        lon.append(i[1])
                    if i[0:5] == "<time":
                        i = i.split('>')
                        res = i[1].split('<')
                        times.append(res[0])


        new = Route(self.name, route_name, self.time_helper(times[0])[0], Decimal(self.get_distance(lat, lon)), Decimal(self.abs_dist(lat, lon)), Decimal(self.get_time(times)))
        return new


    def get_distance(self, lat, lon):
        dys = 0.0
        for i in range(len(lat)):
            if lat[i] != lat[i-1] and lon[i] != lon[i-1]:
                elem = math.acos(
                    math.sin(math.radians(float(lat[i]))) * math.sin(math.radians(float(lat[i - 1]))) + math.cos(
                        math.radians(float(lat[i]))) * math.cos(math.radians(float(lat[i - 1]))) * math.cos(
                        math.radians(float(lon[i]) -
                                     float(lon[i - 1])))) * float(EARTH_RADIUS)
                dys = dys + elem
        return dys

    def abs_dist(self, lat, lon):
        lat_help = []
        lon_help = []
        lat_help.append(lat[0])
        lat_help.append(lat[len(lat) - 1])
        lon_help.append(lon[0])
        lon_help.append(lon[len(lon) - 1])
        return self.get_distance(lat_help, lon_help)

    def time_helper(self, time):
        full_time = time.split('T')
        t = full_time[1].split(':')
        d = full_time[0].split('-')
        hours = datetime.time(int(t[0]), int(t[1]), int(t[2][0:2]))
        day = datetime.date(int(d[0]), int(d[1]), int(d[2]))
        return [day, hours]

    def get_time(self, time):
        res = datetime.timedelta(float((self.time_helper(time[len(time) - 1])[0] - self.time_helper(time[0])[0]).days),
                                 float(self.time_helper(time[len(time) - 1])[1].second - self.time_helper(time[0])[1].second), 0.0, 0.0,
                                 float(self.time_helper(time[len(time) - 1])[1].minute - self.time_helper(time[0])[1].minute),
                                 float(self.time_helper(time[len(time) - 1])[1].hour - self.time_helper(time[0])[1].hour))
        return res.total_seconds()



    def save_stats(self):
        file = str(self.name)+".txt"
        with open(file, 'w') as file_txt:
            file_txt.write(str(self.name)+"\t"+str(self.birth_day.day)+"\t"+str(self.birth_day.month)+"\t"+str(self.birth_day.year)+"\n")
            if len(self.friends) > 0:
                for fr in self.friends:
                    file_txt.write(str(fr) + "\t")
            for r in self.my_routes:
                file_txt.write(
                    str(r.owner) + "\t" + str(r.name) + "\t" + str(r.dat) + "\t" + str(
                        r.distance) + "\t" + str(r.abs_dist) + "\t" + str(r.total_time) + "\t\n")
            for r in self.friends_routes:
                file_txt.write(
                    str(r.owner) + "\t" + str(r.name) + "\t" + str(r.dat) + "\t" + str(
                        r.distance) + "\t" + str(r.abs_dist) + "\t" + str(r.total_time) + "\t\n")




    def show_exclusive_stats(self):
        if len(self.my_routes) > 0:
            max_dist = self.my_routes[0].distance
            min_dist = self.my_routes[0].distance
            max_abs_dist = self.my_routes[0].abs_dist
            max_time = self.my_routes[0].total_time
            min_time = self.my_routes[0].total_time
            for r in self.my_routes:
                if r.distance > max_dist:
                    max_dist = r.distance
                if r.distance < min_dist:
                    min_dist = r.distance
                if r.abs_dist > max_abs_dist:
                    max_abs_dist = r.abs_dist
                if r.total_time > max_time:
                    max_time = r.total_time
                if r.total_time < min_time:
                    min_time = r.total_time
            for r in self.my_routes:
                if r.distance == max_dist:
                    max_d = "Max distance: " + str(r.distance)[0:6]
                if r.distance == min_dist:
                    min_d = "Min distance: " + str(r.distance)[0:6]
                if r.abs_dist == max_abs_dist:
                    max_ad = "Max absolute distance: " + str(r.abs_dist)[0:5]
                if r.total_time == max_time:
                    max_t = "Max time(in seconds): " + str(r.total_time)
                if r.total_time == min_time:
                    min_t = "Min time(in seconds): " + str(r.total_time)
            return [max_d, min_d, max_ad, max_t, min_t]
        else:
            return []



    def __str__(self):
        return "User: "+str(self.name)+"  Age(in days): "+str(self.age)






class Route:
    def __init__(self, owner, name, dat, dist, abs_dist, tim):
        self.owner = owner
        self.name = name
        self.dat = dat
        self.distance = dist
        self.abs_dist = abs_dist
        self.total_time = tim



    def __str__(self):
         return "Owner: "+str(self.owner)+ "  Name: "+str(self.name)+ "  Date: "+str(self.dat)+"  Distance: "+str(self.distance)[0:6]+"  Absolete distance: "+str(self.abs_dist)[0:5]+"  Time: "+str(self.total_time)



