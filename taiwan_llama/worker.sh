python -m fastchat.serve.controller --host 0.0.0.0 --port 21001

python3 -m fastchat.serve.model_worker \
    --model-names Llama-3-Taiwan-8B-Instruct \
    --model-path models/models--yentinglin--Llama-3-Taiwan-8B-Instruct/snapshots/f4b968f00a108e40c60347cf9f015cb1978ef665 \
    --worker-address http://localhost:21002 \
    --controller-address http://localhost:21001 \
    --host 0.0.0.0 --num-gpus 2

python3 -m fastchat.serve.openai_api_server --host localhost --port 8000
