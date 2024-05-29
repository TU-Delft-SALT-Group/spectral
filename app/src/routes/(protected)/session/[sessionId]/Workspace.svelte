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

		for (const paneId in state.panes) {
			const pane = state.panes[paneId];

			const panel = panesApi.addPanel({
				id: paneId,
				title: pane.title,
				component: 'default',
				renderer: 'always',
				params: {
					state: pane
				},
				tabComponent: 'not default'
			});

			panel.api.onDidTitleChange((e) => {
				state.panes[paneId].title = e.title;
			});
		}

		panesApi.onDidAddPanel((event) => {
			if (event.params === undefined) {
				return;
			}

			state.panes[event.id] = event.params.state;
		});

		panesApi.onDidRemovePanel((event) => {
			if (event.params === undefined) {
				return;
			}

			delete state.panes[event.id];
		});
	}
</script>

<div class="h-full w-full">
	<Dockview {onReady} component={AnalysisPane} />
</div>
