import traceback
import sys
import gribapi as gapi

from generic_file import GenericFile

class GribFile(GenericFile):
    """
    Simple class for returning basic information about the content
    of an NetCDF file.
    """

    def __init__(self, file_path, level):
        GenericFile.__init__(self, file_path, level)

    def get_handler_id(self):
        return self.handler_id

    def phenomena(self):

        """
        Construct list of Phenomena based on variables in Grib file.
        :returns : List of phenomena.
        """
        phenomenon_attr = {}
        phenomena_list = []
        phenomenon_parameters_dict = {}
        phenomenon_attr_found = {}

        try:
            f = open(self.file_path)

            phen_keys = "paramId cfNameECMF cfName cfVarName units nameECMF name".split()
            found = set()

            while 1:
                gid = gapi.grib_new_from_file(f)
                if gid is None: break

                list_of_phenomenon_parameters = []
                list_of_phenomenon_parameters_t = []

                for key in phen_keys:

                    if not gapi.grib_is_defined(gid, key):
                        break

                    value = str(gapi.grib_get(gid, key))
                    phenomenon_attr["name"] = key
                    phenomenon_attr["value"] = value

                    list_of_phenomenon_parameters.append(phenomenon_attr.copy())
                    list_of_phenomenon_parameters_t.append((key, value))


                #Also add var_id
                phenomenon_attr["name"] = "var_id"
                phenomenon_attr["value"] = "None"
                list_of_phenomenon_parameters.append(phenomenon_attr.copy())
                phenomenon_attr.clear()

                list_of_phenomenon_parameters_t.append(("name", "None"))
                list_of_phenomenon_parameters_tt = tuple(list_of_phenomenon_parameters_t)

                if list_of_phenomenon_parameters_tt not in found:
                    found.add(list_of_phenomenon_parameters_tt)
                    #Dict of phenomenon attributes.
                    phenomenon_parameters_dict["phenomenon_parameters"] = list_of_phenomenon_parameters

                    #list of phenomenon.
                    phenomena_list.append(phenomenon_parameters_dict.copy())
                    phenomenon_parameters_dict.clear()
                else:
                    phenomenon_parameters_dict.clear()

                gapi.grib_release(gid)

            f.close()
            """ 
            phenomena_list_unique = []
            for item in phenomena_list:
                if item not in phenomena_list_unique:
                    phenomena_list_unique.append(item)
            """
            return phenomena_list

        except Exception as e:
            print e
            return None

    def get_properties_grib_level2(self):
        """
        Wrapper for method phenomena().
        :returns:  A dict containing information compatible with current es index.
        """

        pp_phenomena = self.phenomena()

        if pp_phenomena is not None:

            #Get basic file info.
            file_info = self.get_properties_generic_level1()

            self.handler_id = "grib handler level 2."
            file_info["phenomena"] = pp_phenomena

            return file_info

        else:
            return self.get_properties_generic_level2()

    def get_properties(self):

        if self.level == "1":
            return self.get_properties_generic_level1()
        elif self.level  == "2":
            return self.get_properties_grib_level2()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass