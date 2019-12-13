def is_primary_key(data_frame, key):

    number_of_rows = len(data_frame)

    df = data_frame.loc[:,key]
    df = df.drop_duplicates()
    number_of_unique_rows = len(df)

    return (number_of_rows == number_of_unique_rows)
