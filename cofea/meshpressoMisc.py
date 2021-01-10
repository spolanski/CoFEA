# POINT,
# LINE-LIN,
# LINE-QUAD,
# TRI-LIN
# TRI-QUAD
# QUAD-LIN
# QUAD-QUAD
# TET-LIN
# TET-QUAD
# HEX-LIN
# HEX-QUAD
# WEDGE-LIN
# WEDGE-QUAD
# UNV element types
# http://victorsndvg.github.io/FEconv/formats/unv.xhtml
from collections import OrderedDict

class ElementLibrary(object):
    el_library = {
        'PSTRAIN-TRI': {
            'LIN': {
                'ABQ': ['CPE3', ],
                'CCX': ['CPE3', ],
                'UNV': ['51', ],
                },
            'PARA': {
                'ABQ': ['CPE6', 'CPE6M', ],
                'CCX': ['CPE6', ],
                'UNV': ['52', ],
            }
        },
        'PSTRAIN-QUAD': {
            'LIN': {
                'ABQ': ['CPE4', 'CPE4R', 'CPE4H', 'CPE4I', ],
                'CCX': ['CPE4', 'CPE4R', ],
                'UNV': ['54', ],
                },
            'PARA': {
                'ABQ': ['CPE8', 'CPE8R', ],
                'CCX': ['CPE8', 'CPE8R',],
                'UNV': ['55', ],
            }
        },
        'PSTRESS-TRI': {
            'LIN': {
                'ABQ': ['CPS3', ],
                'CCX': ['CPS3', ],
                'UNV': ['41', ],
                },
            'PARA': {
                'ABQ': ['CPS6', 'CPS6M', ],
                'CCX': ['CPS6', ],
                'UNV': ['42', ],
            }
        },
        'PSTRESS-QUAD': {
            'LIN': {
                'ABQ': ['CPS4', 'CPS4R', 'CPS4I' ],
                'CCX': ['CPS4', 'CPS4R', ],
                'UNV': ['44', ],
                },
            'PARA': {
                'ABQ': ['CPS8', 'CPS8R', ],
                'CCX': ['CPS8', 'CPS8R',],
                'UNV': ['45', ],
            }
        },
        'SHELL-TRI': {
            'LIN': {
                'ABQ': ['S3', ],
                'CCX': ['S3', ],
                'UNV': ['91', ],
                },
            'PARA': {
                'ABQ': ['S8R', ],
                'CCX': ['S8R', 'S8'],
                'UNV': ['92', ],
            }
        },
        'SHELL-QUAD': {
            'LIN': {
                'ABQ': ['S4', 'S4R', ],
                'CCX': ['S4', 'S4R', ],
                'UNV': ['94', ],
                },
            'PARA': {
                'ABQ': ['S8R', ],
                'CCX': ['S8R', 'S8'],
                'UNV': ['95', ],
            }
        },
        'SOLID-TET': {
            'LIN': {
                'ABQ': ['C3D4', ],
                'CCX': ['C3D4', ],
                'UNV': ['111', ],
                },
            'PARA': {
                'ABQ': ['C3D10', ],
                'CCX': ['C3D10', ],
                'UNV': ['118', ],
            }
        },
        'SOLID-WEDGE': {
            'LIN': {
                'ABQ': ['C3D6',],
                'CCX': ['C3D6', ],
                'UNV': ['112', ],
                },
            'PARA': {
                'ABQ': ['C3D15', ],
                'CCX': ['C3D15', ],
                'UNV': ['113', ],
            }
        },
        'SOLID-HEX': {
            'LIN': {
                'ABQ': ['C3D8', 'C3D8R'],
                'CCX': ['C3D8R', 'C3D8I'],
                'UNV': ['115', ],
                },
            'PARA': {
                'ABQ': ['C3D20', 'C3D20R'],
                'CCX': ['C3D20', 'C3D20R', 'C3D20RI' ],
                'UNV': ['116', ],
            }
        },
    }

    def __init__(self):
        self.el_container = []
        for topo, val in self.el_library.items():
            for shape_func, soft_type_val in val.items():
                for soft, el_list in soft_type_val.items():
                    temp = [(topo, shape_func, soft, e)
                            for e in el_list]
                    self.el_container.extend(temp)

    def convert_to_general(self, el_type='C3D4'):
        gen_element = [el[:2] for ind, el in enumerate(self.el_container)
                       if el_type in el]
        
        if all(gen_element):
            # if all elements have the same topology and shape function
            return gen_element[0]
        else:
            raise ValueError('Unique topology and shape function not found')
    
    def convert_to_specific_format(self, general_format=('SOLID-TET', 'LIN'),
                                   output = 'ABQ'):
        topo, shape = general_format
        spec_form = [el for el in self.el_container
                     if (topo in el) and (shape in el)]
        
        spec_soft = [el for el in spec_form
                     if output in el]
        
        if len(spec_soft) >= 1:
            element_type = spec_soft[0][-1]
        else:
            raise ValueError('Element not found')
        return element_type

# el_types = ElementLibrary()
# a = el_types.convert_to_general()
# print el_types.convert_to_specific_format(gen_el_def=a,
#                                           soft='ABQ')


# elementTypes = (
#     OrderedDict([('ABQ', 'S3'), ('CCX', 'S3'), ('UNV', '91')]),
#     OrderedDict([('ABQ', 'STRI65'), ('CCX', 'S6'), ('UNV', '92')]),
#     OrderedDict([('ABQ', 'C3D15'), ('CCX', 'C3D15'), ('UNV', '113')]),
#     )

ccxSurfaceDefiniton = {
    'SOLID-TET': {
        'S1': [0, 1, 2],
        'S2': [0, 3, 1],
        'S3': [1, 3, 2],
        'S4': [2, 3, 0],
    },
    'SOLID-WEDGE': {
        'S1': [0, 1, 2],
        'S2': [3, 4, 5],
        'S3': [0, 1, 4, 3],
        'S4': [1, 2, 5, 4],
        'S5': [2, 0, 3, 5],
    },
    'SOLID-HEX': {
        'S1': [0, 1, 2, 3],
        'S2': [4, 5, 6, 7],
        'S3': [0, 1, 4, 5],
        'S4': [1, 2, 5, 6],
        'S5': [2, 3, 6, 7],
        'S6': [0, 3, 4, 7],
    },
    'PSTRESS-QUAD': {
        'S1': [0, 1],
        'S2': [1, 2],
        'S3': [2, 3],
        'S4': [3, 0],
    },
    'PSTRAIN-QUAD': {
        'S1': [0, 1],
        'S2': [1, 2],
        'S3': [2, 3],
        'S4': [3, 0],
    },
    'SHELL-QUAD': {
        'SPOS': [0, 1, 2, 3],
        'SNEG': [0, 1, 2, 3],
        'S3': [0, 1],
        'S4': [1, 2],
        'S5': [2, 3],
        'S6': [3, 0],
    },
}

def _getChunks(itemsToChunk, numOfChunks):
    """Useful function to create lists of lists from list

    Parameters
    ----------
    itemsToChunk : list
        list of objects
    numOfChunks : int
        length of internal list

    Returns
    -------
    list
        list of lists
    """
    temp = [itemsToChunk[i:i + numOfChunks]
            for i in xrange(0, len(itemsToChunk), numOfChunks)]
    return temp
