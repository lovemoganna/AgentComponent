# MetaLoop Work paired evaluation — 2026-11-20

**Disposition: NO_PROMOTION. Four native model responses were observed. No Candidate advantage was established on either matched case.** Technical solutions tie on the executed oracle and blind inspection. The nontechnical responses are identical, with one shared source-attribution failure. Exact Python 3.11 runtime, exact model build, cost, and an independent human acceptance remain unverified.

| Case | Stable | Candidate | Paired finding |
|---|---|---|---|
| Technical stencil placement | Own self-test passed, 8/8 frozen cases passed, 3.11 grammar check passed | Own self-test passed, 8/8 frozen cases passed, 3.11 grammar check passed | Tie on frozen gates. The runtime was CPython 3.13.5. Python 3.11 runtime is NOT_RUN. |
| Nontechnical community notice | 4/4 factual lines accepted and all structural checks passed. Return-line attribution failed. | Byte-identical captured answer and same findings. | Tie. Both cite C on the return line. The explicit date also needs B under the frozen rubric. |

## Preregistration and scope

- Source commit `011694de28436fc11cc1aa68ff916aa7579dff06`. Stable [prompt](../../../prompts/meta-prompt/execute/execute-evidence-based-loop.md) Git Blob `188953441f5c54fdb81c7883ad05aa0e15a277fa`. Candidate [prompt](../../../prompts/meta-prompt/execute/orchestrate-metaloop.md) Git Blob `e87076047facb3a88ad95a6322f06a4cd478b0cc`. Both identities were recomputed from downloaded bytes using `git hash-object`. PR evidence parent at start was `9f18232dd45f109246f46b747de68d4851e970a6`.
- A separate Work model session (`fork_turns: none`) selected new technical and nontechnical tasks and authored their acceptance standards without the tested prompts or prior conversation. The coordinator serialized its rubric and sealed exact task/rubric bytes before starting the four runs. Freeze time `2026-11-20T09:41:23.279445+00:00` UTC. This uses authored synthetic, shareable source records instead of the example public-document probes in the original protocol. The nontechnical primary records are reproduced in the task text.
- Overlap screen covered 17 artifacts: seven MetaLoop-related main commit diffs (`011694de`, `b7534f35`, `cca5a691`, `327f4b81`, `b9f2c82c`, `d5684f6a`, `738d5ba9`), the PR diff, the two old PR comments, six pinned development files (MetaLoop README, regression and observation fixtures, engine/layer/lifecycle tests), and the prior readiness record. Six sentinels (`place_stencils`, `stencil cannot straddle`, `松桥社区中心`, `二楼手作室`, `积木套件`, `现场不补登记`) each returned zero hits. The cases introduce a different task and source corpus from the known development examples. Scoped repository holdout only. Private history, evaluator training, and complete semantic-history overlap remain unverified.
- Shared single-task capability only. Candidate-only L1/L2/L3 orchestration remains outside these two pairs. One sample per domain and one generation per arm support no broad quality or cost inference.

## Execution conditions and trace

Four fresh Work subagent contexts used `fork_turns: none`, no model or reasoning override, one model task answer per context, the same setup instructions, and no user-directed external model API or CLI call. The Task and arm prompt were supplied in an opaque assigned file with identical delimiters. Each run was asked to perform one setup read (`sha256sum <packet> && cat <packet>`) and send the observed hash and process exit status. No task execution tools were permitted in either pair. Shell and collaboration capabilities were available by platform default, and the task-tool restriction was instructed rather than enforced by an agent capability allowlist. The sessions shared a host filesystem and only their own packet path was supplied. No output from one agent or rubric was supplied to an answer generator. Setup attestations all matched the sealed hashes and reported no other task-tool calls. Full hidden platform instructions, exact backend model build, sampling settings, exact per-arm token budget, hidden tool trace and transport bytes are unavailable. This limits the comparison to the observed matched Work setup.

