"""Convert tagged image colors to sRGB before interpreting their channel values."""

from __future__ import annotations

import hashlib
import io

from PIL import Image, ImageCms, ImageOps

from .scene import InputError


def to_srgb(image, *, preserve_alpha=False):
    image = ImageOps.exif_transpose(image)
    if image.mode in ("P", "PA"):
        image = image.convert("RGBA")
    profile = image.info.get("icc_profile")
    report = {
        "input_mode": image.mode,
        "output_space": "sRGB",
        "profile_sha256": hashlib.sha256(profile).hexdigest() if profile else None,
        "policy": "relative_colorimetric; gamut clipping possible",
        "alpha": "preserved" if preserve_alpha else "composited_on_white",
    }
    alpha = (
        image.convert("RGBA").getchannel("A")
        if image.mode in ("RGBA", "LA", "P", "PA") or "transparency" in image.info
        else None
    )
    if profile:
        if len(profile) > 4_000_000:
            raise InputError("ICC profile exceeds 4 MB")
        try:
            incoming = ImageCms.ImageCmsProfile(io.BytesIO(profile))
            source = (
                image.getchannel("L")
                if image.mode == "LA"
                else image
                if image.mode in ("RGB", "CMYK", "LAB", "L")
                else image.convert("RGB")
            )
            rgb = ImageCms.profileToProfile(
                source,
                incoming,
                ImageCms.createProfile("sRGB"),
                renderingIntent=1,
                outputMode="RGB",
            )
            report["status"] = "converted"
        except (OSError, ValueError, ImageCms.PyCMSError) as exc:
            raise InputError("Embedded ICC profile cannot be converted to sRGB") from exc
    else:
        if image.mode in ("CMYK", "LAB"):
            raise InputError("CMYK/LAB images require an ICC profile for reliable color conversion")
        rgb = image.convert("RGB")
        report["status"] = "assumed_srgb"
    if alpha is not None:
        rgba = rgb.convert("RGBA")
        rgba.putalpha(alpha)
        if preserve_alpha:
            rgb = rgba
        else:
            base = Image.new("RGBA", image.size, "white")
            base.alpha_composite(rgba)
            rgb = base.convert("RGB")
    # Return explicit sRGB channel values, without retaining the input profile on output.
    rgb.info.clear()
    return rgb, report
