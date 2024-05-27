<script lang="ts">
	import AnalysisPane from '$lib/analysis/AnalysisPane.svelte';
	import { DockviewApi, type DockviewReadyEvent } from 'dockview-core';
	import type { SessionState } from './workspace';
	import Dockview from '$lib/components/dockview/Dockview.svelte';

	export let state: SessionState;
	let panesApi: DockviewApi;

	export function deleteFile(fileId: string) {
		for (const panel of panesApi.panels) {
			let instance = panel.api.getParameters().getInstance();
			instance?.removeFile(fileId);
		}
	}

	function onReady(event: DockviewReadyEvent) {
		panesApi = event.api;

		state.panes.forEach((pane) => {
			panesApi.addPanel({
				id: 'default',
				component: 'default',
				params: {
					state: pane
				}
			});
		});
	}
</script>

<div class="h-full w-full">
	<Dockview {onReady} component={AnalysisPane} />
</div>
