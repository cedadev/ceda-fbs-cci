from pyhdf.HDF import *
from pyhdf.V import *
from pyhdf.VS import *

from _dataset import _geospatial
from metadata import product


class HDF4(_geospatial):
    """
    ARSF HDF4 context manager class.
    """
    def __init__(self, fname):
        """
        :param str fname: The path of the HDF4 file.
        """
        self.fname = fname

    def __enter__(self):
        """
        Open HDF file and interfaces for use as context manager.
        :return self:
        """
        self.hdf = HDF(self.fname)
        self.vs = self.hdf.vstart()
        self.v = self.hdf.vgstart()

        return self

    def __exit__(self, *args):
        """
        Close interfaces and HDF file after finishing use in context manager.
        """
        self.v.end()
        self.vs.end()
        self.hdf.close()

    def _get_coords(self, v, vs, fn):
        """
        Iterate through vgroup and return a list of coordinates (if existing).

        :param HDF4.V.v v: VGroup object
        :param HDF4.V.vs vs: VData object
        :param str fn: Filename of the object
        :return dict: Dict containing geospatial and temporal information.
        """
        mappings = {
            "NVlat2": "lat",
            "NVlng2": "lon",
        }

        coords = {}
        for k, v in mappings.iteritems():
            ref = vs.find(k)
            vd = vs.attach(ref)

            coords[v] = []
            while True:
                try:
                    coord = float(vd.read()[0][0]) / (10**7)
                    coords[v].append(coord)
                except HDF4Error:  # End of file
                    break

            vd.detach()
        return coords

    def get_geospatial(self):
        """
        Search through HDF4 file, returning a list of coordinates from the
        'Navigation' vgroup (if it exists).

        :return dict: Dict containing geospatial and temporal information.
        """
        ref = -1
        while True:
            try:
                ref = self.v.getid(ref)
                vg = self.v.attach(ref)

                if vg._name == "Navigation":
                    geospatial = self._get_coords(self.v, self.vs, self.fname)
                    vg.detach()
                    return geospatial

                vg.detach()
            except HDF4Error:
                break

    def get_temporal(self):
        # TODO
        return None

    def get_properties(self):
        geospatial = self.get_geospatial()
        temporal = self.get_temporal()
        file_level = super(HDF4, self).get_file_level(self.fname)
        data_format = {
            "format": "HDF4",
        }

        props = product.Properties(spatial=geospatial,
                                   temporal=temporal,
                                   file_level=file_level,
                                   data_format=data_format)

        return props