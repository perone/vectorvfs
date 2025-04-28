Using the `vfs` command
===============================================================================
VectorVFS comes with a command-line tool called `vfs` where you can
use to index and search (and index while searching).

`vfs search` command
--------------------------------------------------------------------------------

Let's say that you want to search for images that have cats in a folder,
all you need to do is:

.. code-block:: bash

   $ vfs search cat /my_folder

And it will automatically iterate over all files in the folder, look for
supported files and then embed the file or load existing embeddings directly
from the filesystem.

We are implementing improvements to efficiently detect when files have
changed, but if you want to force VectorFS to re-index you can just use
the flag `-f` for it:

.. code-block:: bash

   $ vfs search -f cat /my_folder

If you want to show only top 3 similar files, you can use:

.. code-block:: bash

   $ vfs search -n 3 cat /my_folder