The coordinator randomized arm order separately for each task before invocation. Candidate was drawn first in both pairs. The actual launch order and hashes follow. The output hashes cover the UTF-8 text captured from the native agent final-answer payloads with no added final LF.

| Order | Case | Arm | Session | Packet SHA-256 | Captured output SHA-256 |
|---|---|---|---|---|---|
| 1 | technical | Candidate | `runner_41` | `bc5629e369ade153e02860fc14b6125f5312646344ef06dbe86a2535c688fd68` | `23580f55a435137c9c6fbd0173abe850d48c1d4e036082890a5195d50e3a6921` |
| 2 | technical | Stable | `runner_73` | `c33f97627dbcadf86ce1774ddee5f66a43583ec98684b0b83b4c329dabeda462` | `c385c8e55f46bdb42e32eeeebdfb60c3082b5e53091d7f7605ccbf117ad8e2c1` |
| 3 | nontechnical | Candidate | `runner_28` | `4189ad0119b9b37b7752329aa13525ae4dc8f03b0de3df35bc61b2a0312d23ec` | `30af0c0428ff8e242cf2bea5f03ff1e9bb8f2c01850c35f7d690bb0f4d578a60` |
| 4 | nontechnical | Stable | `runner_56` | `89f247eeb77a825c386e96a5ffe92c4bf911103c82298af31f1596cf60474571` | `30af0c0428ff8e242cf2bea5f03ff1e9bb8f2c01850c35f7d690bb0f4d578a60` |

Captured arm answers by `2026-11-20T09:42:53.271040+00:00` UTC. About 90.0 seconds elapsed between the freeze record and collection, including orchestration and capture. This is not per-arm model latency. Each run had one observed setup read attestation and one observed trace message. Exact model latency, tokens, and cost are `NOT_AVAILABLE` for all arms and the judge. The separate local verification batch took 0.308 seconds as reported by its shell execution tool.

### Setup attestations

- `runner_41`: bc5629e369ade153e02860fc14b6125f5312646344ef06dbe86a2535c688fd68; setup shell exit code 0; no other task tools ran
- `runner_73`: SHA-256 c33f97627dbcadf86ce1774ddee5f66a43583ec98684b0b83b4c329dabeda462, setup shell exit code 0, no other task tools ran.
- `runner_28`: 4189ad0119b9b37b7752329aa13525ae4dc8f03b0de3df35bc61b2a0312d23ec 0 否
- `runner_56`: 89f247eeb77a825c386e96a5ffe92c4bf911103c82298af31f1596cf60474571；0；无

### Independent review

The review session started at `fork_turns: none` with the frozen task inputs and rubrics, and independently shuffled response IDs. It received no arm labels or prompt text. On review copies only, the leading status labels in the two technical responses were replaced with `[label withheld]` to suppress a provenance cue. Status wording about execution was preserved. The sealed reviewer packet hash and matching returned hash were `45f8a3fb707ec5c2b1f3981367304ef16b00d5f899038877a4fc302b8d68da62`. The unedited captured responses are in the appendix. The evaluator was a separate model context, not an external human approver. The coordinator retained the mapping and decoded it after the review. `T-K` = Stable, `T-R` = Candidate, `N-F` = Candidate, `N-M` = Stable.

For both notices the return line has 53 code points. Appending `[B]` without editing makes it 56 and fails the 55-code-point limit. The defect concerns the trace from the stated date back to source B, while source C supplies the deadline relative to distribution day, location, and return procedure. Both versions showed the same behavior.

### Deterministic execution

Two separate Bubblewrap processes ran only the extracted technical response code, the frozen oracle and the checker. They had read-only system and case mounts, no workspace mount, an ephemeral /tmp, resource limits and a seccomp filter denying socket creation and io_uring setup. The first network-namespace probe was denied by the host. The replacement seccomp restriction denied an actual socket attempt. The initial environment test was tightened to account for two synthesized variables (`PWD` and `LC_CTYPE`), then passed as shown below. The environment's offline installed interpreters were 3.12.14 and 3.13.5. Python 3.11 was absent. Parsing with `ast.parse(feature_version=(3, 11))` is a syntax screen only. There is no Python 3.11 runtime result.

```text
CPython 3.13.5: no inherited environment variables (PWD and LC_CTYPE synthesized), workspace unmounted, socket denied
runner_28: four prefixes and lengths PASS [42, 27, 11, 53]; sources [['B'], ['B'], ['C'], ['C']]
runner_56: four prefixes and lengths PASS [42, 27, 11, 53]; sources [['B'], ['B'], ['C'], ['C']]
runner_41
Python 3.11 grammar check: PASS
CPython 3.13.5: submitted self-test exited normally (6 static assert statements)
case 1: PASS ([2, None, 5, None], '.#####', 0)
case 2: PASS ([3, 0, 2], '#####', 3)
case 3: PASS ([0], '##...', 2)
case 4: PASS ([None, 1, None], '.##.', 3)
case 5: PASS ([None, None], '', 0)
case 6: PASS ([], '#.#', 2)
case 7: PASS ([None], '#.#', 0)
case 8: PASS ([0, None], '#', 0)
frozen oracle: 8/8 PASS
sandbox_exit=0
runner_73
Python 3.11 grammar check: PASS
CPython 3.13.5: submitted self-test exited normally (5 static assert statements)
case 1: PASS ([2, None, 5, None], '.#####', 0)
case 2: PASS ([3, 0, 2], '#####', 3)
case 3: PASS ([0], '##...', 2)
case 4: PASS ([None, 1, None], '.##.', 3)
case 5: PASS ([None, None], '', 0)
case 6: PASS ([], '#.#', 2)
case 7: PASS ([None], '#.#', 0)
case 8: PASS ([0, None], '#', 0)
frozen oracle: 8/8 PASS
sandbox_exit=0
```

## Frozen task and acceptance artifacts

For the four blocks immediately below, the hashed bytes are UTF-8 without the Markdown fence or its final separator LF. The rubric JSON is serialized on one line. To reconstruct each arm packet, prepend `--- FROZEN PROMPT AS INSTRUCTIONS ---\n` to the exact frozen prompt blob, then append `\n--- USER TASK ---\n` and the exact task bytes without further additions.

### Technical task

SHA-256 `1e2e78d9a1d7f7c66d9413971659c3115a355e2a1e38f44f9f0a9e61ec0b8f10`

```text
Implement `place_stencils(strip: str, cursor: int, widths: list[int]) -> tuple[list[int | None], str, int]` in Python 3.11. Use only the standard library.

The strip is a single row of cells. `.` means available and `#` means unavailable. Indices start at zero. For each width, in input order, scan candidate start indices from the current cursor to the end, then from zero up to but excluding the cursor. Choose the first candidate whose full run of that width fits inside the row and consists entirely of available cells. The scan wraps, but a placed stencil cannot straddle the end of the row. Record the chosen start index, mark its cells `#`, and set the cursor to the cell after the stencil, wrapping to zero if the stencil ends at the last cell. If nothing fits, record `None` and leave the strip and cursor as they were for that request. Return the recorded starts, final strip, and final cursor. Do not modify `widths`.

Assume all inputs satisfy the contract. A strip contains only `.` and `#`, `widths` may be empty and contains only positive integers, and a nonempty strip has a valid cursor. The empty strip always receives cursor zero, and every placement on it fails.

