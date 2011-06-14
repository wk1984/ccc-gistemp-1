#! /usr/bin/env python
# $URL$
# $Rev$
#
# read_config.py
#
# Nick Barnes, Ravenbrook Limited, 2010-01-16

"""
Python code to read the various config and station files used by
GISTEMP:
"""

import os

def v2_get_sources():
    """Reads the three tables mcdw.tbl, ushcn2.tbl, sumofday.tbl and
    return a dictionary that maps from 12-digit (string) station ID to
    the source (which is one of the strings 'MCDW', 'USHCN2',
    'SUMOFDAY').
    """

    sources = {}
    for source in ['MCDW', 'USHCN2', 'SUMOFDAY']:
        for line in open('input/%s.tbl' % source.lower()):
            _, id11, duplicate = line.split()
            sources[id11 + duplicate] = source
    return sources


def step1_adjust():
    """Reads the file config/step1_adjust into a dict,
    mapping a record identifier to a tuple (year, month, summand).
    By convention the month is 1 for January."""

    adjust = {}
    for line in open('config/step1_adjust', 'r'):
        id, _, year, month, summand = line.split()
        adjust[id] = (int(year), int(month), float(summand))
    return adjust


def get_changes_dict():
    """Reads the file config/Ts.strange.RSU.list.IN and returns a dict
    result.  Each line in that file begins with a 12-digit station ID
    - actually the tuple (country-code, WMO station, modifier,
    duplicate) - and ends with either yyyy/mm, specifying a month
    datum to omit or with xxxx-yyyy, specifying years to omit.  xxxx
    can be 0, meaning from the beginning. yyyy can be 9999, meaning to
    the end.  The dict is a map from ID to ('month',yyyy,mm) or
    ('years',xxxx,yyyy).
    """

    dict = {}
    for line in open('config/Ts.strange.RSU.list.IN', 'r'):
        split_line = line.split()
        id = split_line[0]
        try:
            year1, year2 = map(int, split_line[-1].split("-"))
            val = ("years", year1, year2)
        except ValueError:
            year, month = map(int, split_line[-1].split("/"))
            val = ("month", year, month)
        dict[id] = dict.get(id,[])
        dict[id].append(val)
    return dict

