'''
Created on 2 Jun 2016

@author: kleanthis
'''
import csv
import re

import ceda_fbs.proc.common_util.util as util

from .generic_file import GenericFile

class BadcCsvFile(GenericFile):

    def __init__(self, file_path, level, additional_param=None, **kwargs):
        GenericFile.__init__(self, file_path, level, **kwargs)
        self.handler_id = "BADC CSV"
        self.FILE_FORMAT = self.get_file_format()

    def get_file_format(self):
        with open(self.file_path, encoding='utf-8', errors='ignore') as fp:
            if 'BADC-CSV' in fp.readline():
                return 'BADC CSV'
            else:
                return 'CSV'

    def csv_parse(self, fp):

        phenomena = {}
        date = None
        location = None

        reader = csv.reader(fp)

        for row in reader:
            new_phenomenon = {}

            if row[0] == "data":
                break
            elif row[1] == "G":
                if row[0] == "date_valid":
                    date = row[2]
                if row[0] == "location":
                    location = row[2]
                continue
            else:
                if row[1] in phenomena:
                    phenomena[row[1]]["attributes"].append({"name": row[0], "value": re.sub(r'[^\x00-\x7F]+',' ', row[2])})
                    try:
                        if row[0] in ["standard_name","long_name"] and len(row) == 4:
                            phenomena[row[1]]["attributes"].append({"name": "units", "value": row[3]})
                    except IndexError:
                        pass

                else:
                    new_phenomenon["attributes"] = []
                    new_phenomenon["attributes"].append({"name": row[0], "value": re.sub(r'[^\x00-\x7F]+',' ', row[2])})
                    try:
                        if row[0] in ["standard_name","long_name"] and len(row) == 4:
                            new_phenomenon["attributes"].append({"name": "units", "value": row[3]})

                    except IndexError:
                        pass
                    phenomena[row[1]] = new_phenomenon

        return (phenomena, date, location)

    def get_phenomena(self, fp):

        phen_list = []

        phenomena, _, _ = self.csv_parse(fp)

        for key in phenomena.keys():
            phen_list.append(phenomena[key])

        file_phenomena = util.build_phenomena(phen_list)

        return file_phenomena

    def get_metadata_level2(self):
        self.handler_id = "CSV handler level 2."

        file_info = self.get_metadata_level1()

        if file_info is not None:
            try:
                with open(self.file_path, encoding='utf-8', errors='ignore') as fp:
                    phen = self.get_phenomena(fp)

            except Exception:
                # Error reading file or getting phenomena
                file_info[0]["info"]["read_status"] = "Read Error"
                return file_info + (None,)

            else:
                # successful file read
                file_info[0]["info"]["read_status"] = "Successful"

                return file_info + phen

        else:
            return None

    def get_metadata_level3(self):
        self.handler_id = "CSV handler level 3."

        loc = (None,)

        file_info = self.get_metadata_level1()

        if file_info is not None:
            try:
                with open(self.file_path, encoding='utf-8', errors='ignore') as fp:
                    meta = self.csv_parse(fp)
                    fp.seek(0)
                    phenomena = self.get_phenomena(fp)

            except Exception:
                # Problem reading file or extracting metadata
                file_info[0]["info"]["read_status"] = "Read Error"
                return file_info

            # Read Successful
            if meta[1] is not None:
                # Constrain date output to isoformat
                iso_date = util.date2iso(meta[1])

                file_info[0]["info"]["temporal"] = {
                    "time_range": {
                        "gte": iso_date,
                        "lte": iso_date
                    },
                    "start_time": iso_date,
                    "end_time": iso_date
                }
            if meta[2] is not None:
                if meta[2] == 'global':
                    loc = ({'coordinates': {'type': 'envelope', 'coordinates': [[-180.0,90.0], [180.0, -90.0]]}},)

            file_info[0]["info"]["read_status"] = "Successful"

            return file_info + phenomena + loc
        else:
            return None

    def get_metadata(self):

        if self.FILE_FORMAT == 'CSV':
            return self.get_metadata_level1()
        else:
            return super().get_metadata()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

if __name__ == "__main__":
    import datetime
    import sys

    # run test
    try:
        level = str(sys.argv[1])
        file = sys.argv[2]
    except IndexError:
        level = '1'
        file = '/badc/ukmo-metdb/data/amdars/2016/12/ukmo-metdb_amdars_20161222.csv'

    baf = BadcCsvFile(file,level)
    start = datetime.datetime.today()
    print( baf.get_metadata())
    end = datetime.datetime.today()
    print( end-start)