from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# OpenAI APIのクライアントを初期化
client = OpenAI()


# 解析結果を用いてChatGPTでフィードバックを生成する


def generate_feedback(estimate_sleep_df, cluster_stats):

    res = client.chat.completions.create(
        model="gpt-4-turbo",
        # 出力フォーマットを書いたテキストまたはmdファイルを指定する
        messages=[]
    )

    # フィードバックを取得
    feedback = res.choices[0].message.content
    print(feedback)
    return feedback


# generate_feedback(None, None)
