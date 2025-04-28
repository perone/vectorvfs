.. vectorvfs documentation master file, created by
   sphinx-quickstart on Fri Apr 25 09:47:33 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. image:: _static/img/logo_vectorvfs.png
   :width: 400
   :align: center
   :alt: Banner

VectorVFS: Your Filesystem as a Vector Database
================================================

VectorVFS is a lightweight Python package that transforms your Linux filesystem into a vector database by
leveraging the native VFS (Virtual File System) extended attributes. Rather than maintaining a separate
index or external database, VectorVFS stores vector embeddings directly alongside each file—turning your
existing directory structure into an efficient and semantically searchable embedding store.

VectorVFS supports Meta's Perception Encoders (PE) `[arxiv] <https://arxiv.org/abs/2504.13181>`_ which
includes image/video encoders for vision language understanding, it outperforms InternVL3, Qwen2.5VL
and SigLIP2 for zero-shot image tasks. We support both CPU and GPU but if you have a large
collection of images it might take a while in the first time to embed all items if you are
not using a GPU.

.. note:: This is the first release of VectorVFS and we are expanding models and data types.
          Currently we support only Perception Encoders (PE) and images.


Key Features
------------
- **Zero-overhead indexing**  
  Embeddings are stored as extended attributes (xattrs) on each file, eliminating the need for external
  index files or services.
- **Seamless retrieval**  
  Perform searches across your filesystem, retrieving files by embedding similarity.
- **Flexible embedding support**  
  Plug in any embedding model—from pre-trained transformers to custom feature extractors—and let
  VectorVFS handle storage and lookup.
- **Lightweight and portable**  
  Built on native Linux VFS functionality, VectorVFS requires no additional daemons, background
  processes or databases.

.. toctree::
   :maxdepth: 4
   :caption: Contents

   installation
   architecture
   usage

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`