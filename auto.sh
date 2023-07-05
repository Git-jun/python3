#!/bin/bash
source /etc/profile

log_file="/root/log_file_dc.log"  # 替换为您想要存储日志的文件路径

unset GOLOG_LOG_LEVEL

# 函数用于获取带有时间戳的日志行
get_timestamped_log() {
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] $1"
}

dc_total=$(wc -l /tmp/auto-ok.txt | awk '{print $1}' | bc)
echo "$(get_timestamped_log 剩余${dc_total}订单)" >> "$log_file"

#echo "$dc_total"
if ((dc_total < 1)); then
    echo "$(get_timestamped_log  当前订单剩余：${dc_total},没有足够的订单可以导入，请发单后导入)"
    echo "$(get_timestamped_log '没有足够的订单可以导入，请发单后导入')" >> "$log_file"
    exit
fi


#if ((dc_total < 1500)); then
#    echo "$(get_timestamped_log  当前订单剩余：${dc_total},小于1500请发单保证订单充足)"
#fi

Market_Available=$(lotus-miner info | grep -A 2 'Market Balance' | tail -1 | awk '{print $(NF-1)}' | bc)
Worker_Balance=$(lotus-miner info | grep 'Worker Balance:' | awk '{print $(NF-1)}' | bc)

echo "$Market_Available"
echo "$Worker_Balance"

if (( $(awk 'BEGIN {print ('$Market_Available' > 50)}') )); then
    #echo "$(get_timestamped_log 'Market_Available大于50可以放心发单')"
    echo "$(get_timestamped_log 'Market_Available大于50可以放心发单')" >> "$log_file"  # 将日志信息追加到日志文件
    if (( $(awk 'BEGIN {print ('$Worker_Balance' > 500)}') )); then
        echo "$(get_timestamped_log 'Worker_Balance余额大于500准备发单')" >> "$log_file"  # 将日志信息追加到日志文件
        echo "$(get_timestamped_log  当前订单剩余：${dc_total},请发单保证订单充足)" >> "$log_file"
        for i in $(seq 200); do
           head -n1 /tmp/auto-ok.txt | awk -F'|' '{print "boostd import-data   "$1"  /mnt/172.*/car/"$4".car"}' | bash && sed -i '1d' /tmp/auto-ok.txt  
           #head -n1 /tmp/ok4.txt | awk -F'|' '{print "boostd import-data   "$1"  /mnt/172.25.10.*/car/"$4".car"}' | bash && sed -i '1d' /tmp/ok4.txt  
        done  2>&1 >> "$log_file"
        echo "$(get_timestamped_log  当前订单剩余：${dc_total},请发单保证订单充足)"
    else
             echo "$(get_timestamped_log 'Worker_Balance小于1000请确认后发单')"
             echo "$(get_timestamped_log 'Worker_Balance小于1000请确认后发单')"  >> "$log_file"
    fi
    dc_total_tmp=$(wc -l /tmp/auto-ok.txt | awk '{print $1}' | bc)
    echo "$(get_timestamped_log 导入完成后剩余剩余${dc_total_tmp}订单)" >> "$log_file"
else
    echo "$(get_timestamped_log 'Market_Available小于50请确认后发单')"
    echo "$(get_timestamped_log 'Market_Available小于50请确认后发单')" >> "$log_file"  # 将日志信息追加到日志文件
fi