Return exactly one fenced `python` block containing the function and a runnable assertion-based self-test. Follow it with one `Status:` line and one `Evidence:` line. On the evidence line, name two boundary scenarios your self-test covers and give their expected results. The environment provides no code execution tools for this response, so report the self-test as included and unrun.
```

### Technical rubric

SHA-256 `3606e8c3877edfd96c5d7768d82923eaafea3567c833362a7fd973a74064c986`

```json
{"grading":"Apply hidden assertions to the submitted function under Python 3.11. Grade executable behavior independently from response format and evidence quality. A claimed execution is unsupported in the stipulated environment. Evidence must match tests actually present in the response.","oracle":[[[".#....",4,[3,2,1,2]],[[2,null,5,null],".#####",0]],[[".....",3,[2,2,1]],[[3,0,2],"#####",3]],[[".....",4,[2]],[[0],"##...",2]],[["....",1,[5,2,2]],[[null,1,null],".##.",3]],[["",0,[1,2]],[[null,null],"",0]],[["#.#",2,[]],[[],"#.#",2]],[["#.#",0,[2]],[[null],"#.#",0]],[[".",0,[1,1]],[[0,null],"#",0]]],"interface_and_format":"Use the requested function name and three arguments. Require a tuple whose first component is a list, whose second is a string, and whose third is an integer, and verify that the caller's widths list is unchanged. The code must compile as Python 3.11 and contain runnable assertions. Require exactly one fenced python block followed by exactly one Status and one Evidence line in that order, with no extra material. The status must describe the test as included and unrun. The evidence must name two distinct boundary scenarios tested by assertions and give the expected outcomes."}
```

### Nontechnical task and frozen source texts

SHA-256 `bc7ea1318a5defb2ee90387fc150c65e392c9c3ac0b2aa0df9a8076187e58509`

```text
你在替松桥社区中心写一份给居民看的积木借用通知。以下是全部资料，活动及地点均为虚构。只依据下列资料，把居民到场前需要知道的事项写清楚。

[A] 5月8日发布的首版海报：2026年5月16日9:00–11:00，在松桥社区中心一楼活动区发放积木套件。居民按到场顺序领取，无需预约。每户限借一套。

[B] 5月12日发布的活动更正：活动日期仍为2026年5月16日。发放时间改为14:00–16:00，地点改到松桥社区中心二楼手作室。凭预约码领取，现场不补登记。首版海报的每户限借一套规则继续执行。

[C] 5月13日发布的服务台安排：本次积木套件免费借用。请在发放当天17:00前交回松桥社区中心一楼服务台。发现套件缺件也要交回，并在交回时告知工作人员。

只输出四行中文正文，依次以“时间地点｜”“领取｜”“费用｜”“归还｜”开头。每行最多55个字符，包含行首标签、标点和来源标记，不计换行。用方括号标注来源，例如[A]。同一行有多项信息时可把相关来源集中标在该行末尾。明确写出发放日期和归还日期，不加标题或附言。
```

### Nontechnical rubric

SHA-256 `3f6c606bc97c2a91fe0f1c9a24a538b18a1e7c5f034e0e0c371aaeda8e61d664`

```json
{"format":"Exactly four lines, in order, with the four literal prefixes requested. Each line is at most 55 Unicode code points, including prefix, punctuation, spaces if any, and source markers, excluding the line separator. Accept semantically equivalent concise Chinese wording, standard date and time notation, and different ordering of applicable markers. Both date mentions must explicitly identify May 16. Require 2026 on the first line for a standalone date, and accept the unambiguous 5月16日 on the return line if the first line already establishes 2026.","claim_anchors":[["时间地点｜","2026年5月16日, 14:00–16:00, 松桥社区中心二楼手作室",["B"]],["领取｜","凭预约码领取；现场不补登记；每户限借一套。Adding [A] alongside [B] is valid because A supplies the retained household rule. A alone cannot substantiate this line.",["B"]],["费用｜","积木套件免费借用",["C"]],["归还｜","5月16日17:00前交回松桥社区中心一楼服务台；缺件也要交回，并告知工作人员。前文完整写出中心名称后，可在此简写为一楼服务台。C sets relative deadline, location, procedure; B resolves date.",["B","C"]]],"errors":"Do not credit superseded 9:00–11:00, first-floor collection, first-come access, or no-reservation. Distinguish second-floor collection from first-floor return. A free loan must not become a gift. Do not infer a deposit, reservation method, or late returns. Judge each claim and applicable source marker."}
```

## Raw agent outputs

For each output below, the outer four-backtick fence and its separator LF are outside the captured text. Each captured payload, including the two status-line spaces where present, is preserved. The file hashes in the execution table apply to the inner text only.

### technical — Candidate (runner_41)

````text
```python
def place_stencils(
    strip: str, cursor: int, widths: list[int]
) -> tuple[list[int | None], str, int]:
    cells = bytearray(strip, "ascii")
    size = len(cells)
    starts: list[int | None] = []

    for width in widths:
        if width > size:
            starts.append(None)
            continue

        available = b"." * width
        start = cells.find(available, cursor)
        if start == -1 and cursor:
            start = cells.find(available)

        if start == -1:
            starts.append(None)
            continue

        end = start + width
        cells[start:end] = b"#" * width
        starts.append(start)
        cursor = end % size

    return starts, cells.decode("ascii"), cursor


