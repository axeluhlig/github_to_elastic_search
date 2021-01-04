# WIP - not yet usable

# Know what's going on in your teams
Use powerful analytics tools like Kibana or Grafana to monitor KPIs that matter. 
- Cycle time
- Number of P1 bugs over time
- "Active" headcount: Number of individual contributers over time
- Number of new and deleted SLOC (lines of code) over time 
- ...

This tool regularly uploads all needed data to an elasticsearch database, which can then serve as data source for your analytic tools. 

## WIP notes

### Next steps
1. Fix tests on Github (green locally)
1. Specify the max number of commits to be pushed at once (-> risk of running out of ram)
1. Test on bigger repos
1. Implement global for loop ? 
### General Steps
1. Write "push all missing commits to ELS"
1. Write "push all missing issues to ELS"
1. Write "push all missing PRs to ELS"
1. Write "push all missing issues to ELS"
1. Write "push number of current issues per tag to ELS" (or "push all current open issues)

### How to avoid duplicate entries in ELS 
Only an issue for metrics which are derived from Github's plain json data (e.g. have all commits in ELS). 

Easy Solution: Do this in a loop. Save current time at beginng of loop. Don't push any entries (e.g. commits, PRs, issues) which are older than this timestamp. 

Harder Solution: Check which data is already present in ELS and upload missing one. 
Advantage: 
- You can start to analyze a lot of data right away

Disadvantage:
- What if you can't affor to keep all the data? -> Can be solved by defining max age for all entries

## Use cases (and how to get there)
### Number of open issues per tag
Usage examples: 
- How many P1 bug tickets per week over time?
- Are P4 tickets tackled at all?

How: monitor over time, easistes with PyGithub. Theoretical this could be done by using the timeline of an issue, but then the development over time is hard to get right in ELS.

### Names of commit authors
Usage examples: 
- How many unique developers have contributed in the last 7 days over time?
- How long do the currently active developers already contribute to the project (over time)? -> How is the experience developing over time?  

How: Save plain json about commits in ELS and use Kibana to do the rest. 
