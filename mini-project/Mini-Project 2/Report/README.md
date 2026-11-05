# CPE333 Mini-Project 2 Report

This report presents the group’s Virtual Memory project: a Linux tool for inspecting virtual memory and counting process page faults. It explains the design, describes the test method, and discusses results from the merged implementation.

## Project details

- **Course:** CPE333 Operating Systems
- **Project:** Mini-Project 2 — Virtual Memory
- **Group:** มูลนิธิทนายตั้ม ช่วยสู้
- **Instructor:** Asst. Prof. Rajchawit Sarochawikasit
- **Members:** Seven students; names and student IDs appear on the cover.

## Report files

| File | Purpose |
|---|---|
| `CPE333_MiniProject2_Report.docx` | Editable Word or Google Docs version |
| `CPE333_MiniProject2_Report.tex` | LaTeX source |
| `output/pdf/CPE333_MiniProject2_Report.pdf` | Final A4 print and reading copy |
| `assets/` | KMUTT logo and report diagrams |
| `evidence/post-merge-5fbcb76/` | Test logs, environment details, terminal captures, and the latest saved demo transcript |

## Layout and typography

The report follows the visual rhythm of the group’s PS04, PS06, and PS07 lab reports: a centered KMUTT logo and title, generous spacing around the author and course details, bold black Problem/Step headings, green emphasis for key terms, and blue italic captions. Body text uses Sarabun 12 pt, matching the lab reports; Menlo is used for commands and code. The cover lists all seven group members and the instructor.

The print-ready PDF is 19 pages in A4 portrait. Body text is 12 pt Sarabun, with smaller Menlo type for terminal output and code; headings and the cover follow the hierarchy used in PS04, PS06, and PS07. Selected terminal captures, the full demo sample table, and experiment output excerpts sit beside the explanations they support. The appendix contains reproduction commands and pointers to complete raw logs; evidence is not collected into a screenshot-only appendix. The editable DOCX uses the same typography and portrait layout, though Word may paginate it differently. Use the PDF for the intended print layout. Original logs and captures remain in the evidence folders.

## Source and test results

- The report records tests on the merged `beambeambeam/cpe333` source at commit `5fbcb7679298f36e2bae8b7cd3dbe6bf6a609800`.
- Build/load, demo, regression checks, and experiments E1–E8 passed in Lima with Ubuntu 24.04.5, Linux 6.8.0-142-generic, and ARM64.
- The latest demo terminal capture supplies all interval samples, rates, workload checkpoints, and the exit summary in the main text. The report explains why `faultgen`'s cumulative counts differ from `pfstat`'s baseline-adjusted counts. E1–E8 are summarized beside their analysis, with the full E7 timeline and SIGCHLD cleanup output shown inline.
- The build reported a compiler-name mismatch and shared-folder clock skew. BTF generation was skipped because `vmlinux` was unavailable; the module still built and loaded.
- GitHub Actions were not configured for the reviewed branch. Results in the report are from manual runs in Lima.
- The report describes the tested configuration and limitations, including the unmeasured probe overhead, descendant accounting scope, and the permission check that was not rerun after merge.

## Rebuild the PDF

Install XeLaTeX, `latexmk`, Sarabun, and Menlo. From this folder, build into a temporary directory:

```sh
report_build_dir="$(mktemp -d -t cpe333-report)"
latexmk -xelatex -interaction=nonstopmode -halt-on-error \
  -outdir="$report_build_dir" CPE333_MiniProject2_Report.tex
cp "$report_build_dir/CPE333_MiniProject2_Report.pdf" output/pdf/
rm -rf "$report_build_dir"
```

The source uses `fontspec`, `polyglossia`, `geometry`, `graphicx`, `longtable`, `needspace`, `fancyhdr`, `titlesec`, `listings`, `xurl`, and `hyperref`. Shell escape is not required.

## Before submission

Prepare the separate 7–11 minute presentation and implementation demo required by the assignment.
