import pandas as pd
import tempfile


def pandas_to_arff(df):
    """
    Convert a Pandas DataFrame into a temporary ARFF file.
    Returns the temporary ARFF file path.
    """

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".arff",
        mode="w",
        encoding="utf-8"
    )

    temp.write("@RELATION dataset\n\n")

    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):
            temp.write(f"@ATTRIBUTE {col} NUMERIC\n")

        else:

            values = sorted(df[col].astype(str).unique())

            values = ",".join(values)

            temp.write(
                f"@ATTRIBUTE {col} {{{values}}}\n"
            )

    temp.write("\n@DATA\n")

    for _, row in df.iterrows():

        line = ",".join(row.astype(str))

        temp.write(line + "\n")

    temp.close()

    return temp.name