#!/bin/bash

# Release Helper Script for VDS Xarray Backend
# This script helps create releases by updating versions and creating tags

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    if ! command_exists git; then
        print_error "Git is required but not installed."
        exit 1
    fi
    
    if ! command_exists uv; then
        print_error "uv is required but not installed. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "This script must be run from within a git repository."
        exit 1
    fi
    
    # Check if we're on main branch
    current_branch=$(git rev-parse --abbrev-ref HEAD)
    if [ "$current_branch" != "main" ] && [ "$current_branch" != "master" ]; then
        print_warning "You're not on the main/master branch. Current branch: $current_branch"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        print_error "You have uncommitted changes. Please commit or stash them first."
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Function to get current version
get_current_version() {
    grep -E '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/'
}

# Function to validate version format
validate_version() {
    local version=$1
    if [[ ! $version =~ ^[0-9]+\.[0-9]+\.[0-9]+([a-zA-Z0-9\-\.]*)?$ ]]; then
        print_error "Invalid version format: $version"
        print_info "Version should follow semantic versioning (e.g., 1.0.0, 1.2.3-beta.1)"
        return 1
    fi
    return 0
}

# Function to update version in files
update_version() {
    local new_version=$1
    
    print_info "Updating version to $new_version..."
    
    # Update pyproject.toml
    sed -i.bak "s/^version = \".*\"/version = \"$new_version\"/" pyproject.toml
    
    # Update __init__.py
    sed -i.bak "s/^__version__ = \".*\"/__version__ = \"$new_version\"/" vdsxarray/__init__.py
    
    # Remove backup files
    rm -f pyproject.toml.bak vdsxarray/__init__.py.bak
    
    print_success "Version updated in all files"
}

# Function to run tests
run_tests() {
    print_info "Running tests..."
    
    uv sync --group test > /dev/null 2>&1
    
    if uv run pytest tests/ -v; then
        print_success "All tests passed"
    else
        print_error "Tests failed. Please fix them before creating a release."
        exit 1
    fi
}

# Function to build package
build_package() {
    print_info "Building package..."
    
    # Install build dependencies
    uv sync --group publish > /dev/null 2>&1
    
    # Clean previous builds
    rm -rf dist/ build/
    
    # Build package
    if uv run python -m build; then
        print_success "Package built successfully"
        
        # Validate package
        if uv run twine check dist/*; then
            print_success "Package validation passed"
        else
            print_error "Package validation failed"
            exit 1
        fi
        
        # Show built files
        print_info "Built files:"
        ls -la dist/
    else
        print_error "Package build failed"
        exit 1
    fi
}

# Function to create and push tag
create_tag() {
    local version=$1
    local tag="v$version"
    
    print_info "Creating and pushing tag $tag..."
    
    # Commit version changes
    git add pyproject.toml vdsxarray/__init__.py
    git commit -m "Bump version to $version"
    
    # Create tag
    git tag -a "$tag" -m "Release $version"
    
    # Push changes and tag
    git push origin HEAD
    git push origin "$tag"
    
    print_success "Tag $tag created and pushed"
}

# Function to show release URL
show_release_info() {
    local version=$1
    local repo_url=$(git config --get remote.origin.url | sed 's/\.git$//')
    
    print_success "Release process initiated!"
    print_info "GitHub Actions will now:"
    print_info "  1. Validate the release"
    print_info "  2. Build the package"
    print_info "  3. Create GitHub release with wheel files"
    print_info "  4. Publish to PyPI (if stable release)"
    echo
    print_info "Monitor the progress at:"
    print_info "  🔗 Actions: $repo_url/actions"
    print_info "  📦 Releases: $repo_url/releases"
    print_info "  🐍 PyPI: https://pypi.org/project/vdsxarray/"
}

# Main release function
main() {
    echo "🚀 VDS Xarray Backend Release Helper"
    echo "===================================="
    echo
    
    check_prerequisites
    
    current_version=$(get_current_version)
    print_info "Current version: $current_version"
    
    echo
    read -p "Enter new version (e.g., 1.0.1): " new_version
    
    if [ -z "$new_version" ]; then
        print_error "Version cannot be empty"
        exit 1
    fi
    
    if ! validate_version "$new_version"; then
        exit 1
    fi
    
    if [ "$new_version" = "$current_version" ]; then
        print_error "New version is the same as current version"
        exit 1
    fi
    
    echo
    print_info "Planned changes:"
    print_info "  Current version: $current_version"
    print_info "  New version: $new_version"
    print_info "  Tag: v$new_version"
    echo
    
    read -p "Proceed with release? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Release cancelled"
        exit 0
    fi
    
    echo
    update_version "$new_version"
    run_tests
    build_package
    
    echo
    read -p "Create tag and push to trigger release? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Version updated but tag not created. You can manually create the tag later:"
        print_info "  git add ."
        print_info "  git commit -m 'Bump version to $new_version'"
        print_info "  git tag -a v$new_version -m 'Release $new_version'"
        print_info "  git push origin HEAD"
        print_info "  git push origin v$new_version"
        exit 0
    fi
    
    create_tag "$new_version"
    show_release_info "$new_version"
}

# Run main function
main "$@"
