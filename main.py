# main.py
import sys
import argparse
import json

from parser_conf import parse_config

def main():
    argp = argparse.ArgumentParser(
        description="Учебный конфигурационный язык -> JSON"
    )
    argp.add_argument(
        "-i", "--input",
        required=True,
        help="Путь к входному файлу конфигурации"
    )
    args = argp.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"Ошибка открытия файла: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        data = parse_config(text)
    except SyntaxError:
        sys.exit(1)

    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
