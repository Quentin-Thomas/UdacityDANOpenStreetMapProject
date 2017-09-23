#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 14:35:40 2017

@author: quentinthomas
"""


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import process_map

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    process_map.process_map('bdx_sample.osm', True)


if __name__ == "__main__":
    test()