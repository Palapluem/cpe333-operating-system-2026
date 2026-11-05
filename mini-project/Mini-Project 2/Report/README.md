# CPE333 Mini-Project 2 Report

This report presents the group’s Virtual Memory project: a Linux tool for inspecting virtual memory and counting process page faults. It explains the design, describes the test method, and discusses results from the merged implementation.

## Project details

- **Course:** CPE333 Operating Systems
- **Project:** Mini-Project 2 — Virtual Memory
- **Group:** มูลนิธิทนายตั้ม ช่วยสู้
- **Instructor:** Asst. Prof. Rajchawit Sarochawikasit
- **Members:** Seven students; names and student IDs appear on the cover.

## Source code

The implementation, Lima helper, experiment runner, and regression tests are maintained in the team repository at the exact revision used for the report: [Mini-Project 2 source at merge commit 5fbcb767](https://github.com/beambeambeam/cpe333/tree/5fbcb7679298f36e2bae8b7cd3dbe6bf6a609800/mini-project-02). The report repository keeps the write-up and reviewed evidence together without duplicating source files from the team repository.

## Report files

| File | Purpose |
|---|---|
| `CPE333_MiniProject2_Report.docx` | Editable Word or Google Docs version |
| `CPE333_MiniProject2_Report.tex` | LaTeX source |
| `output/pdf/CPE333_MiniProject2_Report.pdf` | Final A4 print and reading copy |
| `assets/` | KMUTT logo and report diagrams |
| `evidence/post-merge-5fbcb76/` | Test logs, environment details, eight Terminal-only captures, and the matching run transcripts |

## Layout and typography

The report follows the visual rhythm of PS04, PS06, and PS07: a centered KMUTT logo and title, generous spacing around the author and course details, bold black Problem/Step headings, green emphasis for key terms, and blue italic captions. Body text uses Sarabun 12 pt; Menlo is used for commands and code. The cover lists all seven group members and the instructor.

The print-ready PDF has 21 A4 portrait pages: cover on physical page 1, contents on page 2, report and references on physical pages 3–19 (numbered 1–17), and a two-page appendix on physical pages 20–21. It remains within the assignment's 25-page limit before the appendix. It uses the same Problem/Step hierarchy as the lab reports. Eight genuine, cropped Terminal screenshots appear beside the related discussion, including actual demo, E7 timeline, and SIGCHLD cleanup runs. The `.txt` files retain searchable output from actual runs; they are complete transcripts, not screenshots. The three screenshots for `pfcount run` results now correspond to the same PIDs and values in their transcripts. The appendix gives the full checkout, VM setup, build, live-process inspection, demo, regression, E1–E8 experiment, and cleanup sequence. The editable DOCX uses the same typography and portrait layout; Word or Google Docs may paginate it differently. Use the PDF for the intended print layout.

## Source and test results

- The report records tests on the merged `beambeambeam/cpe333` source at commit `5fbcb7679298f36e2bae8b7cd3dbe6bf6a609800`.
- Build/load, demo, regression checks, and experiments E1–E8 passed in Lima with Ubuntu 24.04.5, Linux 6.8.0-142-generic, and ARM64.
- Eight cropped Terminal screenshots show the required kernel options, module load, the demo, the `pfstat` report, regression checks, the E1–E8 run list, the E7 timeline, and SIGCHLD cleanup. Every `pfcount run` summary shown in the report is now an actual Terminal capture. The `.txt` transcripts retain full output for all recorded runs, including each command, PID, elapsed time, exit status, and measurements. Kernel version and architecture are recorded in the environment log. The demo, E7, and cleanup images match their transcripts by PID and result. The report explains why `faultgen`'s cumulative counts differ from `pfstat`'s baseline-adjusted counts.
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
