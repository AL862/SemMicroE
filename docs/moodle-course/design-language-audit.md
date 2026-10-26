# Audit: Moodle seminars and interactive tests

Baseline: cb60ab3f334334f6c2838c9135c997b87470a8a4. Date: 2026-10-26.

## Applied guidance

- UI UX Pro Max, revision28b3b8dee8c976df4fa3e94aed4e092ad43fcb03: hierarchy, readable navigation, visible focus, generous touch targets and contrast. The initial broad education search suggested a children's interface and was rejected. The narrower university/academic search supplied useful Swiss-style hierarchy guidance; portfolio layout and serif/font suggestions were not adopted. The established Arial/navy course system remains authoritative.
- Academic Research Skills: evidence-anchored editorial checks and sufficient assumptions. No claim of independent peer review or calibrated scoring.
- Scientific Skills: distinguish local approximations from finite changes, preserve assumptions and check units. LanguageTool is a language aid rather than an economic validator.
- Course skills: original exercises and review statements retain their numbers, questions and keys. Student pages contain no book attribution.

## Changes

1. All11introductions now explain the student's decision in clear everyday language. Four objective statements were rephrased to avoid chains of abbreviations.
2. Introduction and objectives use common compact components. The table of contents uses separate numbered links with short labels. The lower previous/all/next links are consistent navigation cards. Unknown URLs remain disabled; edit `tools/moodle-course/navigation.json` and rebuild to insert a confirmed address.
3. Twenty-three explanatory answers were rewritten. Main clarifications: demand versus quantity demanded, conditions of equilibrium comparisons, tax prices, local versus arc elasticity, total revenue and accounting cost recognition. Source questions and assessment keys are preserved.
4. Spaced symbols such as `Q d` are typeset as real subscripts. Whitespace normalization is restricted to unambiguous quantity/utility/product symbols so a Romanian phrase such as `P a crescut` is not misread as an index.
5. All275interactive questions were reconsidered for a single correct answer and adequate wording. Two adapted stems were improved: S2№18 stands alone rather than referring to previous functions; S9№5 explicitly states positive quantity for MR below P. Options, keys and timing are unchanged. Only the corresponding two MBZ/XML pairs need new bytes; all other archives retain the already repaired Moodle header.

## Validation

- All11pages: Chromium at320/390/768/1150px, open answers and notation tables, working range controls and no JS errors or whole-page horizontal overflow.
- Additional navigation tests: keyboard focus, minimum hit area, no empty hrefs and no href on unknown links.
- Romanian LanguageTool6.6 CLI on all11seminar texts. All11test sets have language reports; changed sets2and9were checked again. Mathematical names and symbols are reviewed as dictionary false positives.
- 59exact checks of selected seminar computations and81exact checks of numerical test keys pass.
- All11backups pass Moodle's literal XML-header detection algorithm, archive-index and ID-link checks. All275keys agree between XML and MBZ. Adjacent correct letters differ and each answer position occurs6–7times in each test.
- No authenticated Moodle editor or restore session was available. Browser rendering and format detection do not constitute an actual server restore.

## Pedagogical comparison for the next stage

[Mankiw's Teaching the Principles of Economics](https://mankiw.scholars.harvard.edu/publications/teaching-principles-economics) and his [StLouis Fed teaching interview](https://www.stlouisfed.org/education/teach-economics-podcast-series/introducing-economics-to-students-keep-things-simple-greg-mankiw) support prioritizing a small set of clear foundational ideas. [University of Michigan CRLT guidance](https://crlt.umich.edu/tech-tools/presentation-technology) discusses cognitive overload from dense slides and recommends legible visuals and active processing. These are pedagogical references, not empirical proof of this course's learning effectiveness. Their application here is a short seminar opening, one coherent example and a quick comprehension check; not a second full lecture.
