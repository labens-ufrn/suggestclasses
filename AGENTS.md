# Guide for Coding Agents

## Local environment

- Use the project virtual environment:

  ```bash
  source .venv/bin/activate
  ```

- Create local configuration from the tracked template and load it before
  running Django commands or data scripts:

  ```bash
  cp .env.example .env
  # Edit the values required by the local environment.
  source .env
  ```

- Do not commit `.env`. It contains local credentials. Keep secrets only in
  local environment files or in CI secrets.
- `DJANGO_SETTINGS_MODULE=suggestclasses.settings` and `PYTHONPATH` are set by
  `.env`; there is no separate `path.env`.

## Database and tests

- The application reads the default database configuration from
  `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_HOST`, and
  `DATABASE_PORT`.
- No custom Django test database name is configured. Django uses
  `test_<DATABASE_NAME>`; for example, `DATABASE_NAME=scdb_dev` uses
  `test_scdb_dev`.
- To let Django create and remove test databases, grant the database role
  `CREATEDB`:

  ```sql
  ALTER ROLE sc_user WITH CREATEDB;
  ```

- On PostgreSQL 15+, ensure the role can create objects in the `public` schema
  of the test database. In this environment, the role also needed `INHERIT`:

  ```sql
  ALTER ROLE sc_user INHERIT;
  ```

- Run tests with:

  ```bash
  python manage.py test --keepdb
  ```

  `--keepdb` preserves the test database between executions.

## CI

- The GitHub Actions workflow copies `.env.example` to `.env` and then replaces
  the database credentials with those of its PostgreSQL service
  (`postgres`/`postgres`).
- Keep `.env.example` free of real credentials and compatible with the
  variables read by `suggestclasses/settings.py`.

## Session changes recorded

- Removed the unused `DATABASE_TEST` variable. It was not read by the Django
  settings, which rely on Django's default test database naming.
- Added `.env.example` at the repository root with placeholders for sensitive
  values.
- Updated the README and CI workflow to use `.env.example`.
- Removed the obsolete `contrib/` directory and all `path.env` documentation.
- Removed the obsolete `contrib/` entry from `CONTRIBUTING.md` and the obsolete
  `path.env` rule from `.gitignore`.
- The test database permission issue was reproduced and resolved locally after
  granting `CREATEDB` and `INHERIT` to the database role.
- The test suite still has one unrelated pre-existing failure:
  `core/tests/test_historico.py` uses removed `assertEquals`; use
  `assertEqual` when addressing that test separately.
