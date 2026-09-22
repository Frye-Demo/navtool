# Disclosed conference demo fault injection

This directory is an **analysis-only, intentionally unsafe demonstration fixture**,
independent of the Copy messages feature. Do not call or execute it, create archives
for it, or supply it with real data. It has no application or test callers and no
startup code. The SDK-style App project includes this C# source automatically so
the configured C# CodeQL analysis can extract it; no runtime integration is needed.

`DemoOnlyZipSlipAnalysisFixture.cs` deliberately passes an archive entry's unchecked
path to a file operation. The intended published CodeQL finding is `cs/zipslip`
(problem severity **error**, security severity **7.5**, precision **high**):
<https://codeql.github.com/codeql-query-help/csharp/cs-zipslip/>.
An actual alert must be observed; these query properties alone are not evidence
that this revision produced a finding.

A separate functional seed in `Views/MainWindow.Messages.cs` makes clipboard export
use `_messages.ToArray()` rather than `GetVisibleMessages()`. This is wrong when an
interrupted-model popup is open. The retained regression
`MainWindowMessageTests.Copy_messages_uses_popup_model_scope_and_global_notices`
exposes the mismatch for both NOAA and ECMWF. Unrelated models must not be copied;
global notices must still be included.

The correct, seed-free feature checkpoint is
`5b45022635529a3262ee02cfc42525b723095abe`. The seed is a separate commit for honest
before/after comparison, not an accidental feature requirement.

## Reproduction and evidence

Run the product regression without invoking the security fixture:

```sh
dotnet test tests/Navtool.App.Tests/Navtool.App.Tests.csproj --filter FullyQualifiedName~Copy_messages_uses_popup_model_scope_and_global_notices
```

At the initial seed commit `218bac5468bc4a4505cdd85efec15c2617b3f269`, both
model-specific cases fail because the other model's summary is copied. The other
15 Messages popup cases pass. At the correct checkpoint, all 329 App tests and
all four worktree-local native tests pass.

Stage PR: <https://github.com/Frye-Demo/navtool/pull/1>.
Its initial dependency-review run genuinely passed:
<https://github.com/Frye-Demo/navtool/actions/runs/35689582300>.
Security analysis was not scheduled for that first PR event during initial scanner
setup; this documentation-only follow-up requests a fresh PR synchronization after
setup completed. Both intentional faults remain unchanged. Require actual review
and CodeQL evidence for the current revision rather than treating a configured
scanner, a previous revision's green check, or these notes as proof.

## Required final disposition

Restore scoped copying, retain the product regressions and dependency-review
workflow, and **delete this entire demo-only directory**, including the unsafe
fixture. Do not suppress or dismiss alerts, exclude files from analysis, weaken
checks, or remove tests to obtain a green result.

Preparation leaves the stage PR unmerged, with Agent Merge and auto-merge off.
The presenter personally activates Agent Merge during the live demonstration.
Only genuine reviewer comments and analysis results may be presented as findings;
model-generated review output is not deterministic.
