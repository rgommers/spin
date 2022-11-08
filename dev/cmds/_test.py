import os
import sys
import click

from .util import run, get_config, set_pythonpath, get_site_packages


@click.command()
@click.option(
    "--build-dir", default="build", help="Build directory; default is `$PWD/build`"
)
@click.argument("pytest_args", nargs=-1)
def test(build_dir, pytest_args):
    """🔧 Run tests

    PYTEST_ARGS are passed through directly to pytest, e.g.:

    ./dev.py test -- -v
    """
    cfg = get_config()

    if not pytest_args:
        pytest_args = (cfg.get("tool.dev.py.package", None),)
        if pytest_args == (None,):
            print(
                "Please specify `package = packagename` under `tool.dev.py` section of `pyproject.toml`"
            )
            sys.exit(1)

    p = site_path = get_site_packages(build_dir)
    set_pythonpath(build_dir)

    print(f'$ export PYTHONPATH="{p}"')
    proc = run(["pytest", f"--rootdir={site_path}"] + list(pytest_args), cwd=p)
    sys.exit(proc.returncode)