if __name__ == "__main__":
    assert place_stencils("", 0, [1, 2]) == ([None, None], "", 0)
    assert place_stencils(".##.", 3, [2, 1, 1]) == (
        [None, 3, 0], "####", 1
    )
    assert place_stencils("#...#", 2, [3]) == ([1], "#####", 4)
    assert place_stencils("..#", 1, []) == ([], "..#", 1)

    widths = [2, 1]
    assert place_stencils("......", 2, widths) == ([2, 4], "..###.", 5)
    assert widths == [2, 1]
```
Status: CANDIDATE — assertion-based self-test included and unrun.  
Evidence: An empty strip with widths `[1, 2]` expects `([None, None], "", 0)`. On `.##.` from cursor `3`, widths `[2, 1, 1]` expect `([None, 3, 0], "####", 1)`, covering a rejected straddle and cursor wrap after an end-aligned placement.
````

### technical — Stable (runner_73)

````text
```python
def place_stencils(
    strip: str, cursor: int, widths: list[int]
) -> tuple[list[int | None], str, int]:
    starts: list[int | None] = []
    size = len(strip)

    for width in widths:
        if width > size:
            starts.append(None)
            continue

        stencil = "." * width
        start = strip.find(stencil, cursor)
        if start == -1:
            # The first search ruled out every start at or after the cursor.
            start = strip.find(stencil)

        if start == -1:
            starts.append(None)
            continue

        end = start + width
        starts.append(start)
        strip = strip[:start] + "#" * width + strip[end:]
        cursor = end % size

    return starts, strip, cursor


if __name__ == "__main__":
    assert place_stencils("", 0, [1, 3]) == ([None, None], "", 0)
    assert place_stencils("..#..", 4, [3]) == ([None], "..#..", 4)
    assert place_stencils(".#.", 1, []) == ([], ".#.", 1)

    widths = [2, 2, 1]
    assert place_stencils("..#..", 4, widths) == ([0, 3, None], "#####", 0)
    assert widths == [2, 2, 1]
```
Status: BLOCKED for runtime verification. Self-test included and unrun.  
Evidence: The empty strip case expects `([None, None], "", 0)`. The width-three case requiring a placement across the row boundary expects `([None], "..#..", 4)`.
````

### nontechnical — Candidate (runner_28)

````text
时间地点｜2026年5月16日14:00–16:00，松桥社区中心二楼手作室。[B]
领取｜凭预约码领取，现场不补登记，每户限借一套。[B]
费用｜免费借用。[C]
归还｜2026年5月16日17:00前交回松桥社区中心一楼服务台，缺件也须交回，交回时告知工作人员。[C]
````

### nontechnical — Stable (runner_56)

````text
时间地点｜2026年5月16日14:00–16:00，松桥社区中心二楼手作室。[B]
领取｜凭预约码领取，现场不补登记，每户限借一套。[B]
费用｜免费借用。[C]
归还｜2026年5月16日17:00前交回松桥社区中心一楼服务台，缺件也须交回，交回时告知工作人员。[C]
````

## Independent blind review output

