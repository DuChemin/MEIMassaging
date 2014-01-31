import sys
sys.path.insert(0, '..')

from arranger import arranger
from incipit import obliterate_incipit, renumber_measures, orig_clefs
from responsibility import responsibility
from longa import longa
from sources import sources_and_editors
from variants import variants
from emendations import emendations
from reconstructions import reconstructions
from ignored import ignored

from constants import *
from utilities import source_name2NCName

import logging
# logging.basicConfig(filename=(MEDIA + 'transform.log'),level=logging.DEBUG)

class TransformData:
	def __init__(self,
			alternates_list=[],
			arranger_to_editor=False,
			obliterate_incipit=False,
			editorial_resp='',
			replace_longa=False,
			color_for_variants=ANYCOLOR,
			color_for_emendations=ANYCOLOR):
		# The alternates_list field contains information about variants,
		# emendations and reconstructions. It is a list of 4-tuples.
		# A basic file with only four staves will look like this:
		#     [('1', VARIANT, '1', ''), ('2', VARIANT, '2', ''),
		#      ('3', VARIANT, '3', ''), ('4', VARIANT, '4', '')]
		# The first element represents the number of the derivative staff
		# under consideration. Other possible values for the middle element
		# are EMENDATION and RECONSTRUCTION. The third element represents
		# the number of the parent staff. The tuple ('5', RECONSTRUCTION, '2', '')
		# can be read as "staff 5 is a reconstruction of staff 2".
		# The last element represents source or responsibility.
		self.alternates_list = alternates_list
		self.arranger_to_editor = arranger_to_editor
		self.obliterate_incipit = obliterate_incipit
		self.replace_longa = replace_longa
		self.editorial_resp = editorial_resp
		self.color_for_variants = color_for_variants
		self.color_for_emendations = color_for_emendations
	
def validate_ncnames(alternates_list):
	res_list = []
	for alternates_item in alternates_list:
		res_item = (alternates_item[0], alternates_item[1], alternates_item[2], source_name2NCName(alternates_item[3]))
		res_list.append(res_item)
	return res_list

def transform(MEI_doc, data=TransformData()):
	logging.info('alternates_list: ' + str(data.alternates_list))
	logging.info('arranger_to_editor: ' + str(data.arranger_to_editor))
	logging.info('obliterate_incipit: ' + str(data.obliterate_incipit))
	logging.info('replace_longa: ' + str(data.replace_longa))
	logging.info('editorial_resp: ' + str(data.editorial_resp))
	logging.info('color_for_variants: ' + str(data.color_for_variants))
	logging.info('color_for_emendations: ' + str(data.color_for_emendations))
	MEI_tree = MEI_doc.getRootElement()
	data.alternates_list = validate_ncnames(data.alternates_list)
	# Measure renumbering needs to be done first!
	if data.obliterate_incipit:
		obliterate_incipit(MEI_tree)
		renumber_measures(MEI_tree)
	if data.arranger_to_editor:
		arranger(MEI_tree)
	if data.replace_longa:
		longa(MEI_tree)
	orig_clefs(MEI_tree, data.alternates_list)
	responsibility(MEI_tree, data.editorial_resp)
	# Only now should we do the tricky stuff.
	sources_and_editors(MEI_tree, data.alternates_list)
	variants(MEI_tree, data.alternates_list, data.color_for_variants)
	emendations(MEI_tree, data.alternates_list, data.color_for_emendations)
	reconstructions(MEI_tree, data.alternates_list)
	ignored(MEI_tree, data.alternates_list)
	# Thing to do: remove ties from removed staves!
	return MEI_doc

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
