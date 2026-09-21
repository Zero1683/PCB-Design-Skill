"""Shared strict JSON, hashing and closed-file workspace utilities. Python 3.10+."""
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import uuid


def pairs(items):
    out = {}
    for key, value in items:
        if key in out: raise ValueError('Duplicate JSON key: ' + key)
        out[key] = value
    return out


def read(path):
    def bad(value): raise ValueError('Nonfinite JSON number: ' + value)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=pairs, parse_constant=bad)


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(value): return hashlib.sha256(encoded(value)).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''): h.update(block)
    return h.hexdigest()


def text(value, label):
    if not isinstance(value, str) or not value.strip(): raise ValueError('Missing ' + label)
    return value


def finite(value, label):
    if type(value) not in (int, float) or not math.isfinite(value): raise ValueError('Invalid ' + label)
    return value


def no_link(path):
    path = Path(path).absolute()
    for entry in (path, *path.parents):
        if entry.exists() or entry.is_symlink():
            info = entry.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                raise ValueError('Link/reparse path is not allowed: ' + str(entry))
    return path


def inventory(root, allow_empty=False):
    root = no_link(root)
    if not root.is_dir(): raise ValueError('Expected a real project directory')
    out = {}
    def fail(error): raise error
    for parent, dirs, files in os.walk(root, followlinks=False, onerror=fail):
        for name in dirs+files: no_link(Path(parent)/name)
        for name in files:
            path=Path(parent)/name
            if not stat.S_ISREG(path.stat().st_mode): raise ValueError('Nonregular file')
            before=path.stat(); value=file_hash(path); after=path.stat()
            if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):
                raise ValueError('File changed while reading: '+str(path))
            out[path.relative_to(root).as_posix()]={'sha256':value,'bytes':after.st_size}
    if not out and not allow_empty: raise ValueError('Empty project cannot be a recovery checkpoint')
    return dict(sorted(out.items()))


def save(path, data, exclusive=False):
    path=no_link(path)
    payload=encoded(data)+b'\n'
    if exclusive:
        with path.open('xb') as stream: stream.write(payload)
        return
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    try:
        with temp.open('xb') as stream:
            stream.write(payload); stream.flush(); os.fsync(stream.fileno())
        os.replace(temp,path)
    finally:
        if temp.exists(): temp.unlink()
