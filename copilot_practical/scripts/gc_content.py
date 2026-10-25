"""Compute GC content for each record in a FASTA file."""

import argparse


def read_fasta_records(path):
    """Yield (header, sequence) pairs from a FASTA file."""
    header = None
    sequence_parts = []

    with open(path, encoding="utf-8") as fasta_file:
        for line_number, line in enumerate(fasta_file, start=1):
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(sequence_parts)
                header = line[1:].strip()
                sequence_parts = []
            else:
                if header is None:
                    raise ValueError(
                        f"sequence data found before FASTA header on line {line_number}"
                    )
                sequence_parts.append("".join(line.split()).upper())

    if header is not None:
        yield header, "".join(sequence_parts)


def gc_content(sequence):
    """Return GC content as a percentage for a DNA sequence."""
    if not sequence:
        return 0.0
    gc_count = sum(base in {"G", "C"} for base in sequence)
    return (gc_count / len(sequence)) * 100


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Print GC content for each record in a FASTA file."
    )
    parser.add_argument("fasta", help="path to a FASTA file")
    parser.add_argument(
        "--min-gc",
        type=float,
        default=None,
        help="only print records above this GC percentage threshold",
    )
    args = parser.parse_args()

    if args.min_gc is not None and not 0 <= args.min_gc <= 100:
        parser.error("--min-gc must be between 0 and 100")

    try:
        records = list(read_fasta_records(args.fasta))
    except OSError as exc:
        parser.error(str(exc))
    except ValueError as exc:
        parser.error(str(exc))

    if not records:
        parser.error("FASTA file contains no records")

    for header, sequence in records:
        if not sequence:
            print(f"{header}: WARNING: empty sequence skipped")
            continue

        gc = gc_content(sequence)
        if args.min_gc is not None and gc <= args.min_gc:
            continue
        print(f"{header}: {gc:.2f}%")
