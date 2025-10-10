# Releasing

!!! info "Personal Reference"
    Quick reference for future releases

## Quick Release Guide

=== "GitHub Actions (Recommended)"
    1. Go to **GitHub Actions** → **"Create Release"** workflow
    2. Click **"Run workflow"**
    3. Select release type and run

=== "PR Labels"
    1. Add `release:patch/minor/major` label to merged PR
    2. Release triggers automatically

## Release Types

- **`release:patch`** → 1.0.0 → 1.0.1 (bug fixes)
- **`release:minor`** → 1.0.0 → 1.1.0 (new features)
- **`release:major`** → 1.0.0 → 2.0.0 (breaking changes)

## What Happens Automatically

1. **Version calculation** - Bumps version based on release type
2. **Changelog generation** - Uses towncrier to build changelog from fragments
3. **Git operations** - Commits changes and creates version tag
4. **GitHub Release** - Creates release with generated notes
5. **PyPI publishing** - Builds and uploads package automatically
6. **Documentation deployment** - Updates docs site with new version

## Before Releasing

!!! warning "Prerequisites"
    - ✅ All CI checks pass
    - ✅ Changelog fragments exist OR `no-changelog` label added
    - ✅ Main branch is clean

## If Something Goes Wrong

!!! danger "Emergency Response"
    === "Quick Fix"
        - **Yank from PyPI** (prevents new installs)
        - **Add warning** to GitHub release

    === "Major Issues"
        - **Delete release** and git tag
        - **Create hotfix** with patch version
        - **Revert commits** if needed

## Important Files

- **Changelog fragments**: `changelog.d/<number>.<type>.md`
- **Workflow files**: `.github/workflows/release.yml`, `.github/workflows/publish.yml`
- **Nox sessions**: `changelog`, `build`, `docs_deploy`

## Secrets Required

!!! note "GitHub Repository Secrets"
    - `PYPI_API_TOKEN` - For PyPI publishing
    - `PAT_TOKEN` - For GitHub releases (with permission to create release)

## Troubleshooting

!!! tip "Common Issues"
    - **Release failed?** → Check GitHub Actions logs
    - **PyPI upload failed?** → Verify token and version number
    - **Docs not updating?** → Check gh-pages branch
    - **Changelog empty?** → Ensure fragments exist in `changelog.d/`
