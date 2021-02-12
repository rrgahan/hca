import pandas as pd


def main():
    df = pd.read_csv('data/LPD_Dispatch_Records_2017.csv')

    counts = df['INC_'].value_counts()
    counts_df = pd.DataFrame({'code': counts.index, 'count': counts.values})

    mapping = pd.read_csv('data/tighter_mapping_2017.csv')
    # merge = mapping.merge(counts_df.drop_duplicates(), on=['code'], how='left', indicator=True)
    # print(merge[merge['_merge'] != 'both'])

    counts_df['category'] = mapping[mapping['code'] == counts_df['code']]['category']

    category_counts = pd.DataFrame({'category': mapping['category'].unique(), 'count': 0})

    for index, row in counts_df.iterrows():
        if row['category'] not in mapping['category'].values:
            print(f'Please add {row["category"]} to the mapping file')
        category_counts.loc[category_counts['category'] == row['category'], 'count'] += row['count']

    category_counts.sort_values(by='count', ascending=False, inplace=True, ignore_index=True)

    category_counts.to_csv('output/2017_tighter_mapped.csv')


if __name__ == '__main__':
    main()
