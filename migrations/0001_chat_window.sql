-- Chat-specific rate-limit counter for the on-site AI chat widget.
-- Apply once: wrangler d1 execute <db> --file=./migrations/0001_chat_window.sql
-- (or run the CREATE TABLE in the Cloudflare D1 console).
-- The function fails open if this table is missing, so deployment is safe
-- even before the migration is applied; the 19/min cap only engages after.
CREATE TABLE IF NOT EXISTS chat_window (
  window_start INTEGER PRIMARY KEY,
  used INTEGER NOT NULL DEFAULT 0
);
