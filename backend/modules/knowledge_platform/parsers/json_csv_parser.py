"""JSON and CSV parsers — flattens structured data to readable text."""
import csv
import json
import io
from .base_parser import BaseParser


class JsonCsvParser(BaseParser):
    @property
    def supported_extensions(self) -> list[str]:
        return [".json", ".csv", ".tsv"]

    def parse(self, file_bytes: bytes, filename: str = "") -> str:
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        try:
            if ext == "json":
                return self._parse_json(file_bytes)
            elif ext in ("csv", "tsv"):
                delimiter = "\t" if ext == "tsv" else ","
                return self._parse_csv(file_bytes, delimiter)
            else:
                # Try JSON first, then CSV
                try:
                    return self._parse_json(file_bytes)
                except Exception:
                    return self._parse_csv(file_bytes, ",")
        except Exception as e:
            raise ValueError(f"JSON/CSV parse failed for '{filename}': {e}") from e

    def _parse_json(self, file_bytes: bytes) -> str:
        data = json.loads(file_bytes.decode("utf-8"))
        return json.dumps(data, indent=2, ensure_ascii=False)

    def _parse_csv(self, file_bytes: bytes, delimiter: str) -> str:
        text = file_bytes.decode("utf-8", errors="replace")
        reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
        lines = []
        for row in reader:
            lines.append(" | ".join(f"{k}: {v}" for k, v in row.items() if v))
        return "\n".join(lines)
