Monitor Entire C drive
```
<directories check_all="yes" whodata="yes" report_changes="yes">C:</directories>
```
Monitor Limited Directories (for virus total + yara + Fim)
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
