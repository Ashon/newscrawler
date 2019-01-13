workflow "CI" {
  on = "push"
  resolves = [
    "Build Container",
    "Prepare CI Image",
    "Lint",
    "Unittest",
    "Tag"
  ]
}

action "Build Container" {
  uses = "actions/docker/cli@master"
  args = "build -t newscrawler:ci-$GITHUB_SHA ."
}

action "Prepare CI Image" {
  needs = ["Build Container"]
  uses = "actions/docker/cli@master"
  args = [
    "build", "-f", "Dockerfile.ci",
    "--build-arg", "DEVEL_TAG=ci-$GITHUB_SHA",
    "-t", "newscrawler:dev-$GITHUB_SHA", "."
  ]
}

action "Lint" {
  needs = ["Prepare CI Image"]
  uses = "actions/docker/cli@master"
  args = "run --rm -i newscrawler:dev-$GITHUB_SHA flake8"
}

action "Unittest" {
  needs = ["Prepare CI Image"]
  uses = "actions/docker/cli@master"
  args = "run --rm -i newscrawler:dev-$GITHUB_SHA pytest"
}

action "Tag" {
  needs = ["Lint", "Unittest"]
  uses = "actions/docker/cli@master"
  args = "tag newscrawler:ci-$GITHUB_SHA newscrawler:latest"
}
