# Repository instructions

This repository is the owner's public software-testing portfolio for recruiters and technical reviewers.

- Canonical repository: X5t0gods/testing-methods. Reuse this repository for all future versions unless the owner explicitly requests migration.
- Read README.md, MAINTAINING.md and publication.json before publishing an update.
- Use Chinese for primary documentation; write precise, evidence-backed claims with date, scope and limitations.
- Keep historical results separate from newly executed checks. Never claim project-wide 100% coverage from two files, subtract test counts across different snapshots, or invent efficiency and defect metrics.
- Describe AI assistance accurately; do not imply all generated work was independently handwritten.
- Do not upload raw private project files, logs, conversations, databases, credentials, personal paths or contact details. Curate summaries and synthetic examples before the first public commit.
- Preserve Git history. Do not replace existing release tags or create a new repository for every version.
- Run python tools/verify_docs.py and the examples' before/after checks for a release. These checks validate this portfolio, not the private business system.
- Update VERSION, publication.json, README.md, CHANGELOG.md and releases/vX.Y.Z.md together. Create an immutable tag and a GitHub Release after a requested publication.
- Do not modify or test the neighboring business repositories as part of a documentation-only publication.
