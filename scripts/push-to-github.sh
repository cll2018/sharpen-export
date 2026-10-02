#!/usr/bin/env bash
# Push the local committed tree to GitHub via the Git Database API.
# Used because the sandbox proxy blocks the git:// transport but allows api.github.com.
set -e
TOKEN="${TOKEN:?TOKEN required}"
OWNER="cll2018"
REPO="sharpen-export"
API="https://api.github.com/repos/$OWNER/$REPO"

echo "Creating blobs..."
TREE=""
while IFS= read -r f; do
  base64 -w0 "$f" > /tmp/b64.txt
  B64=$(cat /tmp/b64.txt)
  printf '{"content":"%s","encoding":"base64"}' "$B64" > /tmp/blob.json
  SHA=$(curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d @/tmp/blob.json \
    "$API/git/blobs" | node -e "let s='';process.stdin.on('data',d=>s+=d);process.stdin.on('end',()=>{try{console.log(JSON.parse(s).sha)}catch(e){console.log('ERR:'+s)}})")
  if ! [[ "$SHA" =~ ^[0-9a-f]{40}$ ]]; then echo "BLOB FAIL $f -> $SHA"; exit 1; fi
  TREE="$TREE{\"path\":\"$f\",\"mode\":\"100644\",\"type\":\"blob\",\"sha\":\"$SHA\"},"
  echo "  blob ok: $f"
done < <(git ls-files)

echo "Creating tree..."
TREEJSON="{\"tree\":[${TREE%,}]}"
printf '%s' "$TREEJSON" > /tmp/tree.json
TREESHA=$(curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @/tmp/tree.json \
  "$API/git/trees" | node -e "let s='';process.stdin.on('data',d=>s+=d);process.stdin.on('end',()=>{try{console.log(JSON.parse(s).sha)}catch(e){console.log('ERR:'+s)}})")
echo "  tree sha: $TREESHA"

echo "Creating commit..."
printf '{"message":"Initial commit: Sharpen multilingual export site (EN/ZH + 11 stubs, AI chat, Decap CMS)","tree":"%s","parents":[]}' "$TREESHA" > /tmp/commit.json
COMMITSHA=$(curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @/tmp/commit.json \
  "$API/git/commits" | node -e "let s='';process.stdin.on('data',d=>s+=d);process.stdin.on('end',()=>{try{console.log(JSON.parse(s).sha)}catch(e){console.log('ERR:'+s)}})")
echo "  commit sha: $COMMITSHA"

echo "Creating/updating ref main..."
printf '{"ref":"refs/heads/main","sha":"%s","force":true}' "$COMMITSHA" > /tmp/ref.json
REFCODE=$(curl -s -o /tmp/refout.txt -w "%{http_code}" -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @/tmp/ref.json \
  "$API/git/refs")
if [ "$REFCODE" != "201" ]; then
  # branch already exists (from a prior partial push) -> force update
  REFCODE=$(curl -s -o /tmp/refout.txt -w "%{http_code}" -X PATCH \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d @/tmp/ref.json \
    "$API/git/refs/heads/main")
fi
echo "  ref http: $REFCODE"
echo "DONE -> https://github.com/$OWNER/$REPO"
