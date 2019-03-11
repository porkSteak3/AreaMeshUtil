# AreaMeshUtil

総務省資料 : 地域メッシュ統計の特質・沿革 
「統計に用いる標準地域メッシュおよび標準地域メッシュ・コード」（昭和48年７月12日行政管理庁告示第143号）
http://www.stat.go.jp/data/mesh/pdf/gaiyo1.pdf

に基づき、下記の通り変換します。

* 緯度経度⇒地域メッシュ・コード
* 地域メッシュ・コード⇒geojson Polygon

```
    ll2m = LatLngToMesh()
    lat, lng = 35.700001, 139.800001
    meshcode = ll2m.convert2Mesh(3, lat, lng)
    print(meshcode)
    # 53394644
    print(ll2m.convert2LatLng(meshcode))
    # {"geometory": {"coordinates": [[[35.7, 139.8], [35.7, 139.8125], [35.708333333333336, 139.8125], [35.708333333333336, 139.8], [35.7, 139.8]]], "type": "Polygon"}, "geometry": null, "id": "53394644", "properties": {}, "type": "Feature"}
```
