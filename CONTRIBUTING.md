# Contributing

Thank you for your interest in Agoras Actions. Contributions are welcome, and credit is given in the project history.

## Types of Contributions

You can help by:

- Reporting bugs
- Fixing bugs
- Implementing features
- Improving documentation
- Submitting feedback on usability or design

## Report Bugs

Report bugs at [https://github.com/LuisAlejandro/agoras-actions/issues](https://github.com/LuisAlejandro/agoras-actions/issues).

Please include:

- Your operating system and version
- The action version or commit you are using
- Steps to reproduce the problem
- Expected and actual behavior
- Relevant workflow logs or error output

## Suggest Features

When proposing a feature, describe:

- The problem you are trying to solve
- The behavior you would like to see
- Alternatives you considered
- How much scope you are willing to take on

## Local Development

1. Fork and clone the repository.
2. Create a branch from `develop`.
3. Build and start the local Docker environment:

   ```bash
   make image
   make start
   ```

4. Copy `.env.example` to `secrets.env` and fill in credentials for the network you want to exercise.
5. Open a shell in the container when needed:

   ```bash
   make console
   ```

The action wraps the [Agoras](https://github.com/LuisAlejandro/agoras) CLI via `docker/execute.py`. See the [Agoras documentation](https://agoras.luisalejandro.org/) for command-line behavior and supported networks.

To build the GitHub Action runtime image locally:

```bash
make docker-image
```

## Quality Checks

Before opening a pull request, run:

```bash
make lint
make format
make test
```

These targets run inside the development container via tox (`lint`, `format` check, and `coverage`).

For integration testing against live credentials, use:

```bash
make functional-test
```

That target runs `test.sh` inside the Docker container. Only run it with test credentials you are comfortable using in a development environment.

CI runs repository checks on pull requests to `develop` and on pushes to `develop` and `master`.

## Pull Request Guidelines

- Keep changes focused on one concern.
- Update documentation when user-facing behavior changes (README, `action.yml` inputs, or workflow examples).
- Link related issues when applicable.
- Note any manual testing you performed, especially for workflow or Docker changes.

## Maintainer Notes

Releases and version bumps are handled by maintainers. Contributors should not publish packages, push release tags, or publish the action to the marketplace without maintainer coordination.

See [MAINTAINER.md](MAINTAINER.md) for the maintainer release process.
