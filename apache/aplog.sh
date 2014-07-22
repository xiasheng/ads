

#!/bin/sh 
# analyze apache access log

num=20
filename=""

interfaces="/user/init/ \
            /channels/ \
            /score/ \
            /top/score/ \
            /score/records/ \
            /exchange/records/ \
           "
           


if [ $# -lt 1 ] ; then 
   echo "usage: " $0 "filename [num]"
   exit 0
elif [ $# -lt 2 ] ; then 
   filename=$1
else
  filename=$1
  num=$2
fi 

echo "----------Top"  $num "Access IP" "----------"
cat $filename | awk '{print $1}' | sort | uniq -c | sort -nr | head -$num

echo ""
echo "----------Interface Statistic----------"

for i in $interfaces
do
c=`grep $i $filename | wc -l`
printf "%7d %s\n" $c $i
done

