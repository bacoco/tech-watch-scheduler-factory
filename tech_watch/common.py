"""Shared bounded IO, validation, and canonical hashes."""
from contextlib import contextmanager
from datetime import datetime
from hashlib import sha256
from pathlib import Path, PurePosixPath
import json
import os
import re
import tempfile

REPO_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+\Z")
SHA_RE = re.compile(r"[0-9a-f]{40}\Z")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def repository(value):
    require(isinstance(value, str) and bool(REPO_RE.fullmatch(value)),
            "repository must be owner/name")
    require(value.split('/')[1] not in {'.', '..'}, "invalid repository name")
    return value


def instant(value):
    require(isinstance(value, str), "timestamp must be an ISO string")
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(result.tzinfo is not None, "timestamp requires a timezone")
    return result


def relative(value):
    require(isinstance(value, str) and value and '\\' not in value,
            "invalid relative path")
    p = PurePosixPath(value)
    require(not p.is_absolute() and all(x not in {'.', '..', ''}
            for x in value.split('/')), "unsafe relative path")
    require(not any(ord(c) < 32 for c in value), "control character in path")
    require(':' not in value, "drive or URL is not a relative path")
    return p


def no_symlinks(path, recursive=False):
    path = Path(path).absolute()
    for p in [path, *path.parents]:
        require(not p.is_symlink(), f"symlink refused: {p}")
    if recursive and path.is_dir():
        for p in path.rglob('*'):
            require(not p.is_symlink(), f"symlink refused: {p}")


def read_json(path):
    p = Path(path)
    no_symlinks(p)
    require(p.stat().st_size <= 2_000_000, f"JSON too large: {p}")
    with p.open(encoding='utf-8') as f:
        return json.load(f)


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def digest(data):
    return sha256(data).hexdigest()


def atomic_json(path, value):
    p = Path(path)
    no_symlinks(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.write-', dir=p.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(json_text(value))
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, p)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextmanager
def lock(directory):
    root = Path(directory)
    no_symlinks(root)
    marker = root / '.factory-lock'
    try:
        marker.mkdir()
    except FileExistsError as exc:
        raise ValueError(f"locked; inspect before recovery: {marker}") from exc
    try:
        yield
    finally:
        marker.rmdir()
