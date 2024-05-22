import { paneState, type PaneState } from '$lib/analysis/analysis-pane';
import { z } from 'zod';

export const workspaceState = z
	.object({
		panes: z.array(paneState)
	})
	.default({
		panes: [paneState.parse(undefined)]
	});

// TODO: Modify for tab support (it won't just be an array)
export type WorkspaceState = {
	panes: PaneState[];
};
