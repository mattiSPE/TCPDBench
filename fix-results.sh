#!/bin/bash

# Pfad zum Arbeitsverzeichnis mit den JSON-Dateien
TARGET_DIR="./abed_results/"

# Pfad zum Backup-Wurzelverzeichnis (z. B. ./json_backups)
BACKUP_ROOT="./abed_backups"

# Prüfe, ob Backup-Verzeichnis existiert, sonst anlegen
mkdir -p "$BACKUP_ROOT"

# JSON-Dateien rekursiv durchsuchen
find "$TARGET_DIR" -type f -name "*.json" | while read -r file; do
  # Prüfe JSON-Gültigkeit
  if jq empty "$file" 2>/dev/null; then
    echo "OK: $file"
    continue
  fi

  echo "Invalid JSON: $file – trying to fix..."

  # Relativer Pfad zur Datei vom Wurzelverzeichnis aus
  rel_path="${file#$TARGET_DIR/}"

  # Zielpfad für Backup
  backup_path="$BACKUP_ROOT/$rel_path.backup"

  # Sicherstellen, dass Zielverzeichnis existiert
  mkdir -p "$(dirname "$backup_path")"

  # Backup erstellen
  cp "$file" "$backup_path"

  # Entferne alles vor erstem '{' und schreibe bereinigte Datei zurück
  awk 'found || /{/{found=1} found' "$backup_path" > "$file"

  # Erneut mit jq prüfen
  if jq empty "$file" 2>err.log; then
    echo "✔ Fixed: $file"
    rm -f err.log
  else
    echo "❌ Still invalid after cleanup: $file"
    echo "--- jq error output ---"
    cat err.log
    echo "--- aborting ---"
    exit 1
  fi
done
