# syntax=docker/dockerfile:1

# Raw restricted data/ is mounted at runtime; never baked into this image.

# Stage 1: fetch the uv binary (tooling only — the app env comes from uv.lock).
FROM ghcr.io/astral-sh/uv:0.13.6 AS uv

# Stage 2: runtime image.
FROM python:3.12-slim

# uv-managed environment lives outside the workspace so /workspace can be
# bind-mounted at runtime without shadowing the pinned dependencies.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv

# Install the uv binary (project pins required-version >= 0.11.28 in pyproject.toml).
COPY --from=uv /uv /uvx /bin/

# Non-root user and a workspace it owns.
ARG UID=1000
RUN groupadd --gid "${UID}" app \
    && useradd --uid "${UID}" --gid "${UID}" --create-home --shell /bin/bash app
WORKDIR /workspace
RUN chown app:app /workspace

# Layer 1: project metadata only, so dependency resolution is cached
# independently of source changes.
COPY --chown=app:app pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Layer 2: install the project itself (editable, uv's default for `uv sync`).
COPY --chown=app:app README.md LICENSE ./
COPY --chown=app:app src ./src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENV PATH="/opt/venv/bin:${PATH}"

USER app
