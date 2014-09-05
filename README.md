MEIMassaging
============

MEIMassaging is a set of Python files using [libmei](https://github.com/DDMAL/libmei)
which transform ("massage") the raw MEI files that have been created
by [sibmei](https://github.com/DuChemin/sibmei) to make them more suitable for
a particular use—for example, to make them more compatible with
[MEItoVexFlow](https://github.com/ironchicken/MEItoVexFlow).

More specifically: Sibelius files that include variant readings or
reconstructions have these annotations included as extra staves
in the score, and make use of color to mark these variants.
The purpose of the sibmei plugin is to translate those annotations
exactly into their corresponding MEI equivalents. This helps ensure
that MEI may be used for other projects as a generic plugin, and
also avoids writing code for non-straightforward conversion
in ManuScript, the language for Sibelius plugins.

MEIMassaging is expected to handle at least some of the following
transformations which may be necessary after export via sibmei:

 * Adding additional clef information, through the use of `<choice>`.
   If original clefs have been used in the Sibelius file, appropriate
   regularized clefs should be automatically supplied. If the MEI file
   uses regularized clefs, a form should be available to manually supply
   information about original clefs.
 
 * In the Du Chemin repertory, the final note of each part should
   be changed to a longa.
 
 * Emendations
 
 * Variant readings
 
 * Reconstructions
 
 * Responsibility
 
 * Encoding bracketed (and italicized?) lyrics using the `<supplied>` tag
 
 * Changing `<arranger>` to `<editor>`


Usage
=====

To massage a single MEI file, run the `massage_mei.py` script in the `massage`
directory. This script must take the name of the input file as a parameter;
an output filename can be specified by adding `--out new_file_name.mei`
(where you can substitute the output file name for `new_file_name.mei`.)

To switch on or off any of the functions in the MEIMassaging
modules, simply edit the relevant parameters passed to `TransformData`—
or leave them out to use default settings.

To massage an entire directory, you can use the `massage_dir.py` script.
This also can take the `--out` parameter; instead of files, however, input
and output _directories_ are indicated. `--ignore`, `--filter` and `-R`
(for “recursive”) are additional, advanced optional parameters that are
available.

A simpler script, `massage_script.py`, runs massaging of a single file
multiple times on the shell. This is not as powerful as `massage_dir.py`,
but is potentially useful since a single segfault will not cause
massaging of the entire directory to fail.
