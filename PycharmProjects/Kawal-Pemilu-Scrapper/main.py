import json
import requests
from database import Database
import boto
def get_list_places(code):
    url = "http://www.kawalpemilu.org/api/children/" + str(code) + "?_=1538026960934"
    returned_json = requests.get(url)
    list_places = json.loads(returned_json.text)
    return list_places


def get_tps(code):
    url_tps = "http://www.kawalpemilu.org/api/tps/" + str(code) + "?_=1538026960934"
    returned_json = requests.get(url_tps)
    result = json.loads(returned_json.text)
    print(result)
    return result


def save_result(result, database, code):
    for tps in range(len(result)):
        try:
            if result[tps][4] > 0:
                sql = "INSERT INTO hasil (prabowo, jokowi, suara_sah, suara_tidak_sah) VALUES (%s, %s, %s, %s)"
                val = (result[tps][2], result[tps][3], result[tps][4], result[tps][5])
                database.get_cursor().execute(sql, val)
                database.commit()
                filename = str(code).zfill(7) + str(tps + 1).zfill(3) + '04.jpg'
                result_pic_url = "http://scanc1.kpu.go.id/viewp.php?f=" + filename
                print(result_pic_url)
                save_image(result_pic_url, filename)
        except Exception:
            print('cannot save result')


def save_image(url_image, filename):
    requested_pic = requests.get(url_image)
    if requested_pic.status_code == 200:
        try:
            connection = boto.connect_s3('AKIAIQ2PJXOKYG3NNPYQ', 'UtfaTqkf6Ub4bNlaZN5HCCBrX9bxDbbImZhg9eLn')
            bucket = connection.get_bucket('kawal-pemilu-frieda', validate=False)
            key = bucket.new_key("{filename}".format(filename=filename))
            key.set_contents_from_string(requested_pic.content, replace=True,
                                       policy='authenticated-read',
                                       reduced_redundancy=True)
            # return key.generate_url(expires_in=0, force_http=True)
        except Exception:
            print('cannpt save image result')


def main_func():
    database = Database()
    database.create_table()
    counter = 0
    while counter < 5:
        try:
            list_provinces = get_list_places(0)
            for province in range(len(list_provinces)):
                list_kabupaten = get_list_places(list_provinces[province][0])
                for kabupaten in range(len(list_kabupaten)):
                    list_kecamatan = get_list_places(list_kabupaten[kabupaten][0])
                    for kecamatan in range(len(list_kecamatan)):
                        list_kelurahan = get_list_places(list_kecamatan[kecamatan][0])
                        for kelurahan in range(len(list_kelurahan)):
                           list_tps = get_tps(list_kelurahan[kelurahan][0])
                           save_result(list_tps, database, list_kelurahan[kelurahan][0])
        except Exception:
            print('something is wrong')
            counter +=1
        finally:
            print('done.')


def lambda_handler(event, context):
    # TODO implement
    return main_func()
main_func()