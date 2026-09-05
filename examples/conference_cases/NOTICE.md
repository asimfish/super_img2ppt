# Paper figure provenance and reuse

The runtime is independently implemented. These test figures and their reconstructions have
separate provenance and terms; they are excluded from the distributable `.skill` package.
Authors of the papers do not endorse this project or the fidelity of these reconstructions.

## ViT — ICLR 2021

Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai,
Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly,
Jakob Uszkoreit and Neil Houlsby, *An Image is Worth 16x16 Words: Transformers for Image
Recognition at Scale*. [Official ICLR record](https://iclr.cc/virtual/2021/oral/3458).

Input: `vit_figure.png` from the authors' `google-research/vision_transformer` repository,
commit `64801f1b3b367b3611cc27a3d45cc22870a36fb3`, blob
`9e217d6683ef06e75dd89efc429b0f952b3a103e`.
[Image](https://github.com/google-research/vision_transformer/blob/64801f1b3b367b3611cc27a3d45cc22870a36fb3/vit_figure.png)
and [repository license](https://github.com/google-research/vision_transformer/blob/64801f1b3b367b3611cc27a3d45cc22870a36fb3/LICENSE).
The Apache-2.0 license is reproduced at [licenses/APACHE_2_0.txt](licenses/APACHE_2_0.txt).
No paper text, model code, model weights or fonts were imported. The arXiv paper's different
distribution notice was not used as permission for the author-repository image.

Changes by super_img2ppt contributors, 2026-09-06: independently reconstructed text, shapes,
connectors and arrowheads from this bitmap; retained ten separate photo crops; approximated
rounded path joins and source fonts; generated PPTX/SVG, actual-render comparisons and metrics.
The supplied source reference remains unaltered; reconstructed files are modified derivatives.

## Spatial-Mamba — ICLR 2025

Chaodong Xiao, Minghan Li, Zhengqiang Zhang, Deyu Meng and Lei Zhang,
*Spatial-Mamba: Effective Visual State Space Models via Structure-Aware State Fusion*.
[Official proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/b7216f4a324864e1f592c18de4d83d10-Abstract-Conference.html),
[paper and CC BY 4.0 record](https://openreview.net/forum?id=iDe1mtxqK5),
[CC BY 4.0 terms](https://creativecommons.org/licenses/by/4.0/).

Input: Figure 4 on PDF page 5, rasterized at scale 4 and cropped to
`[424,310,2024,934]` in raster pixel coordinates. The official PDF SHA-256 is
`fa857a65ea4ec31023bd922e1eb622a4e412bbe7d3792d070f6aaca18307cdc7`.

Changes by super_img2ppt contributors, 2026-09-06: cropped the figure from a rendered page;
reconstructed all 39 text elements (15 rotated) as native editable text, and reconstructed
shapes/lines/shadows from pixels; retained the single photo; approximated shadows and rounded
dash corners; generated editable files and comparison evidence. These derivatives retain
attribution under CC BY 4.0. No PDF text coordinates or original vectors were used as answers.

## MobileViT — local test only

Sachin Mehta and Mohammad Rastegari, *MobileViT: Light-weight, General-purpose, and
Mobile-friendly Vision Transformer*, ICLR 2022.
[Author's conference record](https://machinelearning.apple.com/updates/apple-at-iclr-2022),
[paper](https://arxiv.org/abs/2110.02178).

Figure 1 was independently tested locally. The downloaded arXiv v2 paper has the arXiv
non-exclusive distribution license, which we did not interpret as a general redistribution
grant. Source images and derived PPTX/SVG/scene files for this case are therefore not included
here. The repository includes engineering findings and the fixed-source local fetch recipe.
The author's software repository license was not extended to the separately hosted paper.
