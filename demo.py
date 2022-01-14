
import re
from pdf2image import convert_from_path
import pytesseract
from pytesseract import Output
import os
TESSDATA_PREFIX = os.environ.get('TESSDATA_PREFIX', None)
POPPLER_PATH = os.environ.get('POPPLER_PATH', None)
from PIL import Image, ImageEnhance, ImageFilter
print('TESSDATA_PREFIX',TESSDATA_PREFIX)
print('POPPLER_PATH',POPPLER_PATH)
if TESSDATA_PREFIX:
   pytesseract.pytesseract.tesseract_cmd = TESSDATA_PREFIX
else:
   pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
if POPPLER_PATH:
   poppler_path = POPPLER_PATH
else:
   poppler_path = r'./poppler-0.68.0/bin'
def fetch_ocr(file_obj):
    images = convert_from_path(file_obj, 500, poppler_path=poppler_path)
    data = dict()
    for i, image in enumerate(images):
        img_index = 'page_'+str(i)
        data[img_index] = dict()
        # fname = 'C:/Users/Triveni/Desktop/sai_project/image'+str(i)+'.png'
        # image.save(fname, "PNG")

        im = image.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(im)
        im = enhancer.enhance(2)
        im = im.convert('1')
        # im.save('C:/Users/Triveni/Desktop/sai_project/temp2.jpg')

        text = pytesseract.image_to_string(im, config='--oem 3 --psm 6')
        dct = pytesseract.image_to_data(im, output_type=Output.DICT)
        keys = list(dct.keys())
        n_boxes = len(dct['text'])
        for i in range(n_boxes):
            if 'VERIFICATION OF COVERAGE' in text:
                data[img_index]['type'] = 'VERIFICATION OF COVERAGE'
                if 'policy' in dct['text'][i].lower() and 'number' in dct['text'][i+1].lower() and (dct['text'][i+2]).isnumeric():
                    data[img_index]['policy_number'] = dct['text'][i+2]
                # date format
                if 'effective' in dct['text'][i].lower() and 'date' in dct['text'][i+1].lower():
                    data[img_index]['effective_date'] = dct['text'][i+2]
                if 'expiration' in dct['text'][i].lower() and 'date' in dct['text'][i+1].lower() and 'expiration_date' not in data[img_index]:
                    data[img_index]['expiration_date'] = dct['text'][i+2]
                if 'registered' in dct['text'][i].lower() and 'state' in dct['text'][i+1].lower() and 'registred_state' not in data[img_index]:
                    data[img_index]['registred_state'] = dct['text'][i+2]
                if 'vehicle' in dct['text'][i].lower() and 'year' in dct['text'][i+1].lower() and 'vehicle_year' not in data[img_index]:
                    data[img_index]['vehicle_year'] = dct['text'][i+2]
                if 'make' in dct['text'][i].lower() and 'make' not in data[img_index]:
                    data[img_index]['make'] = dct['text'][i+1]
                if 'model' in dct['text'][i].lower() and 'model' not in data[img_index]:
                    data[img_index]['model'] = dct['text'][i+1] + \
                        ' '+dct['text'][i+2]
                if 'vin' in dct['text'][i].lower() and 'vin' not in data[img_index]:
                    data[img_index]['vin'] = dct['text'][i+1] + dct['text'][i+2]
                if 'collision' in dct['text'][i].lower() and 'collision' not in data[img_index]:
                    data[img_index]['collision'] = dct['text'][i+1]
                if 'comprehensive' in dct['text'][i].lower() and 'comprehensive' not in data[img_index]:
                    data[img_index]['comprehensive'] = dct['text'][i+3]
                if 'property' in dct['text'][i].lower() and 'damage' in dct['text'][i+1].lower() and 'liability' in dct['text'][i+2].lower():
                    data[img_index]['property_damage_liability'] = dct['text'][i+3]
                if 'personal' in dct['text'][i].lower() and 'injury' in dct['text'][i+1].lower() and 'protection' in dct['text'][i+2].lower():
                    data[img_index]['personal_injury_protection'] = dct['text'][i+3]
                if 'property' in dct['text'][i].lower() and 'damage' in dct['text'][i+1].lower() and 'liability' not in dct['text'][i+2].lower():
                    data[img_index]['property_damage'] = dct['text'][i+6]
                if 'mechanical' in dct['text'][i].lower() and 'breakdown' in dct['text'][i+1].lower():
                    data[img_index]['mechanical_breakdown'] = dct['text'][i+2]
                # print(dct['text'][i], 'left', dct['left'][i], 'top', dct['top']
                    #   [i], 'width', dct['width'][i], 'height', dct['height'][i])
                if 'mailing' in dct['text'][i].lower() and 'address' in dct['text'][i+1].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-4 <= dct['left'][j] <= dct['left'][i]+2250 and dct['top'][i]+4 <= dct['top'][j] <= dct['top'][i]+370:
                            if 'mailing_address' in data[img_index].keys():
                                if dct['text'][j]:
                                    data[img_index]['mailing_address'] += ' ' + \
                                        " ".join(dct['text'][j].split())
                            else:
                                data[img_index]['mailing_address'] = " ".join(
                                    dct['text'][j].split())
                if 'mailing_address' in data[img_index].keys():
                    data[img_index]['mailing_address'] = data[img_index]['mailing_address'].strip(
                    )

            elif 'insurance Identification Card' in text:
                data[img_index]['type'] = 'Insurance Identification Card'
                if 'policy' in dct['text'][i].lower() and 'number' in dct['text'][i+1].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-4 <= dct['left'][j] <= dct['left'][i]+100 and dct['top'][i]+60 <= dct['top'][j] <= dct['top'][i]+65:
                            data[img_index]['policy_number'] = dct['text'][j]
                if 'effective' in dct['text'][i].lower() and 'date' in dct['text'][i+1].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-4 <= dct['left'][j] <= dct['left'][i]+100 and dct['top'][i] <= dct['top'][j] <= dct['top'][i]+65:
                            data[img_index]['effective_date'] = dct['text'][j][0:8]
                if 'expiration' in dct['text'][i].lower() and 'date' in dct['text'][i+1].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-4 <= dct['left'][j] <= dct['left'][i]+100 and dct['top'][i] <= dct['top'][j] <= dct['top'][i]+65:
                            data[img_index]['expiration_date'] = dct['text'][j][0:8]
                # print(dct['text'][i])
                if 'year' in dct['text'][i].lower():
                    for j in range(n_boxes):
                        if data[img_index].keys() and dct['left'][i]-4 <= dct['left'][j] <= dct['left'][i]+100 and dct['top'][i] <= dct['top'][j] <= dct['top'][i]+65:
                            try:
                                data[img_index]['year'] = int(dct['text'][j])
                            except:
                                pass
                if 'make' in dct['text'][i].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-20 <= dct['left'][j] <= dct['left'][i]+100 and dct['top'][i] <= dct['top'][j] <= dct['top'][i]+67 and 'make' not in dct['text'][j].lower():
                            data[img_index]['make'] = dct['text'][j]

                # ipdb.set_trace()
            elif 'Coverages' in text:
                data[img_index]['type'] = 'Coverages'
                if 'dear' in dct['text'][i].lower():
                    data[img_index]['name'] = dct['text'][i+1] +' '+ dct['text'][i+2]
                if 'mailing' in dct['text'][i].lower() and 'address' in dct['text'][i+1].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-4 <= dct['left'][j] <= dct['left'][i]+750 and dct['top'][i]+2 <= dct['top'][j] <= dct['top'][i]+1150:
                            print('insideloop',dct['text'][j],"dct['text'][j]")
                            if 'mailing_address' in data[img_index].keys():
                                if dct['text'][j]:
                                    data[img_index]['mailing_address'] += ' ' + \
                                        " ".join(dct['text'][j].split())
                            else:
                                data[img_index]['mailing_address'] = " ".join(
                                    dct['text'][j].split())
                if 'mailing_address' in data[img_index].keys():
                    data[img_index]['mailing_address'] = data[img_index]['mailing_address'].strip(
                    )
                if 'liability' in dct['text'][i].lower():
                    data[img_index]['liability'] = dct['text'][i+1]
                if 'liability' in dct['text'][i].lower():
                    data[img_index]['liability'] = dct['text'][i+1]
                if 'property' in dct['text'][i].lower() and 'damage' in dct['text'][i+1].lower():
                    data[img_index]['property_damage'] = dct['text'][i+2]
                if 'personal' in dct['text'][i].lower() and 'injury' in dct['text'][i+1].lower() and 'protection' in dct['text'][i+2].lower():
                    data[img_index]['personal_injury_protection'] = dct['text'][i+3]
                if 'pip' in dct['text'][i].lower() and 'primacy' in dct['text'][i+1].lower() and 'of' in dct['text'][i+2].lower() and 'coverage' in dct['text'][i+3].lower():
                    data[img_index]['pip_primacy_of_coverage'] = dct['text'][i+4]
                if 'pip' in dct['text'][i].lower() and 'medical' in dct['text'][i+1].lower() and 'expense' in dct['text'][i+2].lower() and 'only' in dct['text'][i+3].lower():
                    data[img_index]['pip_medical_expense_only'] = dct['text'][i+4]
                if 'uninsd/underinsd' in dct['text'][i].lower() and 'motorists' in dct['text'][i+1].lower() and 'pd' not in dct['text'][i+2].lower():
                    data[img_index]['uninsd/underinsd_motorists'] = dct['text'][i+2]
                if 'uninsd/underinsd' in dct['text'][i].lower() and 'motorists' in dct['text'][i+1].lower() and 'pd' in dct['text'][i+2].lower():
                    data[img_index]['uninsd/underinsd_motorists_pd'] = dct['text'][i+3]
                if 'comprehensive' in dct['text'][i].lower():
                    data[img_index]['comprehensive'] = dct['text'][i+1]
                if 'collision' in dct['text'][i].lower():
                    data[img_index]['collision'] = dct['text'][i+1]
                if 'rental' in dct['text'][i].lower():
                    data[img_index]['rental'] = dct['text'][i+1]
                if 'personal' in dct['text'][i].lower() and 'property' in dct['text'][i+1].lower() and 'covg' in dct['text'][i+2].lower():
                    data[img_index]['personal_property_covg'] = dct['text'][i+3]
                if 'roadside' in dct['text'][i].lower() and 'assistance' in dct['text'][i+1].lower() and 'coverage' in dct['text'][i+2].lower():
                    data[img_index]['roadside_assistance_coverage'] = dct['text'][i+3]
                if 'total' in dct['text'][i].lower() and 'per' in dct['text'][i+1].lower() and 'vehicle' in dct['text'][i+2].lower():
                    data[img_index]['total_per_vehicle'] = dct['text'][i+3]
            elif 'Discounts' in text:
                data[img_index]['type'] = 'Discounts'
                if 'early' in dct['text'][i].lower() and 'quote' in dct['text'][i+1].lower():
                    data[img_index]['early_quote'] = 'yes'
                if 'good' in dct['text'][i].lower() and 'payer' in dct['text'][i+1].lower():
                    data[img_index]['good_payer'] = 'yes'
                if 'safe' in dct['text'][i].lower() and 'driver' in dct['text'][i+1].lower():
                    data[img_index]['safe_driver'] = 'yes'
                if 'eft' in dct['text'][i].lower() :
                    data[img_index]['eft'] = 'yes'
                if 'multi-policy' in dct['text'][i].lower():
                    data[img_index]['multi_policy'] = 'yes'
                if 'total' in dct['text'][i].lower() and 'savings' in dct['text'][i+1].lower():
                    data[img_index]['total_savings_included'] = dct['text'][i+7]
                if 'driver' in dct['text'][i].lower() and 'name' in dct['text'][i+1].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-50 <= dct['left'][j] <= dct['left'][i]+250 and dct['top'][i]+2 <= dct['top'][j] <= dct['top'][i]+150:
                            if 'driver_name' in data[img_index].keys():
                                if dct['text'][j]:
                                    data[img_index]['driver_name'] += ' ' + \
                                        " ".join(dct['text'][j].split())
                            else:
                                data[img_index]['driver_name'] = " ".join(
                                    dct['text'][j].split())
                if 'dob' in dct['text'][i].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-150 <= dct['left'][j] <= dct['left'][i]+250 and dct['top'][i]+2 <= dct['top'][j] <= dct['top'][i]+150:
                            if 'DOB' in data[img_index].keys():
                                if dct['text'][j]:
                                    data[img_index]['DOB'] += ' ' + \
                                        " ".join(dct['text'][j].split())
                            else:
                                data[img_index]['DOB'] = " ".join(
                                    dct['text'][j].split())
                if 'status' in dct['text'][i].lower() and 'driver' in dct['text'][i+1].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-150 <= dct['left'][j] <= dct['left'][i]+250 and dct['top'][i]+2 <= dct['top'][j] <= dct['top'][i]+150:
                            if 'marital_status' in data[img_index].keys():
                                if dct['text'][j]:
                                    data[img_index]['marital_status'] += ' ' + \
                                        " ".join(dct['text'][j].split())
                            else:
                                data[img_index]['marital_status'] = " ".join(
                                    dct['text'][j].split())
                if 'vehicle' in dct['text'][i].lower() and '&' in dct['text'][i+1].lower() and 'vin' in dct['text'][i+2].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-50 <= dct['left'][j] <= dct['left'][i]+5 and dct['top'][i]+2 <= dct['top'][j] <= dct['top'][i]+150:
                            if 'vehicle_year' in data[img_index].keys():
                                if dct['text'][j]:
                                    data[img_index]['vehicle_year'] += ' ' + \
                                        " ".join(dct['text'][j].split())
                            else:
                                data[img_index]['vehicle_year'] = " ".join(
                                    dct['text'][j].split())
                        if dct['left'][i]+5 <= dct['left'][j] <= dct['left'][i]+1250 and dct['top'][i]+2 <= dct['top'][j] <= dct['top'][i]+150:
                            if 'vehicle_model' in data[img_index].keys():
                                if dct['text'][j]:
                                    data[img_index]['vehicle_model'] += ' ' + \
                                        " ".join(dct['text'][j].split())
                            else:
                                data[img_index]['vehicle_model'] = " ".join(
                                    dct['text'][j].split())
                        if dct['left'][i]-50 <= dct['left'][j] <= dct['left'][i]+1250 and dct['top'][i]+150 <= dct['top'][j] <= dct['top'][i]+550:
                            if 'vin' in data[img_index].keys():
                                if dct['text'][j]:
                                    data[img_index]['vin'] += ' ' + \
                                        " ".join(dct['text'][j].split())
                            else:
                                data[img_index]['vin'] = " ".join(
                                    dct['text'][j].split())
                if 'use' in dct['text'][i].lower() :
                    for j in range(n_boxes):
                        if dct['left'][i]-100 <= dct['left'][j] <= dct['left'][i] and dct['top'][i]+2 <= dct['top'][j] <= dct['top'][i]+350:
                            if 'vehicle_use' in data[img_index].keys():
                                if dct['text'][j]:
                                    data[img_index]['vehicle_use'] += ' ' + \
                                        " ".join(dct['text'][j].split())
                            else:
                                data[img_index]['vehicle_use'] = " ".join(
                                    dct['text'][j].split())
                if 'theft' in dct['text'][i].lower() :
                    for j in range(n_boxes):
                        if dct['left'][i]+50 <= dct['left'][j] <= dct['left'][i]+350 and dct['top'][i]+50 <= dct['top'][j] <= dct['top'][i]+350:
                            if 'anti_theft' in data[img_index].keys():
                                if dct['text'][j]:
                                    data[img_index]['anti_theft'] += ' ' + \
                                        " ".join(dct['text'][j].split())
                            else:
                                data[img_index]['anti_theft'] = " ".join(
                                    dct['text'][j].split())
                if 'lock' in dct['text'][i].lower() :
                    for j in range(n_boxes):
                        if dct['left'][i] <= dct['left'][j] <= dct['left'][i]+250 and dct['top'][i]+2 <= dct['top'][j] <= dct['top'][i]+350:
                            if 'anti_lock' in data[img_index].keys():
                                if dct['text'][j]:
                                    data[img_index]['anti_lock'] += ' ' + \
                                        " ".join(dct['text'][j].split())
                            else:
                                data[img_index]['anti_lock'] = " ".join(
                                    dct['text'][j].split())
                if 'restraint' in dct['text'][i].lower() :
                    for j in range(n_boxes):
                        if dct['left'][i]+50 <= dct['left'][j] <= dct['left'][i]+450 and dct['top'][i]+50 <= dct['top'][j] <= dct['top'][i]+350:
                            if 'passive_restraint' in data[img_index].keys():
                                if dct['text'][j]:
                                    data[img_index]['passive_restraint'] += ' ' + \
                                        " ".join(dct['text'][j].split())
                            else:
                                data[img_index]['passive_restraint'] = " ".join(
                                    dct['text'][j].split())
                if 'premium' in dct['text'][i].lower() :
                    for j in range(n_boxes):
                        if dct['left'][i] <= dct['left'][j] <= dct['left'][i]+100 and dct['top'][i]+2 <= dct['top'][j] <= dct['top'][i]+350:
                            if 'vehicle_premium' in data[img_index].keys():
                                if dct['text'][j]:
                                    data[img_index]['vehicle_premium'] += ' ' + \
                                        " ".join(dct['text'][j].split())
                            else:
                                data[img_index]['vehicle_premium'] = " ".join(
                                    dct['text'][j].split())
                if 'name' in dct['text'][i].lower() and 'term' in dct['text'][i+1].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-50 <= dct['left'][j] <= dct['left'][i]+1100 and dct['top'][i]+2 <= dct['top'][j] <= dct['top'][i]+150:
                            if 'taxes_name' in data[img_index].keys():
                                if dct['text'][j]:
                                    data[img_index]['taxes_name'] += ' ' + \
                                        " ".join(dct['text'][j].split())
                            else:
                                data[img_index]['taxes_name'] = " ".join(
                                    dct['text'][j].split())
                if 'term' in dct['text'][i].lower() and 'amount' in dct['text'][i+1].lower():
                    for j in range(n_boxes):
                        if dct['left'][i]-50 <= dct['left'][j] <= dct['left'][i]+1100 and dct['top'][i]+2 <= dct['top'][j] <= dct['top'][i]+150:
                            if 'term_amount' in data[img_index].keys():
                                if dct['text'][j]:
                                    data[img_index]['term_amount'] += ' ' + \
                                        " ".join(dct['text'][j].split())
                            else:
                                data[img_index]['term_amount'] = " ".join(
                                    dct['text'][j].split())
                if 'total' in dct['text'][i].lower():
                    data[img_index]['total_amount'] = dct['text'][i+1]
            else:
                data[img_index]['type'] = 'not supported document'
    return data

        # if dct['left'][i] <= 3000 and dct['top'][i] == 699:
        # print(dct['text'][i], 'left', dct['left'][i], 'top', dct['top']
        #   [i], 'width', dct['width'][i], 'height', dct['height'][i])
        # import ipdb
        # ipdb.set_trace()
