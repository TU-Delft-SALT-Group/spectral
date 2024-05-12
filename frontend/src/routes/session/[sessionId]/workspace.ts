import type { PaneState } from "$lib/analysis/analysis-pane"

// TODO: Modify for tab support (it won't just be an array)
export type WorkspaceState = {
	panes: PaneState[]
}
