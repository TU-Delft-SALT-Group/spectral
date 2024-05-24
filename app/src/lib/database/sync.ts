import type { PaneState } from '$lib/analysis/analysis-pane';
import used from '$lib/utils';

export async function syncPaneStateToDb(state: PaneState) {
	used(state);
	// console.log('Should be syncing state', state);
}
