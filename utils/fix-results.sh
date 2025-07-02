#!/bin/bash

# Feste Definition: Wurzel für die Verzeichnisstruktur
TARGET_DIR="./abed_results"

# Backup-Verzeichnis (außerhalb TARGET_DIR!)
BACKUP_ROOT="./abed_backups"

# Optional: Startverzeichnis für die Suche (innerhalb TARGET_DIR)
START_DIR="$TARGET_DIR"

# Falls ein Pfad übergeben wurde, setze START_DIR entsprechend
if [[ -n "$1" ]]; then
  START_DIR="$1"
fi

# Sicherstellen, dass BACKUP_ROOT existiert
mkdir -p "$BACKUP_ROOT"

# Alle *.json-Dateien im gewünschten Teilbaum suchen
find "$START_DIR" -type f -name "*.json" | while read -r file; do
  # Prüfung mit jq
  if jq empty "$file" 2>/dev/null; then
    echo "OK: $file"
    continue
  fi

  echo "Invalid JSON: $file – trying to fix..."

  # Relativer Pfad zum TARGET_DIR (nicht START_DIR!)
  rel_path="${file#$TARGET_DIR/}"

  # Zielpfad für Backup
  backup_path="$BACKUP_ROOT/$rel_path.backup"

  # Verzeichnisstruktur erzeugen
  mkdir -p "$(dirname "$backup_path")"

  # Backup anlegen
  cp "$file" "$backup_path"

  # Datei ab erster { bereinigen
  awk 'found || /{/{found=1} found' "$backup_path" > "$file"

  # Erneute Prüfung mit jq
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
