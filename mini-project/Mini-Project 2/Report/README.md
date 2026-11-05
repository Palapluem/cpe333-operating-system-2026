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
| `evidence/post-merge-5fbcb76/` | Test logs, environment details, six Terminal-only captures, and the latest saved demo transcript |

## Layout and typography

The report follows the visual rhythm of PS04, PS06, and PS07: a centered KMUTT logo and title, generous spacing around the author and course details, bold black Problem/Step headings, green emphasis for key terms, and blue italic captions. Body text uses Sarabun 12 pt; Menlo is used for commands and code. The cover lists all seven group members and the instructor.

The print-ready PDF is 21 pages in A4 portrait: cover on physical page 1, contents on page 2, report and references on physical pages 3–19 (numbered 1–17), and a two-page appendix on physical pages 20–21. The report stays within the assignment's 25-page limit before the appendix. It uses the same Problem/Step hierarchy as the lab reports. Six genuine, cropped Terminal screenshots appear beside the related discussion. The `.txt` files are full command transcripts saved from actual runs; they are searchable run output, not screenshots. The report uses those transcripts for complete values and keeps screenshots as visual evidence for selected stages. The appendix gives the full checkout, VM setup, build, live-process inspection, demo, regression, E1–E8 experiment, and cleanup sequence. The editable DOCX uses the same typography and portrait layout; Word or Google Docs may paginate it differently. Use the PDF for the intended print layout.

## Source and test results

- The report records tests on the merged `beambeambeam/cpe333` source at commit `5fbcb7679298f36e2bae8b7cd3dbe6bf6a609800`.
- Build/load, demo, regression checks, and experiments E1–E8 passed in Lima with Ubuntu 24.04.5, Linux 6.8.0-142-generic, and ARM64.
- Six cropped Terminal screenshots show the required kernel options, module load, a clearly labeled separate demo run, the `pfstat` report, regression checks, and the E1–E8 run list. They do not depict every individual `pfcount run`. The `.txt` transcripts are the actual complete output from the recorded runs, including each `pfcount run` command, PID, elapsed time, exit status, and measurements. Kernel version and architecture are recorded in the environment log. The report includes the full latest demo samples, rates, workload checkpoints, E1–E8 results, E7 timeline, and SIGCHLD cleanup output beside the related discussion. It explains why `faultgen`'s cumulative counts differ from `pfstat`'s baseline-adjusted counts; the transcript is authoritative when the separate screenshot has different counts.
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