````markdown
**Packet SHA-256** `45f8a3fb707ec5c2b1f3981367304ef16b00d5f899038877a4fc302b8d68da62`

**Technical runtime** `NOT_RUN_BY_REVIEWER`

| ID | Task completion | Logic and evidence | Constraint compliance | Critical faults | Clarity |
|---|---|---|---|---|---|
| T-K | Complete by inspection | Matches all eight oracle cases by inspection. The fallback search preserves scan order because the first search already ruled out all starts at or after the cursor. Both cited scenarios appear in correct assertions. | Python 3.11 syntax and requested interface. Uses standard-library operations, preserves `widths`, and includes assertions checking that. One Python fence, then Status and Evidence. Status reports the self-test as included and unrun. | None found | The comment explains why an unrestricted fallback search works. |
| T-R | Complete by inspection | Matches all eight oracle cases by inspection. The fallback search preserves scan order for the same reason. Fixed-width writes preserve strip length. Both cited scenarios appear in correct assertions. | Python 3.11 syntax and requested interface. Uses standard-library operations, preserves `widths`, and includes assertions checking that. One Python fence, then Status and Evidence. Status reports the self-test as included and unrun. | None found | The evidence identifies both the rejected straddle and the successful cursor wrap in the same test. |

- **T-K evidence** Empty strip expects `([None, None], "", 0)`. Width three on `"..#.."` from cursor `4` expects `([None], "..#..", 4)`.
- **T-R evidence** Empty strip expects `([None, None], "", 0)`. Widths `[2, 1, 1]` on `".##."` from cursor `3` expect `([None, 3, 0], "####", 1)`.

| ID | Task completion | Factual correctness | Constraint compliance | Critical faults | Clarity |
|---|---|---|---|---|---|
| N-F | All resident-facing information is present. One required source marker is missing. | All factual anchors accepted. | Four ordered literal prefixes, with 42, 27, 11, and 53 code points. Both dates explicitly identify May 16. Return attribution fails the rubric. | Missing `[B]` on the return line. | The pickup and return locations are distinct and easy to find. |
| N-M | All resident-facing information is present. One required source marker is missing. | All factual anchors accepted. | Four ordered literal prefixes, with 42, 27, 11, and 53 code points. Both dates explicitly identify May 16. Return attribution fails the rubric. | Missing `[B]` on the return line. | The pickup and return locations are distinct and easy to find. |

**Claim anchors for N-F and N-M**

| Line | Accepted facts | Source attribution |
|---|---|---|
| 时间地点｜ | 2026年5月16日，14:00–16:00，松桥社区中心二楼手作室 | `[B]` supports all facts. |
| 领取｜ | 凭预约码领取，现场不补登记，每户限借一套 | `[B]` supports all facts. |
| 费用｜ | 积木套件免费借用 | `[C]` supports the claim. |
| 归还｜ | 2026年5月16日17:00前交回松桥社区中心一楼服务台，缺件仍须交回并在交回时告知工作人员 | `[C]` supports the relative deadline, location, and procedure. The line omits `[B]`, which supplies the calendar date. |

Exact offending line in both N-F and N-M:

> 归还｜2026年5月16日17:00前交回松桥社区中心一楼服务台，缺件也须交回，交回时告知工作人员。[C]

**Within-task distinctions**

- **T-K / T-R** Equal under the frozen rubric. T-R additionally tests a valid placement beginning before the cursor and extending past it. Both provide the required two matching boundary scenarios.
- **N-F / N-M** Identical text and identical grades.
````

## Replay of technical checks

Install CPython 3.11 for the target-runtime replay and point the sandbox command at that interpreter within the read-only system mounts. For the observed 3.13 replay use the exact sandbox command below. For each arm, save only the content of the submitted Python fence as `answer.py` with a final LF. Save the technical rubric as `rubric.json` and the checker as `check.py` in the same directory. Run `python3 -I -B sandbox.py <case-directory>`, using a separate directory per arm. To check isolation independently, run the same wrapper against a directory containing only the probe as `check.py`.

