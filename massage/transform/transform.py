import sys
sys.path.insert(0, '..')

from arranger import arranger
from clefs import clefs
from incipit import obliterate_incipit
from incipit import renumber_measures
from longa import longa
from variants import variants
from emendations import emendations
from reconstructions import reconstructions

from constants import *
from pymei import XmlImport, XmlExport

class TransformData:
	def __init__(self,
	             alternates_list=[],
	             arranger_to_editor=False,
	             obliterate_incipit=False,
	             replace_longa=False,
	             orig_clefs=EMPTY_CLEFS):
		# The alternates_list field contains information about variants,
		# emendations and reconstructions. It is a list of 4-tuples.
		# A basic file with only four staves will look like this:
		#     [('1', VARIANT, '1', ''), ('2', VARIANT, '2', ''),
		#      ('3', VARIANT, '3', ''), ('4', VARIANT, '4', '')]
		# The first element represents the number of the derivative staff
		# under consideration. Other possible values for the middle element
		# are EMENDATION and RECONSTRUCTION. The third element represents
		# the number of the parent staff. The tuple ('5', RECONSTRUCTIOn, '2', '')
		# can be read as "staff 5 is a reconstruction of staff 2".
		# The last element represents source or responsibility.
		self.alternates_list = alternates_list
		self.arranger_to_editor = arranger_to_editor
		self.obliterate_incipit = obliterate_incipit
		self.replace_longa = replace_longa
		self.orig_clefs = orig_clefs

def TEST_SET_UP(data):
	"""Mutates data to test specific transformations"""
	data.arranger_to_editor = True
	data.replace_longa = True
	data.obliterate_incipit = True
	data.alternates_list = [('1', 'variant', '1', ''),
	                        ('2', 'variant', '2', ''),
	                        ('3', 'variant', '3', ''),
	                        ('4', 'variant', '4', ''),
	                        ('5', 'reconstruction', '2', 'MJW'),
	                        ('6', 'reconstruction', '4', 'MJW')]

def transform(MEI_doc, data=TransformData()):
	MEI_tree = MEI_doc.getRootElement()
	if True:
		clefs(MEI_tree, data.orig_clefs)
		variants(MEI_tree, data.alternates_list)
		emendations(MEI_tree, data.alternates_list)
		reconstructions(MEI_tree, data.alternates_list)
	if data.arranger_to_editor:
		arranger(MEI_tree)
	if data.obliterate_incipit:
		obliterate_incipit(MEI_tree)
		renumber_measures(MEI_tree)
	if data.replace_longa:
		longa(MEI_tree)
	return MEI_doc

def write_transformation(filename, data=TransformData()):
	old_MEI_doc = XmlImport.documentFromFile(MEDIA + filename)
	new_MEI_doc = transform(old_MEI_doc, data)
	XmlExport.meiDocumentToFile(new_MEI_doc, MEDIA + filename.replace(UPLOADS, PROCESSED))

def test_ui():
	old_filename = raw_input("Filename to transform: ")
	if '.mei' not in old_filename or old_filename[-4:] != '.mei':
		old_filename += '.mei'
	data = TransformData() # Will be filled in
	TEST_SET_UP(data) # For testing purposes
	old_MEI_doc = XmlImport.documentFromFile(old_filename)
	new_MEI_doc = transform(old_MEI_doc, data)
	new_filename = old_filename[:-4] + '_.mei'
	status = XmlExport.meiDocumentToFile(new_MEI_doc, new_filename)
	if status:
		print("Transformed file saved as " + new_filename)
	else:
		print("Transformation failed")

if __name__ == "__main__":
	test_ui()

#                                 ,_-=(!7(7/zs_.
#                              .='  ' .`/,/!(=)Zm.
#                .._,,._..  ,-`- `,\ ` -` -`\\7//WW.
#           ,v=~/.-,-\- -!|V-s.)iT-|s|\-.'   `///mK%.
#         v!`i!-.e]-g`bT/i(/[=.Z/m)K(YNYi..   /-]i44M.
#       v`/,`|v]-DvLcfZ/eV/iDLN\D/ZK@%8W[Z..   `/d!Z8m
#      //,c\(2(X/NYNY8]ZZ/bZd\()/\7WY%WKKW)   -'|(][%4.
#    ,\\i\c(e)WX@WKKZKDKWMZ8(b5/ZK8]Z7%ffVM,   -.Y!bNMi
#    /-iit5N)KWG%%8%%%%W8%ZWM(8YZvD)XN(@.  [   \]!/GXW[
#   / ))G8\NMN%W%%%%%%%%%%8KK@WZKYK*ZG5KMi,-   vi[NZGM[
#  i\!(44Y8K%8%%%**~YZYZ@%%%%%4KWZ/PKN)ZDZ7   c=//WZK%!
# ,\v\YtMZW8W%%f`,`.t/bNZZK%%W%%ZXb*K(K5DZ   -c\\/KM48
# -|c5PbM4DDW%f  v./c\[tMY8W%PMW%D@KW)Gbf   -/(=ZZKM8[
# 2(N8YXWK85@K   -'c|K4/KKK%@  V%@@WD8e~  .//ct)8ZK%8`
# =)b%]Nd)@KM[  !'\cG!iWYK%%|   !M@KZf    -c\))ZDKW%`
# YYKWZGNM4/Pb  '-VscP4]b@W%     'Mf`   -L\///KM(%W!
# !KKW4ZK/W7)Z. '/cttbY)DKW%     -`  .',\v)K(5KW%%f
# 'W)KWKZZg)Z2/,!/L(-DYYb54%  ,,`, -\-/v(((KK5WW%f
#  \M4NDDKZZ(e!/\7vNTtZd)8\Mi!\-,-/i-v((tKNGN%W%%
#  'M8M88(Zd))///((|D\tDY\\KK-`/-i(=)KtNNN@W%%%@%[
#   !8%@KW5KKN4///s(\Pd!ROBY8/=2(/4ZdzKD%K%%%M8@%%
#    '%%%W%dGNtPK(c\/2\[Z(ttNYZ2NZW8W8K%%%%YKM%M%%.
#      *%%W%GW5@/%!e]_tZdY()v)ZXMZW%W%%%*5Y]K%ZK%8[
#       '*%%%%8%8WK\)[/ZmZ/Zi]!/M%%%%@f\ \Y/NNMK%%!
#         'VM%%%%W%WN5Z/Gt5/b)((cV@f`  - |cZbMKW%%|
#            'V*M%%%WZ/ZG\t5((+)L\'-,,/  -)X(NWW%%
#                 `~`MZ/DZGNZG5(((\,    ,t\\Z)KW%@
#                    'M8K%8GN8\5(5///]i!v\K)85W%%f
#                      YWWKKKKWZ8G54X/GGMeK@WM8%@
#                       !M8%8%48WG@KWYbW%WWW%%%@
#                         VM%WKWK%8K%%8WWWW%%%@`
#                           ~*%%%%%%W%%%%%%%@~
#                              ~*MM%%%%%%@f`
