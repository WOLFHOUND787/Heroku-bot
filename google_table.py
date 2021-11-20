import vk_api, json
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
import gspread
#import opd.py
gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('141YkihhlI7rb1RPKI_BG4QU3oy3pp2Pj22gTRXj2i90')
worksheet = sh.sheet1
#res = worksheet.get_all_records()
#res = worksheet.get_all_values()
#res = worksheet.col_values(1)

def ident(ide):
    iden = [ide]
    worksheet.append_row(iden)


#print(res)
