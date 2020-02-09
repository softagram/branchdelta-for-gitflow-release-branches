import os
import re
import sys


def get_forgotten_commits(r, branch1, branch2):
    commits = []
    with os.popen(f'git -C {r} cherry {branch1} {branch2}') as p1:
        for line in p1:
            if line.strip().startswith('+'):
                commit = line.lstrip('+ ').strip()
                with os.popen(f'git -C {r} rev-list --format=%B --max-count=1 {commit}') as p2:
                    commit = p2.read().replace('\n', ' ').strip()
                    commits.append(commit)
    return '; '.join(commits)


def branchdelta(outfile, rel_branch_prefix):
    rel_branch_replace_nums = re.compile('[0-9]+')

    repos = {}
    for r in os.listdir('.'):
        if os.path.isdir(r) and os.path.exists(r + '/.git'):
            # TODO HACKED AWAY os.system(f'echo {r} && git -C {r} fetch')
            branches = []
            with os.popen(f'git -C {r} branch -r') as f:
                for line in f:
                    branches.append(line.strip())
            release_branches = list(filter(lambda x: x.startswith(rel_branch_prefix + '/'),
                                           branches))
            release_branches.sort(reverse=True)

            rel_branch_groups = {}
            for rel_branch in release_branches:
                rel_branch_group = rel_branch_replace_nums.sub('{n}', rel_branch)
                rel_branch_groups.setdefault(rel_branch_group, []).append(rel_branch)

            for k, v in rel_branch_groups.items():
                repos.setdefault(r, {})[k] = v

    repos_tuples = []
    for k, v in repos.items():
        repos_tuples.append((k, len(v), v))

    repos_tuples.sort(key=lambda x: x[1], reverse=True)

    repos = []
    repos_by_branch_group = {}
    for k, lv, v in repos_tuples:
        repos.append(k)
        for branch_group, branches in v.items():
            repos_by_branch_group.setdefault(branch_group, {})[k] = branches

    print(repos_tuples)

    def print_out(s, out_lines):
        out_lines.append(s + '\n')

    out_lines = []
    print_out('## Repositories and their release branch groups', out_lines)
    print_out('| ' + ' | '.join(repos) + '|', out_lines)
    print_out('| ' + ' | '.join(map(lambda x: ' --- ', repos)) + ' |', out_lines)

    rows = []
    for i in range(0, 100):
        found = False
        row = []
        for repo, lv, v in repos_tuples:
            branch_groups = list(sorted(v.keys()))
            if len(branch_groups) > i:
                found = True
                row.append(branch_groups[i])
            else:
                row.append(' - ')
        if not found:
            break
        rows.append(row)

    for row in rows:
        print_out('| ' + ' | '.join(row) + ' |', out_lines)

    branch_groups = []
    for branch_group, v in repos_by_branch_group.items():
        branch_groups.append(branch_group)

    branch_groups.sort()

    print_out('\n\n## Latest rel branches\n| repo | ' + ' | '.join(branch_groups) + '|', out_lines)
    print_out('| --- | ' + ' | '.join(map(lambda x: '---', branch_groups)) + '|', out_lines)
    for r in repos:
        row = '' + r
        for bg in branch_groups:
            if bg in repos_by_branch_group:
                v = repos_by_branch_group[bg]
                if r in v:
                    if len(v[r]) > 1:
                        row += ' | ' + v[r][0] + ' <-- ' + v[r][1]
                    elif len(v[r]) == 1:
                        row += ' | ' + v[r][0]
                    elif len(v[r]) == 0:
                        row += ' | ? '
                else:
                    row += ' | -'
        row += ' | \n'
        out_lines.append(row)

    print_out('\n\n## Not in latest rel branch\n| repo | ' + ' | '.join(branch_groups) + '|',
              out_lines)
    print_out('| --- | ' + ' | '.join(map(lambda x: '---', branch_groups)) + '|', out_lines)

    for r in repos:
        row = '' + r
        for bg in branch_groups:
            if bg in repos_by_branch_group:
                v = repos_by_branch_group[bg]
                if r in v:
                    if len(v[r]) > 1:
                        commits_list = get_forgotten_commits(r, v[r][0], v[r][1])
                        row += ' | ' + commits_list
                    else:
                        row += ' | '
                else:
                    row += ' | -'
        row += ' | '
        print_out(row, out_lines)

    with open(outfile, 'w') as f:
        for o in out_lines:
            f.write(o.replace(rel_branch_prefix + '/', ''))


def main():
    rel_branch_prefix = 'origin/release'
    branchdelta(sys.argv[1], rel_branch_prefix)  # output file path


if __name__ == '__main__':
    main()
