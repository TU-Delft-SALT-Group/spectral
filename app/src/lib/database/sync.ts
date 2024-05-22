import type { PaneState } from '$lib/analysis/analysis-pane';

export async function syncPaneStateToDb(state: PaneState) {
	console.log('Should be syncing state', state);
}
