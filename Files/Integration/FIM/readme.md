If u change the frequency to lowest that would'nt give exact result on real time monitoring on next day on log(reccomend dont change). Else set 10 sec monitoring
```xml
<frequency>10<frequency>
```
Monitor Entire C drive
```
<directories check_all="yes" whodata="yes" report_changes="yes">C:</directories>
```
Monitor Limited Directories (for virus total + yara + wazuh)
```
<directories check_all="yes" whodata="yes" report_changes="yes" realtime="yes"></directories>
<directories check_all="yes" whodata="yes" report_changes="yes" realtime="yes"></directories>
<directories check_all="yes" whodata="yes" report_changes="yes" realtime="yes"></directories>
<directories check_all="yes" whodata="yes" report_changes="yes" realtime="yes"></directories>
<directories check_all="yes" whodata="yes" report_changes="yes" realtime="yes"></directories>
<directories check_all="yes" whodata="yes" report_changes="yes" realtime="yes"></directories>
```
```internal_options.conf```

# Maximum number of directories monitored for realtime on windows [1..1024]
syscheck.max_fd_win_rt=1024
