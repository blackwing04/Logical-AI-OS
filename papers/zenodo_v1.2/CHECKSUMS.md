# CHECKSUMS — Zenodo v1.2 deposit files

sha256 and md5 of the **raw bytes** of each file in this directory
(not LF-normalised: these are deposit files and byte-exactness is the point;
`manifest/public_manifest.md` lists the same files LF-normalised, which is
how that table computes every entry).

| File | Bytes | sha256 | md5 |
| --- | --- | --- | --- |
| `report_v1.2.pdf` | 310050 | `5d995b2791fefdf5d9a7680c8a64f71f8430853eec70f308b0892c97c2059ae6` | `7c9acfbfc30a21c27b0d9acbe1a1cd69` |
| `report_v1.2.md` | 41701 | `174c54a482e1d287ac04f37963addaea1a9aef3a27f90d6c1c6c509c8fb464f4` | `3d6ff9ffd4b9dbdfc7eb79ce18e7f651` |
| `abstract_zh.md` | 5177 | `0c12f04d013882c851dd2e5c9787275311a09e355bc5debb8c73fe983cb80ed6` | `746df4ef538d47ec5c118d1b5fff5ddb` |
| `references.bib` | 22915 | `99ee6a7e00bee8750c555e1308350794a21501d29ca16df3a21c401391b89a7d` | `de4d1e38aed8845718857dca20967c8f` |

## What is in the Zenodo deposit, and what is not

**Only `report_v1.2.pdf` is in the deposit at [10.5281/zenodo.23226740](https://doi.org/10.5281/zenodo.23226740).**
That file is **byte-identical** to the published one: the record's own API
reports `md5:7c9acfbfc30a21c27b0d9acbe1a1cd69` and 310050 bytes, which is what the table above gives.

The other three files are **the sources the PDF was built from** — the
Markdown body, the Chinese abstract, and the bibliography. They were not
uploaded to Zenodo, so there is nothing on Zenodo to compare them against.
They are here because a searchable text version of a report is more useful
to a reviewer than a PDF alone. **Said plainly rather than left for a reader
to discover: three of these four files are not part of the deposit.**

The command that produced the PDF from `report_v1.2.md` is recorded in the
project's internal working repository, not here.

## Verify

```bash
sha256sum report_v1.2.pdf report_v1.2.md abstract_zh.md references.bib
# and against the published record:
curl -s https://zenodo.org/api/records/23226740 | grep -o '"checksum":"[^"]*"'
```
