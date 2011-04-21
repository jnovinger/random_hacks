#build_doc.sh

build_doc.sh is a tool a threw together for building Markdown based documents to html or pdf for non-technical consumption. Use as follows:

`./build_docs.sh pdf document.md`

will output a PDF version of 'document.md' to 'document.pdf',

`.build_docs.sh html document.md`

will output an HTML version of 'document.md' to 'document.html'. This last option is really just a shortcut for

`markdown document.md > document.html`.

Cheers!