def generate_deafults():
    """Hack to generate GISTEMP default config files."""

    # step1_adjust: originally (?) info/use (?)
    step1_adjust = """147619010000 147619010002 1976 8 1.0
    425911650000 dummy 1949 12 0.84"""

    # Ts.strange.RSU.list.IN: originally found (?) info/use (?)
    Ts_strange_RSU_list_IN = """122637720000 LAMU                      lat,lon   -2.3   40.8 omit: 1914/07
    148628400000 MALAKAL                   lat,lon    9.6   31.7 omit: 1990/08
    148628400000 MALAKAL                   lat,lon    9.6   31.7 omit: 1991/03
    215442140000 UIGI                      lat,lon   48.9   89.9 omit: 2010/04
    223404300002 MADINAH                   lat,lon   24.6   39.7 omit: 2010/05
    303838210000 IGUAPE                    lat,lon  -24.7  -47.5 omit: 1985/04
    403718670006 THE PAS,MAN.              lat,lon   54.0 -101.1 omit: 1995/05
    614028360003 SODANKYLA                 lat,lon   67.4   26.7 omit: 2010/03
    614028690001 KUUSAMO                   lat,lon   66.0   29.2 omit: 2010/03
    614028750001 OULU                      lat,lon   64.9   25.4 omit: 2010/03
    614028970003 KAJAANI                   lat,lon   64.3   27.7 omit: 2010/03
    614029290001 JOENSUU                   lat,lon   62.7   29.6 omit: 2010/03
    614029350003 JYVASKYLA                 lat,lon   62.4   25.7 omit: 2010/03
    614029580001 LAPPEENRANTA              lat,lon   61.1   28.2 omit: 2010/03
    614029630003 JOKIOINEN                 lat,lon   60.8   23.5 omit: 2010/03
    614029720003 TURKU                     lat,lon   60.5   22.3 omit: 2010/03
    614029740000 HELSINKI/SEUTULA          lat,lon   60.3   25.0 omit: 2010/03
    501947190020 GILGANDRA POST OFFICE     lat,lon  -31.7  148.7 omit: 1920/07
    651032920010 SCARBOROUGH UK            lat,lon   54.2    -.4 omit: 1912/08
    651032920010 SCARBOROUGH UK            lat,lon   54.2    -.4 omit: 1912/09
    623160900003 VERONA/VILLAF             lat,lon   45.4   10.9 omit: 1987/04
    623161580004 PISA/S.GIUST              lat,lon   43.7  161.5 omit: 1987/10
    113655550000 BOUAKE                    lat,lon    7.7   -5.1 omit: 0-1954
    115624500010 SUEZ                      lat,lon   29.9   32.6 omit: 0-1888
    140632500000 BARDERA                   lat,lon    2.4   42.3 omit: 0-1919
    150617010000 BATHURST/YUNDUM           lat,lon   13.4  -16.7 omit: 0-1939
    155674750003 KASAMA                    lat,lon  -10.2   31.1 omit: 0-1932
    205526520000 ZHANGYE                   lat,lon   38.9  100.4 omit: 0-1944
    205528360002 DULAN                     lat,lon   36.3   98.1 omit: 0-1949
    205535640010 XINGXIAN                  lat,lon   38.5  111.1 omit: 0-1929
    205538630000 JIEXIU                    lat,lon   37.1  111.9 omit: 0-1950
    205560800020 LINXIA                    lat,lon   35.6  103.2 omit: 0-1951
    205565710002 XICHANG                   lat,lon   27.9  102.3 omit: 0-1938
    205565860010 LEIBO                     lat,lon   28.3  103.6 omit: 0-1954
    205573480000 FENGJIE                   lat,lon   31.1  109.5 omit: 0-1956
    205577990000 JI'AN                     lat,lon   27.1  115.0 omit: 0-1934
    302853650000 YACUIBA                   lat,lon  -21.9  -63.6 omit: 0-1935
    315814050000 CAYENNE/ROCHA             lat,lon    4.8  -52.4 omit: 0-1911
    403717140040 SHAWINIGAN,QU             lat,lon   46.6  -72.7 omit: 0-1918
    414765560010 MASCOTA, JALISCO          lat,lon   20.5 -104.8 omit: 0-1940
    414767260010 CUAUTLA, MORELOS          lat,lon   18.8  -98.9 omit: 0-1953
    425702710000 GULKANA/INTL.             lat,lon   62.2 -145.4 omit: 0-1930
    425725910004 RED BLUFF/MUN             lat,lon   40.2 -122.2 omit: 0-1889
    425745090010 LOS GATOS           USA   lat,lon   37.2 -122.0 omit: 0-1890
    432788970000 LE RAIZET,GUA             lat,lon   16.3  -61.5 omit: 0-1940
    501943330000 BOULIA                    lat,lon  -22.9  139.9 omit: 0-1899
    501943660010 BOWEN POST OFFICE         lat,lon  -20.0  148.3 omit: 0-1909
    501945660000 GYMPIE (FORES             lat,lon  -26.1  152.6 omit: 0-1909
    501945890000 YAMBA                     lat,lon  -29.4  153.4 omit: 0-1899
    501947840000 TAREE                     lat,lon  -31.9  152.5 omit: 0-1909
    501948420000 CAPE OTWAY                lat,lon  -38.8  143.5 omit: 0-1900
    501949330000 GABO ISLAND               lat,lon  -37.6  149.9 omit: 0-1899
    501949370000 MORUYA HEADS              lat,lon  -35.9  150.2 omit: 0-1898
    523969950000 CHRISTMAS ISL             lat,lon  -10.4  105.7 omit: 0-1970
    636085060002 HORTA (ACORES             lat,lon   38.5  -28.6 omit: 0-1916
    205544710010 GAIXIAN XIONGYUE          lat,lon   40.2  122.2 omit: 1920-1930
    205567780004 KUNMING                   lat,lon   25.0  102.7 omit: 1940-1945
    207425150003 CHERRAPUNJI               lat,lon   25.3   91.7 omit: 1991-1993
    403718260000 NITCHEQUON                lat,lon   53.3  -70.9 omit: 2000-9999
    115624640010 HURGHADA                  lat,lon   27.3   33.8 omit: 0-9999
    134652010000 LAGOS/IKEJA               lat,lon    6.6    3.3 omit: 0-9999
    134652360000 WARRI                     lat,lon    5.5    5.7 omit: 0-9999
    134652430000 LOKOJA                    lat,lon    7.8    6.7 omit: 0-9999
    205549450010 JUXIAN                    lat,lon   35.6  118.8 omit: 0-9999
    207433330002 PORT BLAIR                lat,lon   11.7   92.7 omit: 0-9999
    210476960010 YOKOSUKA                  lat,lon   35.3  139.7 omit: 0-9999
    219415600005 PARACHINAR                lat,lon   33.9   70.1 omit: 0-9999
    303824000000 FERNANDO DE N             lat,lon   -3.9  -32.4 omit: 0-9999
    314804440000 CIUDAD BOLIVA             lat,lon    8.2  -63.5 omit: 0-9999
    403717300040 RUEL,ON                   lat,lon   47.3  -81.4 omit: 0-9999
    414762200010 CIUDAD GUERRERO,CHIHUAHUA lat,lon   28.6 -107.5 omit: 0-9999
    414762580020 QUIRIEGO, SONORA          lat,lon   27.5 -109.2 omit: 0-9999
    414763730000 TEPEHUANES,DG             lat,lon   25.4 -105.7 omit: 0-9999
    414766950010 CHAMPOTON, CAMPECHE       lat,lon   19.4  -90.7 omit: 0-9999
    414767750030 CANTON, OAXACA            lat,lon   18.0  -96.3 omit: 0-9999
    440785260010 ANNAS HOPE, ST.CROIX VIRG lat,lon   17.7  -66.7 omit: 0-9999
    425724910030 HOLLISTER USA             lat,lon   36.8 -121.4 omit: 0-9999
    501947880000 KEMPSEY                   lat,lon  -31.0  152.8 omit: 0-9999
    643081600003 ZARAGOZA AERO       SPAIN lat,lon   41.7   -1.0 omit: 0-9999
    643083300010 SINTRA/GRANJA             lat,lon   38.8   -9.3 omit: 0-9999
    643083730010 ALBACETE            SPAIN lat,lon   39.0    1.8 omit: 0-9999"""

    directory = 'config'

    if not os.path.exists(directory):
        os.makedirs(directory)

    # here goes step1_adjust
    path = os.path.join(directory, 'step1_adjust')
    if not os.path.isfile(path):
        text_file = open(path, 'w')
        text_file.write(step1_adjust)
        text_file.close()

    # here goes Ts.strange.RSU.list.IN
    path = os.path.join(directory, 'Ts.strange.RSU.list.IN')
    if not os.path.isfile(path):
        text_file = open(path, 'w')
        text_file.write(Ts_strange_RSU_list_IN)
        text_file.close()