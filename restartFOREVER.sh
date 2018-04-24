while [ true ]
do
  python3 Parallel-crawler.py &
  PID=$!
  sleep 3600s
  kill $PID
  pkill -f "Parallel-crawler.py"
  echo "starting again"
  echo ""
done
