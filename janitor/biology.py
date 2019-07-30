"""
Biology and bioinformatics-oriented data cleaning functions.
"""

from typing import Union

import pandas as pd

import pandas_flavor as pf

from .utils import deprecated_alias, import_message

try:
    from Bio import SeqIO
except ImportError:
    import_message(
        "biology", "biopython", "conda install -c conda-forge biopython"
    )


@pf.register_dataframe_method
@deprecated_alias(col_name="column_name")
def join_fasta(
    df: pd.DataFrame, filename: str, id_col: str, column_name: str
) -> pd.DataFrame:
    """
    Convenience method to join in a FASTA file as a column.

    This allows us to add the string sequence of a FASTA file as a new column
    of data in the dataframe.

    This method only attaches the string representation of the SeqRecord.Seq
    object from Biopython. Does not attach the full SeqRecord. Alphabet is
    also not stored, under the assumption that the data scientist has domain
    knowledge of what kind of sequence is being read in (nucleotide vs. amino
    acid.)

    This method mutates the original DataFrame.

    For more advanced functions, please use phylopandas.

    Functional usage example:

    .. code-block:: python

        import pandas as pd
        import janitor.biology

        df = pd.DataFrame(...)

        df = janitor.biology.join_fasta(
            df=df,
            filename='fasta_file.fasta',
            id_col='sequence_accession',
            column_name='sequence',
        )

    Method chaining usage example:

    .. code-block:: python

        import pandas as pd
        import janitor.biology

        df = pd.DataFrame(...)

        df = df.join_fasta(
            filename='fasta_file.fasta',
            id_col='sequence_accession',
            column_name='sequence',
        )

    :param df: A pandas DataFrame.
    :param filename: Path to the FASTA file.
    :param id_col: The column in the DataFrame that houses sequence IDs.
    :param column_name: The name of the new column.
    :returns: A pandas DataFrame with new FASTA string sequence column.
    """
    seqrecords = {
        x.id: x.seq.__str__() for x in SeqIO.parse(filename, "fasta")
    }
    seq_col = [seqrecords[i] for i in df[id_col]]
    df[column_name] = seq_col
    return df


@pf.register_dataframe_method
def sequence_features(
    df: pd.DataFrame,
    column_name: str,
    kind: str,
    featurization_type: Union[str, int],
    pad_character="-",
    sequence_length="most_common_only",
):
    """
    Return sequence features as a new pandas DataFrame.


    :param df: The pandas DataFrame
        containing a column of sequences (as strings)
    :param column_name: The column that houses the sequences.
    :param kind: One of (``protein``, ``dna``)
    :param featurization_type: One of
        (``one-hot``, ``pka``, ``mw``, and ``t``)
    :param pad_character: The character to use to pad the sequence.
    :param sequence_length: One of
        (``most_common_only``, ``most_common_max``, ``longest``, or a number).
        ``most_common_only`` keeps only sequences of the most common length.
        ``most_common_max`` keeps sequences up to the most common length,
        and right-pads any sequences of smaller length
        with a dash character.
        ``longest`` keeps all sequences,
        and right-pads any sequence of smaller length
        with a dash character.
        Putting in an integer keeps only sequences of that given length.
    """
    pass
