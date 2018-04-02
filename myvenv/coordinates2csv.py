#!/usr/bin/env python
# coordinates2csv.py
# Created: 2nd april 2018

'''
This will extract name, address and other contact info
from a gad-releveFactures-*.tex file and write it to a
csv file.
Attention ! A column is used as the separator instead
of the traditional comma.
'''

__author__ = 'Yevgueny KASSINE'
__version__ = '0.1'

import sys, argparse, re, csv
from TexSoup import TexSoup

def get_parser():
    parser = argparse.ArgumentParser(
        description='Extracts and converts client name, address included in a gad-releveFactures-XXX.tex file to a csv (column replaces the traditionnal comma) file.',
        epilog=str(sys.argv[0])+' output.csv input.tex'
        )
    parser.add_argument('csv', type=str, nargs=1, help='writable output csv file')
    parser.add_argument('tex', type=str, nargs='+', help='readable input tex file')
    return parser

def get_flushright(filename):
    with open(filename) as raw:
        soup = TexSoup(raw.read())

    flushright = list(
            soup.find_all('flushright')
            )

    try:
        res = flushright[2]
    except:
        res = None
    finally:
        return res


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


def main():
    '''
    This will be called if the script is directly invoked.
    '''
    parser = get_parser()
    args = vars(parser.parse_args())

    ofn = args['csv'][0]
    ifn = args['tex']
    
    with open(ofn, 'w', newline='') as csvfile:
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

        for filename in ifn:
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
            writer.writerow(d)


if __name__ == '__main__':
    main()
