"""
MFF UK - 2019/20 Winter - Programing 1 - Credit Program
@author Václav Hrouda - wujido (vahrouda@gmail.com)

Class used to handling game file
"""

import json

import config


class DataHandler:
    """
    A class used to handling game file
    Serves as interface between program and storing technology


    Attributes
    ----------
    source_file : str
        Name of source file
    source : dict
        Data represented as dictionary


    Methods
    -------
    get_data(key)
        Return data of provided key
    set_data(key, data)
        Set data to provided key
    save()
        Save data to the file
    """

    def __init__(self, filename, data=None):
        """
        Constructor of DataHandler class

        If the `data` attribute is provided, initial state is not read from the file

        Parameters
        ----------
        filename : int
            Name of file
        data : dict
            Optional, initial state of the file
        """

        self.source_file = filename

        if data:
            self.source = data
            self.save()
        else:
            try:
                file = open(self.source_file, 'r')
                self.source = json.loads(file.read())
            finally:
                file.close()

    def get_data(self, key):
        """
        Return data of provided key

        Parameters
        ----------
        key : str
            Key of required data

        Returns
        -------
        any
            Required data
        """

        return self.source[key]

    def set_data(self, key, data):
        """
        Set data to provided key

        Parameters
        ----------
        key : str
            Key of required data
        data : any
            Data to save


        Returns
        -------
        any
            Required data
        """

        self.source[key] = data
        self.source[config.STATE_KEY]["step"] += 1
        self.save()

    def save(self):
        """
        Save local source data to the file
        """

        try:
            file = open(self.source_file, 'w')
            file.write(json.dumps(self.source))
        finally:
            file.close()
