<script lang="ts">
	import AnalysisPane from '$lib/analysis/AnalysisPane.svelte';
	import { DockviewApi, type DockviewReadyEvent, type SerializedDockview } from 'dockview-core';
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
		let layout = state.layout as SerializedDockview | undefined; // since layout is only stored from here, everything should be fine

		if (layout !== undefined) layout.panels = {};

		for (const paneId in state.panes) {
			const pane = state.panes[paneId];

			const panel = panesApi.addPanel({
				id: paneId,
				title: pane.title,
				component: 'default',
				renderer: 'onlyWhenVisible',
				tabComponent: 'not default',
				params: {
					state: pane
				}
			});

			if (layout !== undefined) {
				layout.panels[paneId] = panel.toJSON();
			}
		}

		if (layout !== undefined) {
			panesApi.fromJSON(layout);
			for (const panel of panesApi.panels) {
				panel.api.setRenderer('always');
				panel.api.onDidTitleChange((e) => {
					state.panes[panel.id].title = e.title;
				});
			}
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

		panesApi.onDidLayoutChange(() => {
			state.layout = panesApi.toJSON();
		});
	}
</script>

<div class="h-full w-full">
	<Dockview {onReady} component={AnalysisPane} />
</div>
