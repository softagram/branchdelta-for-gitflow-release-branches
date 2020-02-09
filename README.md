# branchdelta-for-gitflow-release-branches
Branch delta analytics for Gitflow release branches


e.g.

## Repositories and their release branch groups
| branchdelta-test-repo-1 | branchdelta-test-repo-2|
|  ---  |  ---  |
| PM-{n}.{n} | PP-{n}.{n}.{n} |
| PP-{n}.{n}.{n} |  -  |


## Latest rel branches
| repo | PM-{n}.{n} | PP-{n}.{n}.{n}|
| --- | --- | ---|
branchdelta-test-repo-1 | PM-2020.1 | PP-1.2.0 | 
branchdelta-test-repo-2 | - | PP-2.3.0 <-- PP-2.2.0 | 


## Not in latest rel branch
| repo | PM-{n}.{n} | PP-{n}.{n}.{n}|
| --- | --- | ---|
branchdelta-test-repo-1 |  |  | 
branchdelta-test-repo-2 | - | commit a1c5038a119792b0213de1ad69f3b0b957f23058 FOO-2; commit eb816624f19f9cb43333c2bc2fdb72b02483a0f8 FOO-3 | 

