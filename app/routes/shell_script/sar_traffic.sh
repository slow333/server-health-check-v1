#!/bin/bash

# 출력 파일 초기화 1106 v1.0

IP_ADDRESS=$(hostname -I | awk '{print $1}')
HOSTNAME=$(hostname)

output_file="/tmp/monthly_traffic_summary_$IP_ADDRESS.csv"
# 헤더 추가
echo "hostname,IP,Interface,Date Time,rxpck/s,txpck/s,rxkB/s,txkB/s" > $output_file

# 오늘 날짜 기준 최근 30일
for i in {0..29}; do
  # 날짜 계산-오늘 날짜를 맨 마지막으로 보냄(8일이면, 31로 함)
  day=$(date -d "-$i day" +%d)
  file="/var/log/sa/sa$day"

  # 파일 존재 여부 확인
  if [ -f "$file" ]; then
    # sar 명령어로 네트워크 트래픽 수집
    LC_ALL=C sar -n DEV -f "$file" | grep -vE "IFACE|lo" \
    | awk -v d=$(date -d "-$i day" +%Y-%m-%d) -v ip=$IP_ADDRESS -v h=$(hostname)\
    '{printf "%s,%s,%s,%s %s,%.2f,%.2f,%.2f,%.2f\n", h,ip, $2, d, $1, $3, $4, $5, $6}'\
     >> $output_file
  fi
done
 
# LC_ALL=C sar -n DEV -f /var/log/sa/sa07 | grep -vE "lo" | awk -v d=$(date -d "-0 day" +%Y-%m-%d) '{ printf "%s,%s,%s,%.2f,%.2f,%.2f,%.2f\n", d, $1, $2, $3, $4, $5, $6}'
# LC_ALL=C sar -n DEV -f /var/log/sa/sa07 | grep -vE "lo" | awk -v d=$(date -d "-0 day" +%Y-%m-%d) -v h=$(hostname -I) '{printf "%s,%s,%s %s,%.2f,%.2f,%.2f,%.2f\n", h, $2, d, $1, $3, $4, $5, $6}'
# LC_ALL=C sar -n DEV -f "$file" | grep -vE "IFACE|lo" | awk -v d=$(date -d "-$i day" +%Y-%m-%d) '{
    #   printf "%s,%s,%s,%.2f,%.2f,%.2f,%.2f\n", d:$1, $2, $3, $4, $5, $6
    # }' >> $output_file