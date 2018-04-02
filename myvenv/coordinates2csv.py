#!/usr/bin/env python

import sys, argparse, re, csv
from TexSoup import TexSoup

parser = argparse.ArgumentParser(
    description='Extracts and converts client name, address included in a gad-releveFactures-XXX.tex file to a csv file.',
    epilog=str(sys.argv[0])+' output.csv input.tex'
    )
parser.add_argument('csv', nargs='+', help='bar help')
parser.add_argument('file', nargs='+', help='bar help')

output = parser.parse_args()

def get_flushright(filename):
    raw = open(filename)
    soup = TexSoup(raw.read())
    raw.close()

    flushright = list(
            soup.find_all('flushright')
            )

    try:
        address = flushright[2]
    except:
        address=None

    return address


def try_get_string(tex):
    try:
        return tex.string
    except:
        return tex

def try_strip(string):
    try:
        string = ' '.join(string.split('\n'))
        string = ' '.join(string.split('\t'))
        string = '_'.join(string.split('\_'))
        string = ' '.join(string.split('\\'))
        string = ' '.join(string.split(r' +'))
        return string.strip()
    except:
        return string

def try_normalize(string):
    pattern = re.compile(r"[\d\w@\ \.\-_,\\\(\)\+\']+")
    m = pattern.search(string)  
    if(m):
        return m.group(0)
    
def try_get_city(li):
    pattern = re.compile(r"\d+\s*([\w\ \.\-_,\(\)\']+)")
    for i in reversed(range(5,11)):
        if(not li[i]):
            continue
        m = pattern.search(li[i])
        if(m):
            return m.group(1)
    raise RuntimeError('No city name found in ', li)
    
def try_get_zip_code(li):
    pattern = re.compile(r"(\d+)\s*([\w\ \.\-_,\(\)\']+)")
    for i in reversed(range(5,11)):
        if(not li[i]):
            continue
        m = pattern.search(li[i])
        if(m):
            return m.group(1)
    raise RuntimeError('No zip code found in ', li)

def try_get_country(li):
    pattern = re.compile(r"^\s*([^\d@]+)\s*$")
    for i in reversed(range(5,len(li))):
        if(not li[i] or 'None' == li[i]):
            continue
        m = pattern.search(li[i])
        if(m):
            return m.group(1)
    raise RuntimeError('No country name found in ', li)
    
def try_get_phone(li):
    pattern = re.compile(r"\d+$")
    for i in reversed(range(11,len(li))):
        if(not li[i] or 'None' == li[i]):
            continue
        m = pattern.search(li[i])
        if(m):
            return m.group(0)
    return None
    
def try_get_email(li):
    pattern = re.compile(r"^\s*([\w\.\-_]+@[\w\.\-_]+)\s*$")
    for i in reversed(range(13,len(li))):
        if(not li[i] or 'None' == li[i]):
            continue
        m = pattern.search(li[i])
        if(m):
            return m.group(1)
    return None

def try_get_name(li):
    return li[0]

def try_get_last_name(li):
    return li[1]

def try_get_company(li):
    pattern = re.compile(r"^([^\d][\w\ \.\-_,\(\)\'\d]+)\s*$")
    for i in range(3,4):
        if(not li[i] or 'None' == li[i]):
            continue
        m = pattern.search(li[i])
        if(m):
            return m.group(1)
    return None

def try_get_street(li):
    pattern = re.compile(r"^\s*(\d{0,3}[^\d][\w\ \.\-_,\(\)\']+)\s*$")
    for i in reversed(range(3,8)):
        if(not li[i] or 'None' == li[i]):
            continue
        m = pattern.search(li[i])
        if(m):
            return m.group(1)
    raise RuntimeError('No street found in ', li)


csvfile = open(sys.argv[1], 'w', newline='')
fieldnames = [
    'name',
    'last_name',
    'company',
    'street',
    'zip_code',
    'city',
    'country',
    'phone',
    'email',
    'url',
    ]
writer = csv.DictWriter(csvfile, delimiter=';' ,fieldnames=fieldnames)
writer.writeheader()


for filename in sys.argv[2:]:
    address = get_flushright(filename)
    if(not address):
        continue
    text = list(address.contents)

    text = [try_get_string(t) for t in text]
    text = [try_strip(t) for t in text]
    text = [try_normalize(str(t)) for t in text]

    d = {
        'name'          : try_get_name(text),
        'last_name'     : try_get_last_name(text),
        'company'       : try_get_company(text),
        'street'        : try_get_street(text),
        'zip_code'      : try_get_zip_code(text),
        'city'          : try_get_city(text),
        'country'       : try_get_country(text),
        'phone'         : try_get_phone(text),
        'email'         : try_get_email(text),
        'url'           : 'file://'+filename,
        }
    print(text)
    print(d)
    writer.writerow(d)

