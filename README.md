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
 
