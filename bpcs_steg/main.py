#!/usr/bin/env python
"""
BPCS Steganography: encoding/decoding messages hidden in a vessel image

Source: http://web.eece.maine.edu/~eason/steg/SPIE98.pdf

BEHAVIORS:
    encoding
        * expects a vessel image file, message file, and alpha value
        * hides the contents of a file inside a vessel image
    decoding
        * expects a vessel image file, and alpha value
        * recovers the message stored inside a vessel image
    capacity
        * expects a vessel image file and alpha value
        * assesses the maximum size of a message that could be encoded within the vessel image

"""
from bpcs_steg_decode import bpcs_steg_decode
from bpcs_steg_encode import bpcs_steg_encode
from bpcs_steg_capacity import capacity

import os.path
import optparse

__author__ = "Jay Hennig"
__license__ = "BSD"
__email__ = "mobeets@gmail.com"

parser = optparse.OptionParser()

valid_opt_behaviors = ['encode', 'decode', 'capacity']
valid_opt_behaviors = {
    'encode': ['infile', 'messagefile', 'alpha'],
    'decode': ['infile', 'outfile', 'alpha'],
    'capacity': ['infile', 'outfile', 'alpha']
    }

parser.add_option('-i', '--infile', dest='infile', action='store', type='string', help='path to vessel image (.png)')
parser.add_option('-o', '--outfile', dest='outfile', action='store', type='string', help='path to write output file')
parser.add_option('-m', '--messagefile', dest='messagefile', action='store', type='string', help='path to message file')
parser.add_option('-a', '--alpha', dest='alpha', action='store', type='float', help='complexity threshold', default=0.45)
parser.add_option('-b', '--behavior', dest='behavior', action='store', type='string', help='interaction modes: {0}'.format(valid_opt_behaviors.keys()))

(opts, args) = parser.parse_args()

def check_file_exists(filename):
    if not os.path.exists(filename):
        parser.error('The file "{0}" could not be found.'.format(filename))

if not opts.behavior:
    parser.error('-h for help.')
if opts.behavior not in valid_opt_behaviors:
    parser.error('Illegal behavior: {0}. Valid behaviors are {1}'.format(opts.behavior, valid_opt_behaviors.keys()))
mandatory_opts = valid_opt_behaviors[opts.behavior]
if any([m for m in mandatory_opts if not opts.__dict__[m]]):
    parser.error('To {0}, you must specify the following: {1}'.format(opts.behavior, mandatory_opts))

check_file_exists(opts.infile)

if opts.behavior == 'decode':
    bpcs_steg_decode(opts.infile, opts.outfile, opts.alpha)
elif opts.behavior == 'encode':
    check_file_exists(opts.messagefile)
    bpcs_steg_encode(opts.infile, opts.messagefile, opts.outfile, opts.alpha)
elif opts.behavior == 'capacity':
    capacity(opts.infile, opts.outfile, opts.alpha)
