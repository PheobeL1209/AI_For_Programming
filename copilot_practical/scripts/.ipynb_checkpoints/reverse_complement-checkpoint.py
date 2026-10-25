# reverse_complement.py
# Reads a single-record DNA sequence from a FASTA file and prints its
# reverse complement.

import argparse

COMPLEMENT = {
    "A": "T",
    "T": "A",
    "C": "G",
    "G": "C",
    "U": "A",
    "R": "Y",
    "Y": "R",
    "S": "S",
    "W": "W",
    "K": "M",
    "M": "K",
    "B": "V",
    "V": "B",
    "D": "H",
    "H": "D",
    "N": "N",
}


def read_fasta_sequence(path):
    """Return the sequence from a single-record FASTA file."""
    sequence_lines = []
    has_header = False

    with open(path, encoding="utf-8") as fasta_file:
        for line_number, line in enumerate(fasta_file, start=1):
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if has_header:
                    raise ValueError("expected a single-record FASTA file")
                has_header = True
            else:
                if not has_header:
                    raise ValueError(
                        f"sequence data found before FASTA header on line {line_number}"
                    )
                sequence_lines.append("".join(line.split()).upper())

    if not has_header:
        raise ValueError("FASTA file is missing a header")

    sequence = "".join(sequence_lines)
    if not sequence:
        raise ValueError("FASTA file contains no sequence")
    return sequence


def reverse_complement(seq):
    """Return the reverse complement of a DNA sequence."""
    if not isinstance(seq, str):
        raise TypeError("sequence must be a string")

    sequence = seq.upper()
    if not sequence:
        raise ValueError("sequence must not be empty")

    invalid_bases = sorted(set(sequence) - set(COMPLEMENT))
    if invalid_bases:
        raise ValueError(
            f"sequence contains unsupported base(s): {''.join(invalid_bases)}"
        )
    translation = str.maketrans(COMPLEMENT)
    return sequence.translate(translation)[::-1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Print the reverse complement of a single-record DNA FASTA file."
    )
    parser.add_argument("fasta", help="path to a FASTA file")
    args = parser.parse_args()

    try:
        print(reverse_complement(read_fasta_sequence(args.fasta)))
    except (OSError, ValueError) as error:
        parser.error(str(error))
