import base64

import seaborn as sns
import numpy as np
import pandas as pd
from io import BytesIO

import matplotlib.pyplot as plt


class PlotsGenerator:

    def __init__(self, labels_dict_path):
        with open(labels_dict_path) as f:
            self.classes = [line.split(':')[0] for line in f.readlines()]

    def generate_plot(self, data_list, duration):
        columns = [data['label'] for data in data_list]
        df = pd.DataFrame(np.NaN, index=np.arange(0, duration, 1), columns=columns)
        for idx, data in enumerate(data_list):
            label = data.get('label', None)
            if label not in self.classes:
                raise Exception(f'Invalid class label {label}')
            ranges = data.get('ranges', None)
            for points_range in ranges:
                df[label] = df.index.to_series().apply(
                    lambda x: idx + 1 if points_range['start'] <= x <= points_range['end'] else df.loc[x, label])

        sns.set_theme()
        sns.set_context("poster")
        p = df.plot(kind='line', ylim=[0, len(columns) + 1], xlim=[0, duration], colormap='tab20c', style=['-'] * len(df.columns), legend=False, linewidth=6, figsize=(12, 6))
        p.set_yticks(range(1, (len(columns) + 1)))
        p.set_yticklabels(columns, rotation=15, fontdict={'fontsize': 16})
        p.set_xticklabels(np.arange(0, 31, 5), fontdict={'fontsize': 12})
        p.set_title('Objects occurences', fontdict={'fontsize': 36}, pad=20)
        p.set_xlabel('media time [s]', fontdict={'fontsize': 18})
        plt.tight_layout()
        buf = BytesIO()
        p.figure.savefig(buf, format="png")
        return base64.b64encode(buf.getbuffer())