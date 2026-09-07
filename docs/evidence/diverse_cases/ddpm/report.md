# DDPM table and rate-distortion plot

Source: Jonathan Ho, Ajay Jain and Pieter Abbeel, Denoising Diffusion Probabilistic Models, NeurIPS 2020. Author-published rate.png supplied a 1024×512 PNG. Only this bitmap was used; no PDF text, coordinates or source chart data were extracted. This case was reconstructed by the parent task, not an independent blind evaluator.

The first scene had a caption frame 0.25 px narrower than the measured advance plus reserve. Expanding only its empty frame by 1 px made build_02 pass. That actual PPTX render still showed mathematical number spacing and subscript differences. A source-based revision used explicit spaces around ±, preserved the bold central value separately, changed mathematical numbers from 19 to 20.25 source pixels, and used separate native loss subscript text. The first prefix frame of that revision overflowed and collided with L; its diagnostics are retained in validation_03.json. A measured frame/label adjustment led to build_04 pass for preflight, native objects and rendered text.

The 66 fixed source ROIs were retained throughout. Maximum absolute edge delta decreased from 29 px to 14 px; median absolute edge delta is 1 px in both measurements. This is not uniform alignment: bold numerical strings, NLL inequalities/parentheses and loss notation still differ visibly. The final loss notation has wider gaps than the source. All 69 text objects remain editable. The curve is traced as 157 native thin rectangles from visible blue pixels, with no inferred data values; it is not a data-linked chart. There are 28 native lines, no image elements, and 254 total objects.

The original and candidate figures were rendered with LibreOffice and inspected at full page. Runtime masks and gradient/polygon additions are not claimed to solve the remaining mathematical typography. The final pass is only automatic gate evidence; PowerPoint/WPS are unverified.

Full figure, PPTX, scene and previews remain local at output/diverse_cases_20260906/ddpm/build_04 because no general redistribution license was established for the author-site figure. Numerical engineering measurements and failure diagnostics are archived here.
