import geojson
from geojson import Polygon, Feature, FeatureCollection

class LatLngToMesh():
    def __init__(self):
        pass

    def convert2Mesh(self, code_type, lat, lng):
        # Latitude
        p, a = divmod(lat * 60, 40)
        q, b = divmod(a, 5)
        r, c = divmod(b * 60, 30)
        s, d = divmod(c, 15)
        t, e = divmod(d, 7.5)
        t2, e2 = divmod(e, 3.75)

        # Longitude
        u, f = divmod(lng, 1)
        u = u - 100
        v, g = divmod(f * 60, 7.5)
        w, h = divmod(g * 60, 45)
        x, i = divmod(h, 22.5)
        y, j = divmod(i, 11.25)
        y2, j2 = divmod(j, 5.625)

        # 1st
        p = int(p)
        u = int(u)

        # 2nd
        q = int(q)
        v = int(v)

        # 3rd
        r = int(r)
        w = int(w)

        # 4th
        s = int(s)
        x = int(x)

        # 5th
        t = int(t)
        y = int(y)

        # 6th
        t2 = int(y2)
        y2 = int(y2)

        m = (s * 2) + (x + 1)
        n = (t * 2) + (y + 1)
        n2 = (t2 * 2) + (y2 + 1)

        return self.__comb_code(code_type, p, u, q, v, r, w, m, n, n2)

    def __comb_code(self, code_type, p, u, q, v, r, w, m, n, n2):
        if code_type == 1:
            return "{}{}".format(p, u)
        if code_type == 2:
            return "{}{}{}{}".format(p, u, q, v)
        if code_type == 3:
            return "{}{}{}{}{}{}".format(p, u, q, v, r, w)
        if code_type == 4:
            return "{}{}{}{}{}{}{}".format(p, u, q, v, r, w, m)
        if code_type == 5:
            return "{}{}{}{}{}{}{}{}".format(p, u, q, v, r, w, m, n)
        if code_type == 6:
            return "{}{}{}{}{}{}{}{}{}".format(p, u, q, v, r, w, m, n, n2)

    def convert2LatLng(self, meshcode):
        code_type = len(meshcode)

        # (lat3, lng3) - (lat4, lng4)
        #      |              |
        # (lat1, lng1) - (lat2, lng2)

        lat1 = 0.0
        lng1 = 0.0
        diff_lat = 0.0
        diff_lng = 0.0

        # 1st
        if code_type > 3:
            p = int(meshcode[0:2])
            u = int(meshcode[2:4])
            lat1 += p * 40 / 60
            lng1 += u + 100
            diff_lat = 40 / 60
            diff_lng = 1

        # 2nd
        if code_type > 5:
            q = int(meshcode[4])
            v = int(meshcode[5])
            lat1 += (q * 5) / 60
            lng1 += (v * 7.5) / 60
            diff_lat = 5 / 60
            diff_lng = 7 / 60 + 30 / 3600

        # 3rd
        if code_type > 7:
            r = int(meshcode[6])
            w = int(meshcode[7])
            lat1 += (r * 30) / 3600
            lng1 += (w * 45) / 3600
            diff_lat = 30 / 3600
            diff_lng = 45 / 3600

        # 4th
        if code_type > 8:
            m = int(meshcode[8])
            lat1 += (m - 1) // 2 * 15 / 3600
            if ((m - 1) % 2) > 0:
                lng1 += 22.5 / 3600
            diff_lat = 15 / 3600
            diff_lng = 22.5 / 3600

        # 5th
        if code_type > 9:
            n = int(meshcode[9])
            lat1 += (n - 1) // 2 * 7.5 / 3600
            if ((n - 1) % 2) > 0:
                lng1 += 11.25 / 3600
            diff_lat = 7.5 / 3600
            diff_lng = 11.25 / 3600

        # 6th
        if code_type > 10:
            n2 = int(meshcode[10])
            lat1 += (n2 - 1) // 2 * 3.75 / 3600
            if ((n2 - 1) % 2) > 0:
                lng1 += 5.625 / 3600
            diff_lat = 3.75 / 3600
            diff_lng = 5.625 / 3600

        lat2, lng2 = lat1, lng1 + diff_lng
        lat3, lng3 = lat1 + diff_lat, lng1 + diff_lng
        lat4, lng4 = lat1 + diff_lat, lng1

        coodinates = list()
        coodinates.append([lng1, lat1])
        coodinates.append([lng2, lat2])
        coodinates.append([lng3, lat3])
        coodinates.append([lng4, lat4])
        coodinates.append([lng1, lat1])
        p = Polygon([coodinates])

        return Feature(meshcode, geometry=p)


if __name__ == "__main__":
    ll2m = LatLngToMesh()
    lat, lng = 35.700001, 139.800001
    meshcode = ll2m.convert2Mesh(3, lat, lng)
    print(meshcode)
    print(ll2m.convert2LatLng(meshcode))

    mesh_list = list()
    mesh_list.append(ll2m.convert2LatLng(meshcode))
    fc = FeatureCollection(mesh_list)
    with open('./mesh.json', 'w', encoding='utf-8') as fp:
        fp.write(geojson.dumps(fc, indent=2))
