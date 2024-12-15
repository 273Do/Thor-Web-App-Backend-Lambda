import sys
import numpy as np
from sklearn.cluster import KMeans


# # 歩数のクラスタリングを行う関数


def clustering(df):
    # 歩数カラムのみを抽出
    value_df = df.iloc[:, 3:]

    # クラスタリング
    kmeans_model = KMeans(n_clusters=3, random_state=2).fit(value_df)

    # クラスタリング結果を格納
    labels = kmeans_model.labels_

    # dfにクラスタリング結果を追加
    df["cluster"] = labels

    # セントロイドを取得
    centroids = kmeans_model.cluster_centers_

    # セントロイドの値が小さい順に並び替えたインデックスを取得
    sorted_indices = np.argsort(centroids.flatten())
    print(sorted_indices)

    # クラスタ番号を再マッピングする辞書を作成
    remap_clusters = {old: new for new, old in enumerate(sorted_indices)}
    print(remap_clusters)
    # 再マッピングされたクラスタ番号をデータフレームに適用
    df["cluster"] = df["cluster"].map(remap_clusters)

    # 各クラスタから最大値と最小値を取得し，配列に格納
    cluster_stats = []
    for cluster in sorted_indices:
        cluster_stats.append(
            {
                "cluster": remap_clusters[cluster],
                "centroids": round(centroids[cluster].item(), 2),
                "min": df[df["cluster"] == remap_clusters[cluster]]["value"].min().item(),
                "max": df[df["cluster"] == remap_clusters[cluster]]["value"].max().item()
            }
        )

    # csvファイルに出力
    # df.to_csv(f"{os.path.dirname(__file__)}/../test/clu_res.csv", index=False)

    return df, cluster_stats
