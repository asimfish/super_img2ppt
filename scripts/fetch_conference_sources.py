"""Fetch hash-pinned public paper and chart images for local reconstruction experiments."""

import argparse
import hashlib
from contextlib import closing
from pathlib import Path
from urllib.request import urlopen

import pypdfium2 as pdfium
from super_img2ppt.prepare import fresh_directory, json_write

SOURCES = {
    "teaser_lora": {
        "url": "https://raw.githubusercontent.com/asimfish/super_teaser/6b1d41b0b81ed09ed5cd692182ae05fc5573ac12/examples/images/lora-clean.png",
        "sha256": "19afb88cb69b32f27290eb30e9097091997a2fab8cbe8846becb6987cdc6079a",
        "format": "png",
        "source": "super_teaser AI-generated conceptual LoRA illustration, not an original paper figure",
    },
    "teaser_routing": {
        "url": "https://raw.githubusercontent.com/asimfish/super_teaser/6b1d41b0b81ed09ed5cd692182ae05fc5573ac12/examples/images/fixtures/fixture-routed-branches.png",
        "sha256": "dbb4273914d4fa86e82b63b7053ede38f5f40890f0e90891f4f009e7c283831b",
        "format": "png",
        "source": "super_teaser AI-generated synthetic routed-branches fixture, not measured research data",
    },
    "teaser_embodied": {
        "url": "https://raw.githubusercontent.com/asimfish/super_teaser/6b1d41b0b81ed09ed5cd692182ae05fc5573ac12/examples/images/embodied/pi05-hierarchy-v3.png",
        "sha256": "830083551c6d6bd3db1553f1fff0a3e33e7bbded09f931851ca74263c357ae06",
        "format": "png",
        "source": "super_teaser AI-generated pi0.5 conceptual illustration, not original experimental photographs or a paper figure",
    },
    "heatmap": {
        "url": "https://matplotlib.org/3.11.1/_images/sphx_glr_image_annotated_heatmap_002.png",
        "sha256": "7d07f73d16e3dafb7f74fbbac2b8aa2739e29e39e5e430bf918d811606baacd8",
        "alternate_sha256": ["38bbe92c47b0ee9f99fd5619a261e7fc26bd523df43f080e2b1454db4292e7ba"],
        "variant_note": "Both observed PNG responses decode to identical RGB pixels; one omits Software and DPI metadata.",
        "format": "png",
        "source": "Matplotlib 3.11.1 documentation, not a conference paper",
    },
    "clip": {
        "url": "https://raw.githubusercontent.com/openai/CLIP/d05afc436d78f1c48dc0dbf8e5980a9d471f35f6/CLIP.png",
        "sha256": "308a3ca4503f1c7a07803916c369d78c4ef501e5ab7fc727da9b5e1d2f9ec85b",
        "format": "png",
        "venue": "ICML 2021",
    },
    "swin": {
        "url": "https://raw.githubusercontent.com/microsoft/Swin-Transformer/f82860bfb5225915aca09c3227159ee9e1df874d/figures/teaser.png",
        "sha256": "4edbd1fbd66972804cf11d66c6224f24b54209a2ec4607ac36ab9a7c1e18dfa2",
        "format": "png",
        "venue": "ICCV 2021",
    },
    "ddpm_rate": {
        "url": "https://hojonathanho.github.io/diffusion/assets/img/rate.png",
        "sha256": "2eada145639eb6df706dfd401477fd3ad2955066eeb52a926ec7911a84305c20",
        "format": "png",
        "venue": "NeurIPS 2020",
    },
    "vit": {
        "url": "https://raw.githubusercontent.com/google-research/vision_transformer/64801f1b3b367b3611cc27a3d45cc22870a36fb3/vit_figure.png",
        "sha256": "4614d5404f0feb77c6d1dfc6b9db00969acf08387f3ec886f9fd06bb81d51b26",
        "format": "png",
        "venue": "ICLR 2021",
    },
    "mobilevit": {
        "url": "https://arxiv.org/pdf/2110.02178",
        "sha256": "f0257b993891fcc8ebfd17bfe29c949cc5be97af7ae2cbc7fb899165c7533281",
        "format": "pdf",
        "page": 2,
        "crop_at_scale_4": [420, 312, 2020, 1256],
        "venue": "ICLR 2022",
    },
    "spatial_mamba": {
        "url": "https://proceedings.iclr.cc/paper_files/paper/2025/file/b7216f4a324864e1f592c18de4d83d10-Paper-Conference.pdf",
        "sha256": "fa857a65ea4ec31023bd922e1eb622a4e412bbe7d3792d070f6aaca18307cdc7",
        "format": "pdf",
        "page": 5,
        "crop_at_scale_4": [424, 310, 2024, 934],
        "venue": "ICLR 2025",
    },
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cases", nargs="+", choices=list(SOURCES), default=list(SOURCES))
    args = parser.parse_args()
    fresh_directory(args.out)
    report = {"cases": []}
    for name in args.cases:
        spec = SOURCES[name]
        path = args.out / f"{name}.{spec['format']}"
        digest, size = hashlib.sha256(), 0
        try:
            with urlopen(spec["url"], timeout=45) as response, path.open("xb") as target:
                while block := response.read(65536):
                    size += len(block)
                    if size > 25_000_000:
                        raise ValueError("Source exceeds the 25 MB download limit")
                    target.write(block)
                    digest.update(block)
            if digest.hexdigest() not in {spec["sha256"], *spec.get("alternate_sha256", [])}:
                raise ValueError("Source hash changed; review the upstream revision before reuse")
            if spec["format"] == "pdf":
                with (
                    pdfium.PdfDocument(path) as document,
                    closing(document[spec["page"] - 1]) as page,
                ):
                    bitmap = page.render(scale=4)
                    try:
                        bitmap.to_pil().crop(spec["crop_at_scale_4"]).save(args.out / f"{name}.png")
                    finally:
                        bitmap.close()
            record = {
                "id": name,
                "status": "verified",
                "bytes": size,
                "download_sha256": digest.hexdigest(),
                **spec,
            }
        except (OSError, ValueError, RuntimeError) as exc:
            record = {"id": name, "status": "fail", "error": str(exc), **spec}
        report["cases"].append(record)
        json_write(args.out / "sources.json", report)
        print(f"{name}: {record['status']}", flush=True)
    return 0 if all(c["status"] == "verified" for c in report["cases"]) else 2


if __name__ == "__main__":
    raise SystemExit(main())