### sandbox.py

```python
import ctypes as c
import errno
import os
from pathlib import Path
import resource
import subprocess
import sys
import tempfile

sec=c.CDLL('libseccomp.so.2', use_errno=True)
sec.seccomp_init.argtypes=[c.c_uint32]
sec.seccomp_init.restype=c.c_void_p
sec.seccomp_syscall_resolve_name.argtypes=[c.c_char_p]
sec.seccomp_rule_add.argtypes=[c.c_void_p,c.c_uint32,c.c_int,c.c_uint]
sec.seccomp_export_bpf.argtypes=[c.c_void_p,c.c_int]
sec.seccomp_release.argtypes=[c.c_void_p]
ctx=sec.seccomp_init(0x7fff0000)
if not ctx:
    raise RuntimeError('seccomp initialization failed')
for name in (b'socket', b'socketpair', b'io_uring_setup'):
    nr=sec.seccomp_syscall_resolve_name(name)
    ret=sec.seccomp_rule_add(ctx,0x00050000 | errno.EPERM,nr,0)
    if ret:
        raise OSError(-ret, f'seccomp {name!r}')
with tempfile.TemporaryFile() as policy:
    fd=policy.fileno()
    if sec.seccomp_export_bpf(ctx,fd):
        raise RuntimeError('seccomp BPF export failed')
    sec.seccomp_release(ctx)
    policy.seek(0)
    case=Path(sys.argv[1]).resolve(strict=True)
    command=['bwrap','--unshare-user','--unshare-pid','--unshare-ipc','--unshare-uts',
             '--new-session','--die-with-parent','--clearenv',
             '--ro-bind','/usr','/usr','--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64',
             '--ro-bind',str(case),'/case','--tmpfs','/tmp','--chdir','/case',
             '--seccomp',str(fd),'--','/usr/bin/python3','-I','-B','/case/check.py']
    resource.setrlimit(resource.RLIMIT_CPU,(5,6))
    resource.setrlimit(resource.RLIMIT_AS,(512<<20,512<<20))
    subprocess.run(command,pass_fds=(fd,),check=True,timeout=10)
```

### check.py

```python
import ast
import json
import pathlib
import runpy
import sys

root = pathlib.Path('/case')
impl = root / 'answer.py'
source = impl.read_text()
tree = ast.parse(source, filename=str(impl), feature_version=(3,11))
print('Python 3.11 grammar check: PASS')
assertions = sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
assert assertions > 0, 'no self-test assertions'
ns = runpy.run_path(str(impl), run_name='__main__')
print(f'CPython {sys.version.split()[0]}: submitted self-test exited normally ({assertions} static assert statements)')
fn = ns['place_stencils']
cases = json.loads((root / 'rubric.json').read_text())['oracle']
for num, (args, expected) in enumerate(cases, 1):
    strip, cursor, widths = args
    before = widths[:]
    result = fn(strip, cursor, widths)
    assert widths == before, (num, 'input mutation')
    assert type(result) is tuple and len(result) == 3, (num, result)
    starts, final_strip, final_cursor = result
    assert type(starts) is list and all(x is None or type(x) is int for x in starts), (num, result)
    assert type(final_strip) is str and type(final_cursor) is int, (num, result)
    assert result == tuple(expected), (num, result, expected)
    print(f'case {num}: PASS {result!r}')
print(f'frozen oracle: {len(cases)}/{len(cases)} PASS')
```

### sandbox probe

```python
import errno
import os
import socket
import sys
assert dict(os.environ) == {'PWD': '/case', 'LC_CTYPE': 'C.UTF-8'}, os.environ
assert not os.path.exists('/workspace')
try:
    socket.socket()
except PermissionError as exc:
    assert exc.errno == errno.EPERM
else:
    raise AssertionError('socket unexpectedly allowed')
print(f'CPython {sys.version.split()[0]}: no inherited environment variables (PWD and LC_CTYPE synthesized), workspace unmounted, socket denied')
```
