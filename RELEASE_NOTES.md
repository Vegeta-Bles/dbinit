# Release Notes Template

Use this template when creating a new release.

## Version X.Y.Z - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Deprecated
- Features that will be removed in future versions

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security improvements

---

## Quick Release Checklist

- [ ] Update version numbers in:
  - [ ] `setup.py`
  - [ ] `dbinit/__init__.py`
  - [ ] `dbinit/cli.py`
- [ ] Update `CHANGELOG.md`
- [ ] Run tests (if applicable)
- [ ] Build package: `./scripts/build-and-publish.sh`
- [ ] Commit changes
- [ ] Create git tag: `git tag -a vX.Y.Z -m "Release X.Y.Z"`
- [ ] Push to GitHub: `git push origin master && git push origin vX.Y.Z`
- [ ] Publish to PyPI: `./scripts/build-and-publish.sh --publish`
- [ ] Create GitHub release (optional)
