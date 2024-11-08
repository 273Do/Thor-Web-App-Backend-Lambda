import os
from sklearn.cluster import KMeans

# 歩数のクラスタリングを行う関数


def clustering(df):

    # 歩数カラムのみを抽出
    value_df = df.iloc[:, 3:]

    # クラスタリング
    kmeans_model = KMeans(n_clusters=3, random_state=2).fit(value_df)

    # クラスタリング結果を格納
    labels = kmeans_model.labels_

    # dfにクラスタリング結果を追加
    df["cluster"] = labels

    # 重心を計算
    centroids = kmeans_model.cluster_centers_
    # 部屋：0,家：1,外：2 ここは毎回変わるので統一する必要がある

    # 各クラスタから最大値と最小値を取得し，配列に格納
    cluster_stats = []
    for cluster in df["cluster"].unique():
        cluster_stats.append(
            {
                "cluster": cluster.item(),
                "centroids": centroids[cluster].item(),
                "min": df[df["cluster"] == cluster]["value"].min().item(),
                "max": df[df["cluster"] == cluster]["value"].max().item()
            }
        )

    # csvファイルに出力
    # df.to_csv(f"{os.path.dirname(__file__)}/../test/clu_res.csv", index=False)

    return df, cluster_stats
