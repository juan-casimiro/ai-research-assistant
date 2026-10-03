# Selected research corpus

This directory contains the 55 unique selected articles for the corpus rebuild:
54 licensed CC BY 4.0 and one CC0 1.0. Original publisher PDFs and their existing
UTF-8 extracted text are copied without changes. Text extraction uses pypdf in
physical page order; PDF layout and figures are not reproduced in plain text.
Preserve supplied notices and credits when redistributing either format.

| Folder | Articles | Selection and attribution |
| --- | --- | --- |
| `cardiology-v1/` | 21 | [Manifest](../../benchmark/cardiology/v1/manifest.json), [attribution](cardiology-v1/ATTRIBUTION.md) |
| `diabetes-v1/` | 11 additional | [Manifest](../../benchmark/diabetes/v1/manifest.json), [attribution](diabetes-v1/ATTRIBUTION.md) |
| `oncology-v1/` | 14 | [Manifest](../../benchmark/oncology/v1/manifest.json), [attribution](oncology-v1/ATTRIBUTION.md) |
| `outliers-v1/` | 5 | [Manifest](../../benchmark/outliers/v1/manifest.json), [attribution](outliers-v1/ATTRIBUTION.md) |
| `als-ftd-v1/` | 4 | [Manifest](../../benchmark/als-ftd/v1/manifest.json), [attribution](als-ftd-v1/ATTRIBUTION.md) |

The diabetes selection includes the 21 cardiology articles. Those shared files
are stored once in `cardiology-v1/`; its attribution inventory therefore also
lists articles in that folder. The original topic folder names and article
basenames are preserved. Downloaded candidates and historical restricted-license
articles outside the current selections are not included.

[inventory.json](inventory.json) maps every PDF/text pair to article identity,
licence, benchmark manifest membership and SHA-256 checksums. The benchmark
manifests retain the detailed version, source, extraction and third-party review
evidence. Article terms apply independently of any repository code licence:
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).

The bundled files do not change benchmark membership, document hashes or recorded
results. Existing ingestion commands still use the separate topic directories
specified by their benchmark instructions. This directory remains excluded from
the Docker build context by `.dockerignore`.
