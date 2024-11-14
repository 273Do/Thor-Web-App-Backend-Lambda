from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# OpenAI APIのクライアントを初期化
client = OpenAI()


# 解析結果を用いてChatGPTでフィードバックを生成する


def generate_feedback(estimate_sleep_df, cluster_stats):

    try:
        # ChatGPTによるフィードバック生成
        res = client.chat.completions.create(
            model="gpt-4-turbo",  # gpt-4-turboを使用
            # 出力フォーマットを書いたテキストまたはmdファイルを指定する
            messages=[]
        )

        # フィードバックを取得
        feedback = res.choices[0].message.content
        return True, None, feedback

    except Exception as e:
        return False, str(e), None
