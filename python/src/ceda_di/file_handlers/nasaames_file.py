from ceda_di.file_handlers.generic_file import GenericFile
from ceda_di.metadata import product
import nappy


class NasaAmesFile(GenericFile):
    """
    Class for returning basic information about the content
    of an nasaames file.
    """

    def __init__(self, file_path, level):
        GenericFile.__init__(self, file_path, level)

    def get_handler_id(self):
        return self.handler_id

    def phenomena(self):

        try:
            na_fhandle = nappy.openNAFile(self.file_path)

            variables = {}
            for var in na_fhandle.getVariables():
                variables.update({
                    var[0]: {
                        "name": var[0],
                        "units": var[1]
                    }
                })

            variables = [product.Parameter(k, other_params=var) for (k, var) in variables.iteritems()]
            return variables
        except Exception:
            return None

    def get_properties_nanaames_level2(self):

        #Get basic file info.
        file_info = self.get_properties_generic_level1()

        if file_info is not None:

            self.handler_id = "Nasaames handler level 2."

            nasaames_phenomena = self.phenomena()

            if nasaames_phenomena is None:
                return None

            #List of phenomena
            phenomena_list = []
            var_id_dict = {}
            phenomenon_parameters_dict = {}

            for item in nasaames_phenomena:           #get all parameter objects.

                name = item.get_name()               #get phenomena name.

                var_id_dict["name"] = "var_id"
                var_id_dict["value"] = name

                list_of_phenomenon_parameters = item.get()
                list_of_phenomenon_parameters.append(var_id_dict.copy())
                phenomenon_parameters_dict["phenomenon_parameters"] = list_of_phenomenon_parameters

                phenomena_list.append(phenomenon_parameters_dict.copy())

                var_id_dict.clear()
                phenomenon_parameters_dict.clear()


            file_info["phenomena"] = phenomena_list


            return file_info

        else:
            return self.get_properties_generic_level2()

    def get_properties_nanaames_level3(self):
       return self.get_properties_nanaames_level2()

    def get_properties(self):

        if self.level == "1":
            return self.get_properties_generic_level1()
        elif self.level == "2":
            return self.get_properties_nanaames_level2()
        elif self.level == "3":
            return self.get_properties_nanaames_level3()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass
