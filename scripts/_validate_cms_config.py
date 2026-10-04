# -*- coding: utf-8 -*-
"""Validate admin/config.yml against Decap CMS' config rules (the same rules
that broke the admin: view_filters/view_groups entries, field definitions,
duplicate names, missing files/folders).

Usage:
  python scripts/_validate_cms_config.py           # validate
  python scripts/_validate_cms_config.py --list    # also print the menu tree
"""
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = os.path.join(ROOT, "admin", "config.yml")

WIDGETS = {
    "string", "text", "markdown", "richtext", "number", "boolean", "select",
    "list", "object", "image", "file", "date", "datetime", "hidden",
    "relation", "map", "code", "color", "uuid",
}
errors = []
warnings = []


def err(path, msg):
    errors.append("%s: %s" % (path, msg))


def warn(path, msg):
    warnings.append("%s: %s" % (path, msg))


cfg = yaml.safe_load(open(CFG, encoding="utf-8"))

# --- top level ---
if not isinstance(cfg, dict):
    err("root", "config is not a mapping")
    sys.exit(1)
if not (cfg.get("backend") or {}).get("name"):
    err("backend", "missing name")
if not cfg.get("media_folder"):
    err("media_folder", "missing")
if not cfg.get("collections"):
    err("collections", "missing")

seen_collection_names = set()


def check_fields(fields, where):
    if not isinstance(fields, list) or not fields:
        err(where, "fields must be a non-empty list")
        return
    names = set()
    for i, f in enumerate(fields):
        w = "%s.fields[%d]" % (where, i)
        if not isinstance(f, dict):
            err(w, "field must be a mapping (%r)" % (f,))
            continue
        for req in ("label", "name", "widget"):
            if req not in f:
                err(w, "missing required property '%s'" % req)
        if f.get("name") in names:
            err(w, "duplicate field name '%s'" % f.get("name"))
        names.add(f.get("name"))
        widget = f.get("widget")
        if widget and widget not in WIDGETS:
            err(w, "unknown widget '%s'" % widget)
        if widget == "select" and not f.get("options"):
            err(w, "select widget without options")
        if widget == "list" and not (f.get("field") or f.get("fields")):
            err(w, "list widget without field/fields")
        if widget == "object":
            check_fields(f.get("fields") or [], w)
        if widget == "list" and f.get("fields"):
            check_fields(f["fields"], w)
        # extra properties Decap rejects on simple fields
        allowed = {
            "label", "name", "widget", "required", "default", "hint", "pattern",
            "options", "field", "fields", "types", "media_folder",
            "public_folder", "allow_multiple", "i18n", "collapsed", "summary",
            "min", "max", "step", "value_type", "preview", "comment",
            "multiple", "collection", "display_fields", "search_fields",
            "value_field", "allow_add", "date_format", "time_format",
            "format", "picker_utc", "choose_url", "index_file", "value",
        }
        extra = set(f) - allowed
        if extra:
            warn(w, "unusual field properties: %s" % sorted(extra))


def check_view_filters(filters, where, key):
    if not isinstance(filters, list):
        err(where + "." + key, "must be a list")
        return
    for i, vf in enumerate(filters):
        w = "%s.%s[%d]" % (where, key, i)
        if not isinstance(vf, dict):
            err(w, "must be a mapping, got %r" % (vf,))
            continue
        for req in ("label", "field"):
            if req not in vf:
                err(w, "missing required property '%s'" % req)
        extra = set(vf) - {"label", "field", "pattern"}
        if extra:
            err(w, "must NOT have additional properties %s" % sorted(extra))


for ci, c in enumerate(cfg.get("collections") or []):
    where = "collections[%d]" % ci
    if not isinstance(c, dict):
        err(where, "must be a mapping")
        continue
    name = c.get("name")
    where = "%s(%s)" % (where, name)
    if not name:
        err(where, "missing name")
    elif name in seen_collection_names:
        err(where, "duplicate collection name '%s'" % name)
    else:
        seen_collection_names.add(name)
    if not c.get("label"):
        err(where, "missing label")
    has_files = "files" in c
    has_folder = "folder" in c
    if has_files == has_folder:
        err(where, "must have exactly one of 'files' (file collection) "
                   "or 'folder' (folder collection)")

    if c.get("view_filters") is not None:
        check_view_filters(c.get("view_filters"), where, "view_filters")
    if c.get("view_groups") is not None:
        check_view_filters(c.get("view_groups"), where, "view_groups")

    if has_files:
        seen_files = set()
        for fi, f in enumerate(c["files"] or []):
            w = "%s.files[%d]" % (where, fi)
            for req in ("name", "label", "file", "fields"):
                if req not in f:
                    err(w, "missing required property '%s'" % req)
            if f.get("name") in seen_files:
                err(w, "duplicate file name '%s'" % f.get("name"))
            seen_files.add(f.get("name"))
            check_fields(f.get("fields"), w)
            rel = f.get("file")
            if rel and not os.path.exists(os.path.join(ROOT, rel)):
                err(w, "file does not exist: %s" % rel)
    if has_folder:
        folder = c.get("folder")
        if folder and not os.path.isdir(os.path.join(ROOT, folder)):
            err(where, "folder does not exist: %s" % folder)
        check_fields(c.get("fields"), where)
        if c.get("slug") and str(c["slug"]).endswith(".md"):
            warn(where, "slug should not include the .md extension")

    if c.get("sortable_fields"):
        for sf in c["sortable_fields"]:
            if sf in ("title", "date", "author", "description"):
                continue
            names = {f.get("name") for f in (c.get("fields") or [])}
            if sf not in names:
                warn(where, "sortable field '%s' is not a defined field" % sf)

# --- report ---
print("collections:", len(cfg.get("collections") or []))
if "--list" in sys.argv:
    for c in cfg["collections"]:
        kind = "files" if "files" in c else "folder:" + str(c.get("folder"))
        print("  %-18s %-28s %s" % (c.get("name"), c.get("label"), kind))

print("\nERRORS (%d):" % len(errors))
for e in errors:
    print("  ✗", e)
print("WARNINGS (%d):" % len(warnings))
for w in warnings:
    print("  !", w)
sys.exit(1 if errors else 0)
