source ~/.secrets/monitoring.sh
pip3 install -r python/requirements.txt
nohup python3 python/main.py python/default_config.json
