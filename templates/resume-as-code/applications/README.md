# Tailored applications

One folder per application, `YYYY-MM-company-role/`, containing:
- `job-description.md`
- the tailored `resume.yml` and its PDF/Markdown
- `gap-report.md`

Easiest path: install the ai-toolkit plugin and run `/ai-toolkit:tailor-resume` with the posting. It follows `../RULES.md`. To build by hand:

```bash
python3 resume/build.py applications/<folder>/resume.yml --out applications/<folder> --name <FirstLast>_Resume_<Company>
```

When you submit, tag exactly what you sent: `git tag applied/<folder> && git push origin applied/<folder>`.
