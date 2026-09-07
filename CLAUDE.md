# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Django backend for usriflem1.com — a reference site for the M1 Garand rifle. The core
feature is a serial-number lookup: given a serial number and manufacturer, it identifies
the rifle's production date and the parts (op rod, bolt, bullet guide, trigger group,
stock cartouche, etc.) that were fitted to it based on documented serial-number ranges.
It also serves an education page of embedded videos, exposed to the frontend via a small
DRF API.

## Commands

All Django commands are run from `src/` (that's where `manage.py` lives).

```bash
cd src
python manage.py runserver         # dev server
python manage.py migrate           # apply migrations
python manage.py makemigrations m1 # after changing src/m1/models.py
python manage.py test m1           # run app tests (see note below on m1/tests.py)
python manage.py createsuperuser
```

Dependencies are installed from `requirements.txt` at the repo root (not `src/`).

There is no lint config, formatter config, or CI test stage in this repo — the Bitbucket
pipeline (`bitbucket-pipelines.yml`) only force-pushes `master` to Heroku on push, with no
test/build step.

## Settings and local dev gotcha

`core/settings/__init__.py` tries to import `core/settings/local.py` first and falls back
to `core/settings/production.py` if that import fails (e.g. on Heroku, where `local.py`
doesn't exist). `local.py` is present in this repo for local development.

**`local.py` blocks on `input()` at import time** — every management command (including
`runserver`, `migrate`, `shell`, `test`) will prompt in the terminal:

```
Which DB to connect to? Type "prod" for production.
```

Type anything other than `prod` (e.g. just press enter) to use the local `db.sqlite3`. This
means non-interactive/scripted invocations of `manage.py` will hang waiting on stdin unless
input is piped in, e.g. `echo | python manage.py migrate`.

`production.py` reads `SECRET_KEY` and `DATABASE_URL` from the environment and is what
Heroku uses via the `Procfile` (`gunicorn src.core.wsgi --preload`).

## Architecture

Three Django apps under `src/`:

- **`m1`** — the actual product. Models for every part category (`Receiver`, `OpRod`,
  `Bolt`, `BulletGuide`, `TriggerHousing`, `TriggerGuard`, `Trigger`, `Safety`, `Hammer`,
  `Cartouche`, `Follower`, `Srs`/`SRSVolume`, `Firearm`, `Video`). Nearly every part model
  shares the same shape: `maker` (choices are Springfield Armory / Winchester / IHC / H&R),
  a `drawing_number`, a `[starting_serial, ending_serial]` range, and optional `notes`.
  There's no shared base class for this — it's intentionally repeated per model.
- **`user`** — custom auth user (`AUTH_USER_MODEL = 'user.User'`), extends
  `AbstractUser` with `email` and a `uuid`. Has a `Profile` model.
- **`account`** — thin `Account` model (one-to-one with `User`, plus a `uuid`). Views/tests
  are still stubs.

### The serial-number lookup pipeline

`m1/views.py::index` is the homepage. On POST it validates `RifleDateForm`
(`m1/forms.py`, serial number + maker) and calls `m1/tasks.py::rifle_data(data)`.
`rifle_data` looks up the `Receiver` whose serial range contains the s/n (this gives
month/year of production), then independently queries every other part model
(`get_op_rod`, `get_bolt`, `get_bullet_guide`, `get_cartouche`, `get_trigger_housing`,
`get_trigger_guards`, `get_triggers`, `get_safeties`, `get_hammers`, `get_followers`) via
the same `maker` + serial-range-containment pattern, and assembles one dict describing
every part likely fitted to that rifle. The view then reshapes that dict into
human-readable strings for the template. If no `Receiver` matches, `rifle_data` returns
`{}` and the view re-renders with `error: True`.

When adding a new part category: add a model in `m1/models.py` following the existing
`maker`/`drawing_number`/`starting_serial`/`ending_serial`/`notes` shape, add a
`get_<part>(sn, maker)` lookup function in `m1/tasks.py` mirroring the existing ones, wire
it into `rifle_data`, register it in `m1/admin.py`, and add a line to the `context['rifle']`
dict in `m1/views.py::index`.

### Education/video API

`m1/views.py::education_view` renders `m1/base_education.html` from a fixed dict of named
videos (`tasks.py::get_videos`, keyed by exact video title — adding a video means adding
both a `Video` row and a matching entry in `get_videos`). Separately,
`VideoListView` (DRF `ListAPIView`, `m1/serializers.py::VideoSerializer`) is exposed at
`/api/v1/videos/` for the frontend to consume, ordered by a custom category rank
(military, then maintenance, then production history) and `order` within category.
`Video.Meta` also has its own default `ordering = ['category', 'order']` and a unique
constraint on `(category, order)` — keep both orderings in mind if you touch video sort
logic, since the view's `category_rank` intentionally differs from the model's declared
category order.

## Tests

`m1/tests.py` defines `CustomUnitTests`, a plain class (not a `django.test.TestCase`
subclass) with hand-rolled `assert`/`try`/`except` checks against real fixture data
(hardcoded serial numbers for specific rifles/parts). It is **not** picked up by
`manage.py test` — Django's test runner only discovers `TestCase` subclasses, and nothing
in the repo currently instantiates `CustomUnitTests`. Treat it as executable documentation
of expected serial-number-range behavior rather than a working test suite; if adding real
test coverage for `m1/tasks.py`, prefer wiring these same cases into proper `TestCase`
methods.
