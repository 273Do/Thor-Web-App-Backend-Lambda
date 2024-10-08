# chmod +x start_containers.sh

# envファイルを読み込む
source ./.env
project_pass_list=($FRONTEND_PASS $BACKEND_PASS)

# 引数を受け取る
operation="$1"

# コンテナの起動/終了
for pass in ${project_pass_list[@]}; do
    cd $pass
    if [ $operation = "up" ]; then
        docker compose up -d
    elif [ $operation = "down" ]; then
        docker compose down
    else
        echo "引数が不正です．"
        break
    fi

done
