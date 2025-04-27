<p align="center">
  <img src="docs/source/_static/img/logo_vectorvfs.png" alt="Banner" width="500" />
</p>

# VectorVFS: Your Filesystem as a Vector Database

VectorVFS is a lightweight Python package that transforms your Linux filesystem into a vector database by leveraging the native VFS (Virtual File System) extended attributes. Rather than maintaining a separate index or external database, VectorVFS stores vector embeddings directly alongside each file—turning your existing directory structure into an efficient and semantically searchable embedding store.

VectorVFS currently uses Meta's Perception Encoders (PE) [[arxiv]](https://arxiv.org/abs/2504.13181) which including image/video encoders for vision language understanding, outperforms InternVL3, Qwen2.5VL and SigLIP2 for zero-shot image tasks. More models support coming soon.

## Key Features

- **Zero-overhead indexing**  
  Embeddings are stored as extended attributes (xattrs) on each file, eliminating the need for external index files or services.

- **Seamless retrieval**  
  Perform searches across your filesystem, retrieving files by embedding similarity.

- **Flexible embedding support**  
  Plug in any embedding model—from pre-trained transformers to custom feature extractors—and let VectorVFS handle storage and lookup.

- **Lightweight and portable**  
  Built on native Linux VFS functionality, VectorVFS requires no additional daemons, background processes, or databases.
