cd /home/user/p_c1_12/Target_Journal_Submission/code
mkdir -p results/logs/regen; cat scripts/jobs_s3.txt | xargs -P 4 -I{} sh -c 'L=results/logs/regen/$(echo "{}" | md5sum | cut -c1-8).log; echo "{}" > $L; python3 {} >> $L 2>&1; echo "EXIT $?" >> $L'
echo ALLDONE > results/logs/regen/ALLDONE
