#!/usr/bin/env bash
# Pull the current upstream playbooks into ../references and show what changed.
# Copies files only; commits nothing. Read the diff before committing.
set -euo pipefail

here="$(cd "$(dirname "$0")/.." && pwd)"
refs="$here/references"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

git clone --depth 1 -q https://github.com/Leonxlnx/taste-skill.git "$tmp/taste"
git clone --depth 1 -q https://github.com/vercel-labs/agent-skills.git "$tmp/vercel"

# upstream folder -> library file name (the skill's own `name:`)
while read -r folder name; do
  cp "$tmp/taste/skills/$folder/SKILL.md" "$refs/$name.md"
done <<'EOF'
taste-skill design-taste-frontend
taste-skill-v1 design-taste-frontend-v1
gpt-tasteskill gpt-taste
soft-skill high-end-visual-design
minimalist-skill minimalist-ui
brutalist-skill industrial-brutalist-ui
redesign-skill redesign-existing-projects
output-skill full-output-enforcement
stitch-skill stitch-design-taste
image-to-code-skill image-to-code
imagegen-frontend-web imagegen-frontend-web
imagegen-frontend-mobile imagegen-frontend-mobile
brandkit brandkit
EOF
cp "$tmp/taste/skills/stitch-skill/DESIGN.md" "$refs/stitch-design-taste.example-DESIGN.md"
cp "$tmp/taste/LICENSE" "$refs/LICENSE.taste-skill"
cp "$tmp/vercel/skills/web-design-guidelines/SKILL.md" "$refs/web-design-guidelines.md"

echo "taste-skill   $(git -C "$tmp/taste" rev-parse --short HEAD) ($(git -C "$tmp/taste" log -1 --format=%cs))"
echo "agent-skills  $(git -C "$tmp/vercel" rev-parse --short HEAD) ($(git -C "$tmp/vercel" log -1 --format=%cs))"

new="$(ls "$tmp/taste/skills" | grep -v -x -E 'llms.txt|taste-skill|taste-skill-v1|gpt-tasteskill|soft-skill|minimalist-skill|brutalist-skill|redesign-skill|output-skill|stitch-skill|image-to-code-skill|imagegen-frontend-web|imagegen-frontend-mobile|brandkit' || true)"
[ -n "$new" ] && echo "new upstream skills, not copied: $new"

echo "--- changed files:"
git -C "$here" status --short -- references || true
